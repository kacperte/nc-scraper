import pandas as pd


def clean_nc_transaction_file(file_path: str, filename: str) -> None:
    """
    Function that clean scrpaed file with NC coin transaction - mostly delete useless columns, change name in Method
    column and fix Date and Time columns

    :param file_path: File path to scraped file
    :param filename: filename for return DateFrame
    :return: None
    """
    df = pd.read_csv(file_path)
    # Rename right value from Method column to 'Purchase of NC coins'
    con_1 = (df.Method == "Swap Exact Token...") & (df.From == '0x78e16d2facb80ac536887d1376acd4eeedf2fa08')
    con_2 = (df.Method == "Swap")
    con_3 = (df.Method == "Swap ETH For Exa...")
    con_4 = (df.Method == "Swap Exact ETH F...")
    con_5 = (df.Method == "0x415565b0")
    df.loc[con_1 | con_2 | con_3 | con_4 | con_5, 'Method'] = 'Purchase of NC coins'

    # Rename right value from Method column to 'Sales of NC coins'
    con_1 = (df.Method == "Swap Exact Token...") & (df.From != '0x78e16d2facb80ac536887d1376acd4eeedf2fa08')
    con_2 = (df.Method == "0x0773b509")
    df.loc[con_1 | con_2, 'Method'] = 'Sales of NC coins'

    # Rename 'Add Liquidity ET...' to 'Add Liquidity'
    con_1 = (df.Method == "Add Liquidity ET...")
    df.loc[con_1, 'Method'] = 'Add Liquidity'

    # Rename 'Remove Liquidity...' to 'Remove Liquidity'
    con_1 = (df.Method == "Remove Liquidity...")
    df.loc[con_1, 'Method'] = 'Remove Liquidity'

    # Remove useless value form Method column
    value_to_remove = df.loc[
        (df.Method == "Stake") | (df.Method == "Fund") | (df.Method == "0xf574133c") | (df.Method == "0x6d9cec22") | (
                    df.Method == "Claim") | (df.Method == "Unstake")].index
    df = df.drop(value_to_remove, axis=0)

    # Remove useless columns
    df = df.drop(["Unnamed: 0", "Unnamed: 4", "Unnamed: 7"], axis=1)

    # Format to date type
    # split 'Date Time (UTC)' into two columns 'Date' and "Time", then format to 'Date' to datetime format
    df['Date'], df['Time'] = zip(*df['Date Time (UTC)'].str.split().tolist())
    del df['Date Time (UTC)']
    df["Date"] = pd.to_datetime(df["Date"])

    # Save formatted file
    df.to_csv(filename)

