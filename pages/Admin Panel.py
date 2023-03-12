import streamlit as st
import pandas as pd
orders = pd.read_csv('orders.csv')
messages = pd.read_csv('messages.csv')
order_tracking = pd.read_csv('order-tracking.csv')
name = st.text_input('What is the username?')
password = st.text_input('What is the password?')
login = {
    'Quinn' : 'enterthevoid',
    'Father': "I don't care."
}


if name:
    for i in login:
        if i == name:
            if login[i] == password:
                st.write("Success")
                st.table(data=orders)
                st.table(data=messages)
                edited = st.experimental_data_editor(order_tracking)
                button = st.button('Change')
                if button:
                    with open("order-tracking.csv", 'w') as f:
                        f.write("PercentDone, Status, OrderNumber\n")
                        for i in range(len(edited)):
                            cur = edited.iloc[i]
                            f.write(f"{cur[0]},{cur[1]},{cur[2]}\n")

