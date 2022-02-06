from scraper import scrap_polygonscan
from data_cleaning import clean_nc_transaction_file


URL_1 = 'https://polygonscan.com/token/0x64a795562b02830ea4e43992e761c96d208fc58d'
URL_2 = 'https://polygonscan.com/token/0x78e16D2fACb80ac536887D1376ACD4EeeDF2fA08'
nc_transaction_filename = "nc_transaction.csv"
after_cleaning_filename = "cleaned_nc_transaction.csv"
uniswap_transaction_filename = "uniswap_transaction.csv"

if __name__ == '__main__':
    # NC coin transaction - https://polygonscan.com/token/0x64a795562b02830ea4e43992e761c96d208fc58d
    scrap_polygonscan(url=URL_1, filename=nc_transaction_filename)
    clean_nc_transaction_file(file_path=nc_transaction_filename, filename=after_cleaning_filename)

    # Uniswap V2 transaction - https://polygonscan.com/token/0x78e16D2fACb80ac536887D1376ACD4EeeDF2fA08
    scrap_polygonscan(url=URL_2, filename=uniswap_transaction_filename)
