from zepto.order import scrape_zepto

query = "Coke diet"  # Replace with the actual search query
data = scrape_zepto(query)
print(data)