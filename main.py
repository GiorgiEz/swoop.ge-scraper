from scraper import Collector, Scraper
from utils.file_operations import write_to_csv



if __name__ == "__main__":
    url = "https://swoop.ge/en"  # Website to scrape
    collector = Collector(url)  # Collector class to handle HTTP Requests
    category_soup_pairs = collector.get_categories()  # Creates soup objects for each product category

    path_to_csv = "data/products.csv"
    headers = [
        "product_name", "place_name", "price_after_sale", "price_before_sale",
        "sale_percentage", "sold_amount", "product_link", "product_image", "category"
    ]

    # Iterate over all the categories, scrape the data and save it in the csv file
    all_data = []
    for category_name, category_soup in category_soup_pairs.items():
        data = Scraper(category_name, category_soup).scraper()
        all_data.extend(data)

    write_to_csv(all_data, path_to_csv, headers)
