from datetime import datetime
from collections import defaultdict


def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a comprehensive formatted sales report
    """

    # ---------- PRE-CALCULATIONS ----------
    total_transactions = len(transactions)
    total_revenue = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = [t['Date'] for t in transactions]
    date_range = f"{min(dates)} to {max(dates)}"

    # ---------- REGION-WISE ----------
    region_data = defaultdict(lambda: {"sales": 0, "count": 0})
    for t in transactions:
        amt = t['Quantity'] * t['UnitPrice']
        r = t['Region']
        region_data[r]["sales"] += amt
        region_data[r]["count"] += 1

    region_sorted = sorted(
        region_data.items(),
        key=lambda x: x[1]["sales"],
        reverse=True
    )

    # ---------- PRODUCT AGGREGATION ----------
    product_data = defaultdict(lambda: {"qty": 0, "rev": 0})
    for t in transactions:
        product_data[t['ProductName']]["qty"] += t['Quantity']
        product_data[t['ProductName']]["rev"] += t['Quantity'] * t['UnitPrice']

    top_products = sorted(
        product_data.items(),
        key=lambda x: x[1]["qty"],
        reverse=True
    )[:5]

    # ---------- CUSTOMER AGGREGATION ----------
    customer_data = defaultdict(lambda: {"spent": 0, "count": 0})
    for t in transactions:
        amt = t['Quantity'] * t['UnitPrice']
        customer_data[t['CustomerID']]["spent"] += amt
        customer_data[t['CustomerID']]["count"] += 1

    top_customers = sorted(
        customer_data.items(),
        key=lambda x: x[1]["spent"],
        reverse=True
    )[:5]

    # ---------- DAILY TREND ----------
    daily_data = defaultdict(lambda: {"rev": 0, "count": 0, "customers": set()})
    for t in transactions:
        d = t['Date']
        amt = t['Quantity'] * t['UnitPrice']
        daily_data[d]["rev"] += amt
        daily_data[d]["count"] += 1
        daily_data[d]["customers"].add(t['CustomerID'])

    daily_sorted = sorted(daily_data.items())

    best_day = max(daily_sorted, key=lambda x: x[1]["rev"])

    # ---------- API ENRICHMENT ----------
    enriched_count = sum(1 for t in enriched_transactions if t["API_Match"])
    success_rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0

    failed_products = sorted(
        set(t["ProductName"] for t in enriched_transactions if not t["API_Match"])
    )

    # ---------- WRITE REPORT ----------
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 45 + "\n")
        f.write("SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {total_transactions}\n")
        f.write("=" * 45 + "\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 45 + "\n")
        f.write(f"Total Revenue: {total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_transactions}\n")
        f.write(f"Average Order Value: {avg_order_value:,.2f}\n")
        f.write(f"Date Range: {date_range}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 45 + "\n")
        f.write("Region | Total Sales | % of Total | Transactions\n")
        for r, d in region_sorted:
            percent = (d["sales"] / total_revenue) * 100
            f.write(f"{r} | {d['sales']:,.2f} | {percent:.2f}% | {d['count']}\n")
        f.write("\n")

        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 45 + "\n")
        f.write("Rank | Product | Quantity | Revenue\n")
        for i, (p, d) in enumerate(top_products, 1):
            f.write(f"{i} | {p} | {d['qty']} | {d['rev']:,.2f}\n")
        f.write("\n")

        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 45 + "\n")
        f.write("Rank | Customer | Total Spent | Orders\n")
        for i, (c, d) in enumerate(top_customers, 1):
            f.write(f"{i} | {c} | {d['spent']:,.2f} | {d['count']}\n")
        f.write("\n")

        f.write("DAILY SALES TREND\n")
        f.write("-" * 45 + "\n")
        f.write("Date | Revenue | Transactions | Unique Customers\n")
        for d, info in daily_sorted:
            f.write(f"{d} | {info['rev']:,.2f} | {info['count']} | {len(info['customers'])}\n")
        f.write("\n")

        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 45 + "\n")
        f.write(f"Best Selling Day: {best_day[0]} ({best_day[1]['rev']:,.2f})\n")
        f.write("Low Performing Products:\n")
        for p, d in product_data.items():
            if d["qty"] < 10:
                f.write(f"- {p} ({d['qty']} units)\n")
        f.write("\n")

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 45 + "\n")
        f.write(f"Total Products Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")
        f.write("Products Not Enriched:\n")
        for p in failed_products:
            f.write(f"- {p}\n")

    print("Sales report generated successfully")
