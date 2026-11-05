import pandas as pd
import streamlit as st

from analysis import read_one, clean_sales, revenue_by_month, revenue_by_product

st.title("Sales Dashboard")

files = st.file_uploader("Upload your monthly CSV files", type="csv",accept_multiple_files=True)

if files:
    #1
    dfs = []
    for f in files:
        try:
            dfs.append(read_one(f, f.name))
        except ValueError as e:
            st.error(f"Skipped {f"Skipped {f.name}: {e}"}")

    if not dfs:
        st.stop()

    df = pd.concat(dfs, ignore_index=True)

    good, bad = clean_sales(df)
    if good.empty:
        st.errror("No usable rows found.")
        st.stop()

    st.metric("Total revenue", f"{good['price'].mul(good['quantity']).sum():.2f} €")

    #2 
    st.subheader("Revenue by Month")
    st.line_chart(revenue_by_month(good))

    #3
    st.subheader("Revenue by Product")
    st.bar_chart(revenue_by_product(good))


    if len(bad) > 0:
        st.warning(f"{len(bad)} rows could not be used")
        with st.expander("Show these rows"):
            st.dataframe(bad)

else:
    st.info("Upload one or more CSV files to start")