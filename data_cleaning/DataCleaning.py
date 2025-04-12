from data_cleaning.ProductsDataFrame import ProductsDataFrame



class DataCleaning:
    def __init__(self):
        self.products_df = ProductsDataFrame().get_df()

    def get_shape(self):
        """ Prints the shape of the dataset. Useful for quickly understanding the size of the dataset. """
        print("SHAPE OF THE PRODUCTS DATASET: ", self.products_df.shape)

    def get_info(self):
        """ Prints detailed information about the dataset. Helpful for understanding the dataset structure. """
        print("THE GAMES DATASET INFORMATION: ", self.products_df.info(), '\n')

    def get_description(self):
        """ Prints a statistical summary of the dataset. Useful for a quick overview of data distribution. """
        print("DESCRIPTION OF THE GAMES DATASET:\n", self.products_df.describe(), '\n')

    def get_null_columns(self):
        """ Prints the count of missing (null) values for each column in the dataset. """
        print("AMOUNT OF NULL VALUES IN GAMES DATASET:", self.products_df.isnull().sum(), '\n')

    def fill_nulls(self, column_name, fill_value_func):
        """
        Fills missing values in the specified column using a provided fill function.

        Parameters:
        ----------
        column_name : The name of the column to fill missing values for.
        fill_value_func : A function that specifies how to fill the missing values for the column.
        """
        try:
            if column_name in self.products_df.columns:
                self.products_df[column_name] = fill_value_func(self.products_df)
                print(f"Null values in '{column_name}' column have been filled. "
                      f"Null values left: {self.products_df[column_name].isnull().sum()}")
            else:
                print(f"Column '{column_name}' does not exist.")
        except Exception as e:
            print(f"Error occurred while filling null values in '{column_name}': {e}")

    def fill_product_place_name_nulls(self):
        """ Fills the missing values in the 'matchday' column with 'Unknown Matchday'. """
        self.fill_nulls('product_name', lambda df: df['product_name'].fillna("N/A"))
        self.fill_nulls('place_name', lambda df: df['place_name'].fillna("N/A"))

    def fill_price_nulls(self):
        """ Replaces Null values in price_before_sale and price_after_sale columns by N/A """
        self.fill_nulls('price_before_sale', lambda df: df['price_before_sale'].fillna("N/A"))
        self.fill_nulls('price_after_sale', lambda df: df['price_after_sale'].fillna("N/A"))

    def adjust_sale_percentage(self):
        """ Removes % and - symbols from sale_percentage column """
        self.products_df["sale_percentage"] = (self.products_df["sale_percentage"].
                                               str.replace("%", "").str.replace("-", ""))

    def adjust_amount_sold(self):
        """ Removes 'Sold' string and leading and trailing whitespaces from sold_amount column """
        self.products_df["sold_amount"] = self.products_df["sold_amount"].str.replace("Sold", "").str.strip()

    def df_to_csv(self, path, headers):
        """ Writes data from dataframe to a csv file """
        self.products_df.to_csv(path, columns=headers)
