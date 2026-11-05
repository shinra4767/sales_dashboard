import pandas as pd
import glob
import os
import warnings

def load_csv_folder(folder_path, month_from_filename=True):

    month_map = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }

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

def clean_sales(df):

    df = df.copy()
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df ['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')

    mask = (
        df[['price', 'quantity']].notna().all(axis=1)
        & (df['price'] >= 0)
        &(df['quantity'] >= 0)
        )
    return df[mask], df[~mask]

def revenue_by_month(df):
    df = df.copy()
    df['revenue'] = df['price'] * df['quantity']
    return df.groupby('month', dropna= False)['revenue'].sum()

def revenue_by_product(df):
    df = df.copy()
    df['revenue'] = df['price'] * df['quantity']
    return df.groupby('product')['revenue'].sum()


def main():

    df = load_csv_folder("sample_data")
    good, bad = clean_sales(df)
    print(len(good),"good rows", len(bad),"bad rows" )
    print(revenue_by_month(good))
    print(revenue_by_product(good))
    print(revenue_by_product(good).sum())

if __name__ == "__main__":
    main()