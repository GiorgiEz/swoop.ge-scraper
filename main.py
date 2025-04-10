from scraper import Collector



if __name__ == "__main__":
    url = "https://swoop.ge/en"
    collector = Collector(url)
    categories = collector.get_categories()

    if categories:
        print("✅ All Categories fetched:")
