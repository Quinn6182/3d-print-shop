import streamlit as st
import time
import pandas as pd
from PIL import Image

st.set_page_config(page_title="3D Prints By Quinn", page_icon=":computer:")
st.title("3D Printing Shop")
home_tab, upload_tab, catalog_tab, contact_tab, processing_tab = st.tabs(
    ["Home", "Upload", "Catalog", "Contact", "Processing"]
)
with home_tab:
    st.subheader("Home")
    st.write("Welcome to prints by Quinn.")
    st.write("When you order a product, and it finishes meet me at the quad!")
with upload_tab:
    up_file = st.file_uploader("For stl file", type=["stl"])
    if up_file is not None:
        bytesdata = up_file.getvalue()

        with st.form("order_data"):
            name = st.text_input("What is your name?")
            file_name = st.text_input("What is the file name?")
            amount = st.number_input("How many?")
            color = st.text_input("What is the color?")
            st.write("Price will be calculated at a later time")
            submitted = st.form_submit_button("Submit")
            if submitted:
                date = time.ctime(time.time())
                with open("stls/" + date + ".stl", "wb") as f:
                    f.write(bytesdata)
                with open("orders.csv", "a") as f:
                    hash_data = str(
                        hash(f"{color},{file_name},{amount},TBD,{name},{date},TBD\n")
                    )
                    f.write(
                        f"{color},{file_name},{amount},TBD,{name},{date},{hash_data},TBD\n"
                    )
                st.subheader("Submitted! 😀")
                st.write(
                    "Keep this information, this is your order number used for tracking"
                )
                st.write(hash_data)
                with open("order-tracking.csv", "a") as f:
                    f.write(f"0,TBD,{hash_data}\n")
with contact_tab:
    st.subheader("Use this to contact me!")
    with st.form("contact"):
        name = st.text_input("What is your name?")
        email = st.text_input("What is your email?")
        message = st.text_input("What is your message?")
        sumbitted = st.form_submit_button("Submit")
        if sumbitted:
            with open("messages.csv", "a") as f:
                f.write(f"{name},{message},{email}\n")
            st.subheader("Submitted!")
with processing_tab:
    st.subheader("Use this to track your order!")
    order_tracking = pd.read_csv("order-tracking.csv")
    tracking_number = st.text_input("What is your tracking number?")
    if tracking_number:
        for i in range(len(order_tracking)):
            if str(order_tracking.iloc[i][2]) == str(tracking_number):
                st.progress(int(order_tracking.iloc[i]["PercentDone"]), "Progress")
                st.write(order_tracking.iloc[i][1])
with catalog_tab:
    col1, col2 = st.columns(2)
    catalog = pd.read_csv("catalog.csv")
    names = []
    for i in range(len(catalog)):
        img = Image.open(catalog.iloc[i]["imagePath"])
        if i % 2 == 0:
            col1.image(img)
            col1.write(catalog.iloc[i][3])
        else:
            col2.image(img)
            col2.write(catalog.iloc[i][3])
        names.append(catalog.iloc[i][3])
    option = st.selectbox("What would you like? ", names)
    for i, v in enumerate(names):
        if option == v:
            sizes = catalog.iloc[i][1].split("/")
            size = st.selectbox("What size?", sizes)
            colors = catalog.iloc[i][2].split("/")
            color = st.selectbox("What color?", colors)
            amount = st.number_input("How many?")
            name = st.text_input("What is your name?")
            for k, j in enumerate(sizes):
                if size == j:
                    total = int(catalog.iloc[i][4].split("/")[k].split("$")[1]) * amount
                    st.write(f"Total: ${total}")
            date = time.ctime(time.time())
            order = st.button("Order!")
            if order:
                with open("orders.csv", "a") as f:
                    hash_data = str(
                        hash(
                            f"{color},{option},{amount},{total},{name},{date},{size}\n"
                        )
                    )
                    f.write(
                        f"{color},{option},{amount},{total},{name},{date},{hash_data},{size}\n"
                    )
                st.subheader("Ordered! :smile:")
                st.write("Keep this order number so you can track your order!")
                st.write(hash_data)
                with open("order-tracking.csv", "a") as f:
                    f.write(f"0,TBD,{hash_data}\n")
