import pandas as pd
import glob
import os

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
            df['month'] = month_map.get(name)
        df_list.append(df)

    return pd.concat(df_list, ignore_index=True)

