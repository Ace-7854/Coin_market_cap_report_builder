from figure_builder_mod import DataDisplay
from oracle_module import oracle, table
from pdf_builder_mod import PDFReport
from web_scraper import CoinMarketCapScraper

def build_pdf(db_data: list, web_data: list):
    # Step 1: Identify changes in position and new entries
    db_top_10 = {item[1]: index for index, item in enumerate(sorted(db_data, key=lambda x: x[2], reverse=True)[:10])}
    web_top_10 = {item[1]: index for index, item in enumerate(sorted(web_data, key=lambda x: x[2], reverse=True)[:10])}
    
    position_changes = []
    new_entries = []
    for name, new_rank in web_top_10.items():
        if name in db_top_10:
            old_rank = db_top_10[name]
            if old_rank != new_rank:
                position_changes.append(f"{name} moved from position {old_rank + 1} to {new_rank + 1}.")
        else:
            new_entries.append(f"{name} entered the top 10 at position {new_rank + 1}.")
    
    # Step 2: Generate summary
    summary = "\n".join(position_changes + new_entries)
    if not summary:
        summary = "No significant changes in the top 10 cryptocurrencies."
    
    # Step 3: Generate Figures
    labels = list(web_top_10.keys())  # Use cryptocurrency names as labels
    data = [item[2] for item in sorted(web_data, key=lambda x: x[2], reverse=True)[:10]]
    figure_paths = ["assets/figures/bar_chart.png", "assets/figures/line_chart.png", "assets/figures/pie_chart.png", "assets/figures/table.png"]
    titles = ["Top 10 Cryptos by Market Cap", "Market Cap Trends", "Market Share of Top 10", "Top 10 Data Table"]
    
    table_data = [
        [rank + 1, item[1], f"${float(item[2]):,.2f}", f"{item[3]}", item[4]]
        for rank, item in enumerate(sorted(web_data, key=lambda x: float(x[2]), reverse=True)[:10])
    ]

    # Pass `table_data` explicitly
    DataDisplay.make_figures(labels, data, figure_paths, titles, ["Crypto", "Market Cap ($)"], table_data=table_data)

    # Step 4: Build PDF Report
    report = PDFReport("Coin Market Cap Report", "Crypto Market Changes")
    report.add_title_page()
    report.add_summary(summary)
    for path, title in zip(figure_paths, titles):
        report.add_figure(path, title)
    report.save_pdf(f"assets/reports/crypto_report{report.get_sanitized_timestamp()}.pdf")


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
    lst = database.get_data(table=table_name)
    for i in range(len(lst)):
        lst[i] = list(lst[i])

    return lst

def display_data(db_data:list, web_data:list):
        print("     Database Data   ")
        print("---------------------")
        for data in db_data:
            print(data, sep="\n")
        print("\n")
        print("     Website Data    ")
        print("---------------------")
        for data in web_data:
            print(data, sep="\n")
    
def main():
    print("Connecting to the database...")
    database = oracle() #connects to database
    tables_lst = define_all_objects(database) #defines all the objects from function
    tbl_name = tables_lst[0].table_name #retrieves unrecognized attribute to bypass str declaration
    db_data = retrieve_data(database=database, table_name=tbl_name) #retrieves last input data from tbl
    print("✅Data from oracle recieved")

    web_scraper = CoinMarketCapScraper(pages=1) #instantiates object, defines pages
    web_data = sanitize_data(web_scraper.scrape()) #scrapes data from web page
    print("✅Data Successfully Scraped")

    build_pdf(db_data=db_data, web_data=web_data)
    print("✅PDF successfully made and built")

    database.empty_data(tables_lst[0])
    print(f"✅{tables_lst[0].table_name} Successfully Wiped")

    for data in web_data:
        database.insert_rec(tables_lst[0], data)
    print("✅Oracle Successfully updated!")
     
    database.close_connection() #ends connected session with oracle database

if __name__ == "__main__":
    main()