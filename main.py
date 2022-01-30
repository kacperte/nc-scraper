from scraper import scrap_polygonscan
from data_cleaning import clean_nc_transaction_file


URL = 'https://polygonscan.com/token/0x64a795562b02830ea4e43992e761c96d208fc58d'
nc_transaction_filename = "nc_transaction.csv"
after_cleaning_filename = "cleaned_nc_transaction.csv"

if __name__ == '__main__':
    scrap_polygonscan(url=URL, filename=nc_transaction_filename)
    clean_nc_transaction_file(file_path=nc_transaction_filename, filename=after_cleaning_filename)
