import pandas as pd
import streamlit as st

from analysis import read_one, clean_sales, revenue_by_month, revenue_by_product, filter_sales

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

    with st.sidebar:
        st.header("Filters")
        all_products = sorted(good["product"].unique())
        chosen_products = st.multiselect("Products", all_products, default=all_products)

        all_months = sorted(good["month"].unique())
        chosen_months = st.multiselect("Months", all_months, default=all_months)

    filtered = filter_sales(good, chosen_products, chosen_months)

    if filtered.empty:
        st.warning("Nothing matches these filters")
        st.stop()

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

    st.download_button(
        "Download cleaned data (CSV)",
        filtered.to_csv(index=False, sep=";", decimal=","),
        file_name="sales_clean.csv",
        mime="text/csv,"
    )

else:
    st.info("Upload one or more CSV files to start")