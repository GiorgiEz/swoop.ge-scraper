class Scraper:
    def __init__(self, category_name, category_soup):
        self.category_name = category_name
        self.category_soup = category_soup

    def scraper(self):
        # Finds the title of the category and then searches for a div with a class grid corresponding to the products
        product_container = (self.category_soup.find("h2")
                             .find_next_sibling("div", class_="grid"))
        all_data = []

        if product_container:
            products = product_container.find_all("div", class_="relative", recursive=False)

            for product in products:
                try:
                    product_page = product.find("a")
                    product_link = f"https://swoop.ge{product_page['href']}" if product_page and product_page.get(
                        "href") else None

                    product_image_tag = product_page.find("img") if product_page else None
                    product_image = product_image_tag.get("src") if product_image_tag else None

                    # Get the outer divs (image, and name/price block)
                    outer_divs = product_page.find_all("div", recursive=False) if product_page else []

                    # Get the name/price section
                    name_and_price_div = outer_divs[1].find_all("div", recursive=False) if len(outer_divs) > 1 else []

                    # Name and place
                    name_div = name_and_price_div[0] if len(name_and_price_div) > 0 else None
                    product_name = name_div.find("h4").text.strip() if name_div and name_div.find("h4") else None
                    place_name = name_div.find("div").text.strip() if name_div and name_div.find("div") else None

                    # Prices
                    price_div = name_and_price_div[1] if len(name_and_price_div) > 1 else None
                    price_h4s = price_div.find_all("h4") if price_div else []
                    price_after_sale = price_h4s[0].text.strip() if len(price_h4s) > 0 else None
                    price_before_sale = price_h4s[1].text.strip() if len(price_h4s) > 1 else None

                    # Discount
                    sale_percentage_tag = price_div.find("p") if price_div else None
                    sale_percentage = sale_percentage_tag.text.strip() if sale_percentage_tag else None

                    # Sold count
                    sold_div = name_and_price_div[2] if len(name_and_price_div) > 2 else None
                    sold_amount = sold_div.text.strip() if sold_div else None

                    all_data.append([
                        product_name, place_name, price_after_sale, price_before_sale,
                        sale_percentage, sold_amount, product_link, product_image, self.category_name
                    ])
                except Exception as e:
                    print(f"⚠️ Error extracting one product: {e}")
        else:
            print("❌ Product container not found.")

        return all_data
