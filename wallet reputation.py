import pandas as pd
import json
from datetime import datetime


PATH1 = 'cleaned_nc_transaction.csv'
PATH2 = 'uniswap_transaction.csv'

df_nc = pd.read_csv(PATH1)
df_lp = pd.read_csv(PATH2)
adress = "0x477d7ee756338f0b7f3a8bb6b097a78ccabf70f5"


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


def oldest_date(df):
    date_list = [date for date in df.Date]
    return min(date_list)


def wallet_reputation(adress: str, df_nc, df_lp):
    """

    :param adress:
    :param df_nc:
    :param df_lp:
    :return:
    """
    # select wallet data
    adress_history = df_nc.loc[(df_nc.To == adress.lower())]
    if len(adress_history) == 0:
        return {"Message": "No such adress"}

    # how many LP
    minus_trans = df_nc.loc[(df_nc.From == adress)].sort_values(by="Date")
    plus_trans = df_nc.loc[(df_nc.To == adress)].sort_values(by="Date")
    total_trans = pd.concat([plus_trans, minus_trans]).sort_values(by="Date")
    nc_balance = 0

    for row in total_trans.values:
        if row[2] in ["Claim", "Purchase of NC coins"]:
            nc_balance += row[5]
        elif row[2] == "Transfer" and row[4] == adress:
            nc_balance += row[5]
        else:
            nc_balance -= row[5]
    nc_balance = round(nc_balance)

    #  how long in NC coin
    nc_oldest_date = oldest_date(adress_history)
    today = datetime.today().strftime('%Y-%m-%d')
    how_long_nc = days_between(today, nc_oldest_date)

    # check if the wallet has sold NC
    paper_hands = df_nc.loc[(df_nc.Method == "Sales of NC coins") & (df_nc.From == adress)]
    sold = "No" if len(paper_hands) <= 0 else "Yes"
    proofs = list(paper_hands['Txn Hash'].values)

    # check if wallet add LP
    lp_transaction = df_nc.loc[(df_nc.Method == "Add Liquidity") & (df_nc.From == adress)]
    add_lp = False if len(lp_transaction) <= 0 else True
    if add_lp:
        #  how long in LP
        lp_oldest_date = oldest_date(lp_transaction)
        how_long_lp = days_between(today, lp_oldest_date)

        #  how much lp token was added
        lp_value_plus = df_lp.loc[(df_lp.Method == 'Add Liquidity ET...') & (df_lp.To == adress)]['Quantity']
        lp_value_minus = df_lp.loc[(df_lp.Method == 'Remove Liquidity...') & (df_lp.From == adress)]['Quantity']
        lp_minus = round(sum([value for value in lp_value_minus.values]))
        lp_plus = round(sum([value for value in lp_value_plus.values]))
        lp_total = lp_plus - lp_minus
    else:
        how_long_lp, lp_total = 0, 0

    wallet_reputation = {
        "Time in NC": how_long_nc,
        "Did wallet sell NC Coin": {
            "Paper hands?": sold,
            "Here's the proof": proofs
        },
        "Did wallet add LP": add_lp,
        "Number of time wallet added to LP": how_long_lp,
        "LP Balance": lp_total,
        "NC Coin Balance": nc_balance
    }

    return json.dumps(wallet_reputation, indent=2)


print(wallet_reputation(adress=adress, df_nc=df_nc, df_lp=df_lp))