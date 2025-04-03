from figure_builder_mod import DataDisplay
from oracle_module import oracle, new_table, table
from pdf_builder_mod import PDFReport
from web_scraper import CoinMarketCapScraper

def build_pdf(data:list):
    f_pdf = PDFReport("Coin Market Cap Report", "Coin market Cap Summary")

def define_all_objects(oracle_conn:oracle) -> list:
    tables = oracle_conn.get_all_tables()
    table_objects = []

    for tbl_name in tables:
        fields = oracle_conn.get_table_fields(tbl_name)
        table_objects.append(table(tbl_name.lower(), **fields))

    return table_objects

def start_func(database:oracle):
    """This function makes the initial insertion of data for later comparison"""
    tbl_lst = define_all_objects(oracle_conn=database)

    web_scraper = CoinMarketCapScraper(pages=1)
    scraped_data = web_scraper.scrape()

    index = 0
    new_data_lst = []
    for data in scraped_data:
        data[2] = data[2].strip('$')
        data[2] = data[2].replace(',',"")
        data[2] = float(data[2])
        new_data_lst.append([index, data[0], data[2], data[3], data[1]])
        index += 1

    for data in new_data_lst:
        database.insert_rec(tbl_lst[0], data)

def sanitize_data(current_data:list)->list:
    """Makes scraped data comparible with the data in the database"""
    sanatized_data = []

    index = 0
    for data in current_data:
        data[2] = data[2].strip('$')
        data[2] = data[2].replace(',',"")
        data[2] = float(data[2])
        sanatized_data.append([index, data[0], data[2], data[3], data[1]])
        index += 1

    return sanatized_data 

def retrieve_data(database:oracle, table_name:str) -> list:
    return sanitize_data(database.get_data(table=table_name))


def main():
    print("Connecting to the database")
    database = oracle() #connects to database
    web_scraper = CoinMarketCapScraper(pages=1) #instantiates object, defines pages
    
    web_data = web_scraper.scrape() #scrapes data from web page
    
    tables_lst = define_all_objects(database) #defines all the objects from function
    tbl_name = tables_lst[0].table_name #retrieves unrecognized attribute to bypass str declaration
    db_data = retrieve_data(database=database, table_name=tbl_name) #retrieves last input data from tbl

    #compare the data
    #build a report with figures and make it comparable, explain the differences

    database.close_connection() #ends connected session with oracle database

if __name__ == "__main__":
    main()