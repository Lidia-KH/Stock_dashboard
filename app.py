import streamlit as st
from database import init_db
from services import add_product, get_products, move_stock, get_alert_products, update_ptoduct, delete_product, get_movements
import pandas as pd

init_db()

st.set_page_config(page_title="StockPilot", page_icon= "🗂", layout="wide")
tab1, tab2 = st.tabs(["Dashboard", "Stock History"], width="stretch")

st.markdown("""
    <style>
        .stMetric {
            padding: 15px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# st.title("StockPilot  Inventory Management")
# with tab1:
st.sidebar.header("Add Product")
name = st.sidebar.text_input("Product Name")
sku = st.sidebar.text_input("SKU")
min_threshold = st.sidebar.number_input("Min Stock", min_value=0)
price = st.sidebar.number_input("Unit Price", min_value=0.0)

if st.sidebar.button("Add Product"):
    add_product(name, sku, min_threshold, price)
    st.success("Product added")


st.sidebar.header("Stock Movement")
products = get_products()
product_options = {f"{p.name} ({p.sku})": p.id for p in products}

if product_options:
    selected = st.sidebar.selectbox("Product", list(product_options.keys()))
    move_type = st.sidebar.selectbox("Type", ["IN","OUT"])
    quantity = st.sidebar.number_input("Quantity", min_value=1)

    if st.sidebar.button("Apply Movement"):
        success = move_stock(product_options[selected], move_type, quantity)
        if success:
            st.success("Movement recorded")
        else:
            st.error("Invalid movement")

with tab1:
    st.subheader("Products")

    products = get_products()
    alerts = get_alert_products()

    total_inventory_value = sum(p.quantity * p.price for p in products)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Products", len(products))
    col2.metric("Products in Alert", len(get_alert_products()))
    col3.metric("Total Units", sum(p.quantity for p in products))
    col4.metric("Total Inventory Value", f"{total_inventory_value: .2f}")

    if products:
        data = []
        for p in products:
            stock_value = p.quantity * p.price
            status = "Low Stock" if p.quantity < p.min_threshold else "OK"
            data.append({
                "Name": p.name,
                "SKU": p.sku,
                "Quantity": p.quantity,
                "Unit Price": p.price,
                "Stock Value": stock_value,
                "Min Threshold": p.min_threshold,
                "Status": status
            })

        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)



    selected_product = st.selectbox(
        "Select product to edit",
        products,
        format_func=lambda x: f"{x.name}  ({x.sku})"
    )

    if selected_product:
        new_name = st.text_input("Product Name", value=selected_product.name)
        new_sku = st.text_input("SKU", value=selected_product.sku)
        new_min = st.number_input("Min Threshold", value=selected_product.min_threshold)
        new_price = st.number_input("Price", value=selected_product.price)

        col1, col2 = st.columns(2)

        if col1.button("Update"):
            update_ptoduct(selected_product.id, new_name, new_sku, new_min, new_price)
            st.success("Updated")

        if col2.button("Delete"):
            delete_product(selected_product.id)
            st.warning("Deleted")

    st.subheader("Products in Alert")

    if alerts:
        for p in alerts:
            st.warning(f"{p.name} ({p.sku}) | Current: {p.quantity} | Minimum: {p.min_threshold}")
    else:
        st.success("No products in alert")


with tab2:
    st.subheader("Stock Movements History")

    movements = get_movements()

    if movements:
        history_data= []
        for m in movements:
            history_data.append({
                "Product ID": m.product_id,
                "Type": m.type,
                "Quantity": m.quantity,
                "Date": m.date
            })
        
        history_df = pd.DataFrame(history_data)
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("No movements recorded")