# EDA Project

# Step 1: Import libraries
import pandas as pd
import numpy as np
import random
from faker import Faker

# For reproducibility
random.seed(42)
fake = Faker()
Faker.seed(42)

# Step 2: Define base data

categories = {
    "Furniture": ["Office Chair", "Study Table", "Bookshelf", "Sofa", "Dining Table"],
    "Office Supplies": ["Pen", "Notebook", "Stapler", "File Folder", "Calculator"],
    "Electronics": ["Laptop", "Monitor", "Keyboard", "Mouse", "Headphone"],
    "Groceries": ["Milk", "Bread", "Eggs", "Fruits", "Vegetables", "Snacks", "Rice"]
}

regions = ["North", "South", "East", "West"]
payment_modes = ["Credit Card", "UPI", "Bank Transfer", "Cash", "Net Banking"]
delivery_status = ["Delivered", "Pending", "Cancelled", "Returned"]
customer_segments = ["Consumer", "Corporate", "Home Office"]


# Step 3: Generate dataset

records = []  # empty list to store all rows of data

for i in range(1000):  # generating 1000 records

    # --- Order Info ---
    order_id = f"ORD{1000 + i}"
    order_date = fake.date_between(start_date='-2y', end_date='today')
    ship_date = order_date + pd.Timedelta(days=random.randint(1, 7))

    # --- Customer Info ---
    customer_name = fake.name()
    customer_id = f"CUST{random.randint(100, 999)}"
    customer_segment = random.choice(customer_segments)

    # --- Product Info ---
    category = random.choice(list(categories.keys()))
    product_name = random.choice(categories[category])
    product_id = f"PROD{random.randint(1000, 9999)}"

    # --- Location Info ---
    region = random.choice(regions)
    state = fake.state()
    city = fake.city()

    # --- Pricing Info ---
    quantity = random.randint(1, 10)
    unit_price = round(random.uniform(100, 5000), 2)
    discount = random.choice([0, 5, 10, 15, 20])

    sales_amount = round(quantity * unit_price * (1 - discount / 100), 2)
    cost_price = round(unit_price * random.uniform(0.5, 0.9), 2)

    # --- Delivery Status ---
    delivery = random.choice(delivery_status)

    # --- Profit Logic based on Delivery Status ---
    #
    #  Delivered  → Full profit earned
    #  Pending    → 0  (order not completed yet)
    #  Cancelled  → 0  (order never happened)
    #  Returned   → Negative (refund + return penalty)
    #
    base_profit = round((unit_price - cost_price) * quantity * (1 - discount / 100), 2)

    if delivery == "Delivered":
        profit = base_profit

    elif delivery == "Pending":
        profit = 0.0

    elif delivery == "Cancelled":
        profit = 0.0

    elif delivery == "Returned":
        return_penalty = round(base_profit * random.uniform(0.1, 0.3), 2)
        profit = -return_penalty

    # --- Inventory Info ---
    stock_left = random.randint(0, 50)

    if stock_left < 10:
        auto_reorder = "Yes"
        reorder_quantity = random.randint(20, 50)
    else:
        auto_reorder = "No"
        reorder_quantity = 0

    # --- Supplier Info ---
    supplier_name = fake.company()
    supplier_email = fake.email()
    payment_mode = random.choice(payment_modes)

    # Append row as a dictionary to the records list
    records.append({
        "Order ID": order_id,
        "Order Date": order_date,
        "Ship Date": ship_date,
        "Customer Name": customer_name,
        "Customer ID": customer_id,
        "Customer Segment": customer_segment,
        "Category": category,
        "Product Name": product_name,
        "Product ID": product_id,
        "Region": region,
        "State": state,
        "City": city,
        "Quantity": quantity,
        "Unit Price": unit_price,
        "Discount (%)": discount,
        "Sales Amount": sales_amount,
        "Cost Price": cost_price,
        "Profit": profit,
        "Stock Left": stock_left,
        "Auto Reorder": auto_reorder,
        "Reorder Quantity": reorder_quantity,
        "Supplier Name": supplier_name,
        "Supplier Email": supplier_email,
        "Payment Mode": payment_mode,
        "Delivery Status": delivery
    })


# Step 4: Create DataFrame and save to CSV

df = pd.DataFrame(records)

try:
    df.to_csv("Superstore_Management_Dataset.csv", index=False)
    print("Dataset generated and saved successfully! File saved as 'Superstore_Management_Dataset.csv'")
except PermissionError:
    print("Please close the file 'Superstore_Management_Dataset.csv' if it's open and try again.")
