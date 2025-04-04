# Coin Market Cap Report Builder

This project automates the process of retrieving cryptocurrency data from CoinMarketCap, storing it in an Oracle database, and generating a PDF report with visualizations. It leverages functionalities from three of my other repositories:

- **[Oracle Python CRUD](https://github.com/Ace-7854/oracle_python_CRUD)** – Handles database connections and automates CRUD operations.
- **[CoinMarketCap WebScraper](https://github.com/Ace-7854/CoinMarketCap-WebScraper)** – Extracts cryptocurrency data from CoinMarketCap.
- **[Report Builder Template](https://github.com/Ace-7854/Report_Builder_temp)** – Uses FPDF and Matplotlib to generate detailed PDF reports.

## Features

- **Scrapes latest cryptocurrency data** from CoinMarketCap.
- **Stores the data** in an Oracle database.
- **Generates PDF reports** with charts and formatted data tables.
- **Modularized structure** for easy customization and expansion.

## Installation & Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Ace-7854/Coin_market_cap_report_builder.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd Coin_market_cap_report_builder
   ```

3. **Install Required Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Oracle Database Connection**:

   Modify `oracle_module.py` with your database credentials:

   ```python
   import cx_Oracle
   
   connection = cx_Oracle.connect("username", "password", "host:port/service_name")
   cursor = connection.cursor()
   ```

## Usage

### 1. Scrape Cryptocurrency Data

```python
from web_scraper import scrape_coinmarketcap

data = scrape_coinmarketcap()
print(data)  # Displays extracted cryptocurrency data
```

### 2. Store Data in Oracle Database

```python
from oracle_module import insert_data

crypto_data = [("Bitcoin", "BTC", 70000, 450000000)]  # Example data
insert_data(crypto_data)
```

### 3. Generate PDF Report

```python
from pdf_builder_mod import create_pdf_report

create_pdf_report("crypto_report.pdf")
```

## Project Structure

- `main.py` – Orchestrates the entire workflow.
- `web_scraper.py` – Handles CoinMarketCap data extraction.
- `oracle_module.py` – Manages database interactions.
- `figure_builder_mod.py` – Creates visual data representations.
- `pdf_builder_mod.py` – Generates formatted PDF reports.

## Example Output

After running `main.py`, the output PDF will contain:
- A table of cryptocurrency prices and market data.
- Graphs of historical trends using Matplotlib.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

## License

This project is licensed under the MIT License.

