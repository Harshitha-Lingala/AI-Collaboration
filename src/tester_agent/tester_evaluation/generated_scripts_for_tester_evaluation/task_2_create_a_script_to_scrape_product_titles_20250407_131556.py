import requests
from bs4 import BeautifulSoup

# Bug 1: Using a hardcoded URL for demonstration purposes
url = 'https://www.example-ecommerce-site.com'

# Poor practice: Not handling potential exceptions that may occur during the request
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Bug 2: Selecting the wrong CSS selector to extract product titles
product_titles = soup.select('.product-name')

for title in product_titles:
    print(title.text.strip())