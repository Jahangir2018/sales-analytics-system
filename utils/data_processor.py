def clean_and_process_data(raw_records):
    cleaned_data = []
    invalid_count = 0

    for record in raw_records:
        parts = record.split("|")
        if len(parts) != 8:
            invalid_count += 1
            continue

        tid, date, pid, pname, qty, price, cid, region = parts

        if not tid.startswith("T") or not cid or not region:
            invalid_count += 1
            continue

        try:
            qty = int(qty.replace(",", ""))
            price = float(price.replace(",", ""))
        except:
            invalid_count += 1
            continue

        if qty <= 0 or price <= 0:
            invalid_count += 1
            continue

        pname = pname.replace(",", " ")

        cleaned_data.append({
            "transaction_id": tid,
            "date": date,
            "product_id": pid,
            "product_name": pname,
            "quantity": qty,
            "unit_price": price,
            "customer_id": cid,
            "region": region,
            "total": qty * price
        })

    print(f"Total records parsed: {len(raw_records)}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(cleaned_data)}")

    return cleaned_data

# ---------- PART 1 ----------

def parse_transactions(raw_lines):
    transactions = []

    for line in raw_lines:
        parts = line.split('|')
        if len(parts) != 8:
            continue

        tid, date, pid, pname, qty, price, cid, region = parts
        pname = pname.replace(",", " ")

        try:
            qty = int(qty.replace(",", ""))
            price = float(price.replace(",", ""))
        except ValueError:
            continue

        transactions.append({
            'TransactionID': tid,
            'Date': date,
            'ProductID': pid,
            'ProductName': pname,
            'Quantity': qty,
            'UnitPrice': price,
            'CustomerID': cid,
            'Region': region
        })

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid = []
    invalid = 0

    for t in transactions:
        if (
            t['Quantity'] <= 0 or
            t['UnitPrice'] <= 0 or
            not t['TransactionID'].startswith('T') or
            not t['ProductID'].startswith('P') or
            not t['CustomerID'].startswith('C') or
            not t['Region']
        ):
            invalid += 1
            continue
        valid.append(t)

    regions = set(t['Region'] for t in valid)
    amounts = [t['Quantity'] * t['UnitPrice'] for t in valid]

    print("Available regions:", regions)
    print("Transaction amount range:", min(amounts), "-", max(amounts))

    total_valid = len(valid)

    if region:
        valid = [t for t in valid if t['Region'] == region]

    filtered_by_region = total_valid - len(valid)

    if min_amount is not None:
        valid = [t for t in valid if t['Quantity'] * t['UnitPrice'] >= min_amount]

    if max_amount is not None:
        valid = [t for t in valid if t['Quantity'] * t['UnitPrice'] <= max_amount]

    filtered_by_amount = total_valid - filtered_by_region - len(valid)

    summary = {
        'total_input': len(transactions),
        'invalid': invalid,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(valid)
    }

    return valid, invalid, summary


# ---------- PART 2 ----------

def calculate_total_revenue(transactions):
    return sum(t['Quantity'] * t['UnitPrice'] for t in transactions)


def region_wise_sales(transactions):
    regions = {}
    total = calculate_total_revenue(transactions)

    for t in transactions:
        r = t['Region']
        amt = t['Quantity'] * t['UnitPrice']

        if r not in regions:
            regions[r] = {'total_sales': 0, 'transaction_count': 0}

        regions[r]['total_sales'] += amt
        regions[r]['transaction_count'] += 1

    for r in regions:
        regions[r]['percentage'] = round((regions[r]['total_sales'] / total) * 100, 2)

    return dict(sorted(regions.items(), key=lambda x: x[1]['total_sales'], reverse=True))


def top_selling_products(transactions, n=5):
    products = {}

    for t in transactions:
        p = t['ProductName']
        q = t['Quantity']
        amt = q * t['UnitPrice']

        if p not in products:
            products[p] = {'qty': 0, 'rev': 0}

        products[p]['qty'] += q
        products[p]['rev'] += amt

    result = [(p, d['qty'], d['rev']) for p, d in products.items()]
    result.sort(key=lambda x: x[1], reverse=True)

    return result[:n]


def customer_analysis(transactions):
    customers = {}

    for t in transactions:
        c = t['CustomerID']
        amt = t['Quantity'] * t['UnitPrice']
        p = t['ProductName']

        if c not in customers:
            customers[c] = {
                'total_spent': 0,
                'purchase_count': 0,
                'products_bought': set()
            }

        customers[c]['total_spent'] += amt
        customers[c]['purchase_count'] += 1
        customers[c]['products_bought'].add(p)

    for c in customers:
        customers[c]['avg_order_value'] = round(
            customers[c]['total_spent'] / customers[c]['purchase_count'], 2
        )
        customers[c]['products_bought'] = list(customers[c]['products_bought'])

    return dict(sorted(customers.items(), key=lambda x: x[1]['total_spent'], reverse=True))


def daily_sales_trend(transactions):
    daily = {}

    for t in transactions:
        d = t['Date']
        amt = t['Quantity'] * t['UnitPrice']
        c = t['CustomerID']

        if d not in daily:
            daily[d] = {'revenue': 0, 'transaction_count': 0, 'customers': set()}

        daily[d]['revenue'] += amt
        daily[d]['transaction_count'] += 1
        daily[d]['customers'].add(c)

    for d in daily:
        daily[d]['unique_customers'] = len(daily[d]['customers'])
        del daily[d]['customers']

    return dict(sorted(daily.items()))


def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)

    peak_date = None
    max_revenue = 0
    tx_count = 0

    for d, info in daily.items():
        if info['revenue'] > max_revenue:
            peak_date = d
            max_revenue = info['revenue']
            tx_count = info['transaction_count']

    return (peak_date, max_revenue, tx_count)


def low_performing_products(transactions, threshold=10):
    products = {}

    for t in transactions:
        p = t['ProductName']
        q = t['Quantity']
        amt = q * t['UnitPrice']

        if p not in products:
            products[p] = {'qty': 0, 'rev': 0}

        products[p]['qty'] += q
        products[p]['rev'] += amt

    low = [(p, d['qty'], d['rev']) for p, d in products.items() if d['qty'] < threshold]
    low.sort(key=lambda x: x[1])

    return low
