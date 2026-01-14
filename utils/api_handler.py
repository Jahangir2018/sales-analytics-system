import requests


# ---------------- Task 3.1 (a) ----------------
def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """

    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        products = []
        for p in data.get("products", []):
            products.append({
                "id": p.get("id"),
                "title": p.get("title"),
                "category": p.get("category"),
                "brand": p.get("brand"),
                "price": p.get("price"),
                "rating": p.get("rating")
            })

        print(f"Fetched {len(products)} products from API")
        return products

    except requests.exceptions.RequestException as e:
        print("API connection failed:", e)
        return []


# ---------------- Task 3.1 (b) ----------------
def create_product_mapping(api_products):
    """
    Creates mapping of product ID to product info
    """

    mapping = {}

    for p in api_products:
        pid = p.get("id")
        if pid is not None:
            mapping[pid] = {
                "title": p.get("title"),
                "category": p.get("category"),
                "brand": p.get("brand"),
                "rating": p.get("rating")
            }

    return mapping


# ---------------- Task 3.2 ----------------
def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """

    enriched = []

    for t in transactions:
        new_t = t.copy()

        try:
            # Extract numeric ID: P101 -> 101
            numeric_id = int("".join(filter(str.isdigit, t["ProductID"])))

            if numeric_id in product_mapping:
                api_info = product_mapping[numeric_id]
                new_t["API_Category"] = api_info["category"]
                new_t["API_Brand"] = api_info["brand"]
                new_t["API_Rating"] = api_info["rating"]
                new_t["API_Match"] = True
            else:
                new_t["API_Category"] = None
                new_t["API_Brand"] = None
                new_t["API_Rating"] = None
                new_t["API_Match"] = False

        except Exception:
            new_t["API_Category"] = None
            new_t["API_Brand"] = None
            new_t["API_Rating"] = None
            new_t["API_Match"] = False

        enriched.append(new_t)

    # Save to file
    save_enriched_data(enriched)
    print("Sales data enriched and saved successfully")

    return enriched


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions to file
    """

    header = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("|".join(header) + "\n")

        for t in enriched_transactions:
            row = [
                str(t.get("TransactionID")),
                str(t.get("Date")),
                str(t.get("ProductID")),
                str(t.get("ProductName")),
                str(t.get("Quantity")),
                str(t.get("UnitPrice")),
                str(t.get("CustomerID")),
                str(t.get("Region")),
                str(t.get("API_Category")),
                str(t.get("API_Brand")),
                str(t.get("API_Rating")),
                str(t.get("API_Match"))
            ]
            f.write("|".join(row) + "\n")
