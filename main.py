from scraper import Collector, Scraper
from utils.file_operations import write_to_csv
from data_cleaning import DataCleaning



if __name__ == "__main__":
    url = "https://swoop.ge/en"  # Website to scrape

    """ Step 1: Handle HTTP Requests """
    collector = Collector(url)
    category_soup_pairs = collector.get_categories()  # Creates soup objects for each product category

    """ Step 2: Define headers, scrape the data and save it in a csv file """
    path_to_csv = "data/products.csv"
    headers = [
        "product_name", "place_name", "price_after_sale", "price_before_sale",
        "sale_percentage", "sold_amount", "product_link", "product_image", "category"
    ]

    all_data = []
    scraper = Scraper(all_data)
    for category_name, category_soup in category_soup_pairs.items():
        scraper.scraper(category_name, category_soup)

    write_to_csv(all_data, path_to_csv, headers)

    """ Step 3: Perform data cleaning and save the cleaned data in a separate csv file """
    path_to_cleaned_csv = "data/cleaned_products.csv"
    data_cleaning = DataCleaning()

    data_cleaning.get_shape()
    data_cleaning.get_info()
    data_cleaning.get_description()
    data_cleaning.get_null_columns()

    data_cleaning.fill_product_place_name_nulls()
    data_cleaning.fill_price_nulls()

    data_cleaning.adjust_sale_percentage()
    data_cleaning.adjust_amount_sold()

    data_cleaning.df_to_csv(path_to_cleaned_csv, headers)
