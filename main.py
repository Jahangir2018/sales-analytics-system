# ================================
# SALES ANALYTICS SYSTEM - MAIN
# ================================

from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data
)
from utils.report_generator import generate_sales_report

DATA_FILE = "data/sales_data.txt"


def main():
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # 1. Read sales data
        print("[1/10] Reading sales data...")
        raw_data = read_sales_data(DATA_FILE)
        print(f"✓ Successfully read {len(raw_data)} transactions")

        # 2. Parse and clean data
        print("[2/10] Parsing and cleaning data...")
        parsed_transactions = parse_transactions(raw_data)
        print(f"✓ Parsed {len(parsed_transactions)} records")

        # 3. Display filter options
        print("[3/10] Filter Options Available:")
        valid_transactions, invalid_count, summary = validate_and_filter(parsed_transactions)

        # 4. Validation summary
        print("[4/10] Validating transactions...")
        print(f"✓ Valid: {summary['final_count']} | Invalid: {summary['invalid']}")

        # 5. Perform data analysis
        print("[5/10] Analyzing sales data...")
        total_revenue = calculate_total_revenue(valid_transactions)
        region_sales = region_wise_sales(valid_transactions)
        top_products = top_selling_products(valid_transactions)
        customers = customer_analysis(valid_transactions)
        daily_trend = daily_sales_trend(valid_transactions)
        peak_day = find_peak_sales_day(valid_transactions)
        low_products = low_performing_products(valid_transactions)
        print("✓ Analysis complete")

        # 6. Fetch API data
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)
        print(f"✓ Fetched {len(api_products)} products")

        # 7. Enrich sales data
        print("[7/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
        enriched_count = sum(1 for t in enriched_transactions if t["API_Match"])
        success_rate = (enriched_count / len(valid_transactions)) * 100
        print(f"✓ Enriched {enriched_count}/{len(valid_transactions)} transactions ({success_rate:.1f}%)")

        # 8. Save enriched data (handled inside enrich function)
        print("[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt")

        # 9. Generate report
        print("[9/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_transactions)
        print("✓ Report saved to: output/sales_report.txt")

        # 10. Complete
        print("[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("❌ An error occurred during execution")
        print("Error details:", str(e))


if __name__ == "__main__":
    main()
