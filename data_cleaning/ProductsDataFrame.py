import pandas as pd



class ProductsDataFrame:
    """Singleton class to manage a single DataFrame of all products """

    _instance = None

    def __new__(cls, products_csv="data/products.csv"):
        """Ensures only one instance is created."""
        if cls._instance is None:
            cls._instance = super(ProductsDataFrame, cls).__new__(cls)
            cls._instance.init_data(products_csv)
        return cls._instance

    def init_data(self, products_csv):
        """Loads data from CSV files and merges them into a single DataFrame."""
        self.products_df = pd.read_csv(products_csv)
        print(f"✅ DataFrame loaded with {len(self.products_df)} records.")

    def get_df(self):
        """Returns the DataFrame instance."""
        return self.products_df
