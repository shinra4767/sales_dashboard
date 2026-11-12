import pandas as pd
import glob
import os
import warnings
month_map = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
}
MONTH_LABELS = {number: f"{number:02d} {name}" for name, number in month_map.items()}

def load_csv_folder(folder_path, month_from_filename=True):

    all_files = glob.glob(os.path.join(folder_path, "*.csv"))
    if not all_files:
        raise FileNotFoundError(f"No CSV files found in {folder_path}")

    df_list = []
    for f in all_files:
        df = pd.read_csv(f)
        if month_from_filename:
            name = os.path.splitext(os.path.basename(f))[0].lower()
            month = month_map.get(name)
            if month is None:
                warnings.warn(f"Unkown month in filename: '{name}'")
            df['month'] = month
        df_list.append(df)

    return pd.concat(df_list, ignore_index=True)

def read_one(source, name):
    df = pd.read_csv(source, sep=None, engine ="python", encoding="utf-8-sig")
    stem = os.path.splitext(name)[0].lower()
    month = month_map.get(stem)
    if month is None:
        raise ValueError("filename must be a month (jan, feb, mar,...)")

    required = {"product", "price", "quantity"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"missing columns {sorted(missing)}")

    df["month"] = month
    df["source_file"] = name
    return df

def clean_sales(df):

    df = df.copy()
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df ['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')

    df['reason']= ''
    df.loc[df['price'].isna(),'reason'] = 'price is not a number'
    df.loc[df['quantity'].isna(), 'reason'] = 'quantity is missing or not a number'
    df.loc[(df['price'] < 0), 'reason'] = 'negative price'
    df.loc[(df['quantity'] < 0), 'reason'] = 'negative quantity'

    bad_mask = df['reason'] != ''
    good = df[~bad_mask].drop(columns='reason')
    good['revenue']= good['price'] * good['quantity']
    return good, df[bad_mask]

def revenue_by_month(df):
    df = df.copy()
    df['revenue'] = df['price'] * df['quantity']
    result = df.groupby('month', dropna =False)['revenue'].sum()
    return result.rename(index=MONTH_LABELS)


def revenue_by_product(df):
    df = df.copy()
    df['revenue'] = df['price'] * df['quantity']
    return df.groupby('product')['revenue'].sum()

def filter_sales(df, products, months):
    return df[df["product"].isin(products)& df["month"].isin(months)]

def main():

    df = load_csv_folder("sample_data")
    good, bad = clean_sales(df)
    print(len(good),"good rows", len(bad),"bad rows" )
    print(revenue_by_month(good))
    print(revenue_by_product(good))
    print(revenue_by_product(good).sum())

if __name__ == "__main__":
    main()