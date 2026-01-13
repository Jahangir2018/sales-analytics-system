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
