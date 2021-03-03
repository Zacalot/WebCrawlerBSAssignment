# Scrapes various product information and saves it to a CSV
from bs4 import BeautifulSoup
from unidecode import unidecode
import requests
import csv

def non_ascii_to_space(text):
    return ''.join([i if ord(i) < 128 else " " for i in text])

productsURL = "https://www.tomford.com/beauty/lips/"

print("Downloading products page...")
productsHTML = requests.get(productsURL).text #HTML page of products
soup = BeautifulSoup(productsHTML,'html.parser')

productEntriesParent = soup.find("ul",{"id":"search-result-items"}) #Get parent of product entries
productEntries = productEntriesParent.findAll("li",recursive=False) #Get child product entries of parent
products = []
for i,product in enumerate(productEntries):
	productURL = (product.find("div").find("a")["href"]) #URL of product page
	print("Downloading page %s/%s for %s..." % (i+1,len(productEntries),product["id"]))
	productHTML = requests.get(productURL).text
	productSoup = BeautifulSoup(productHTML,'html.parser')
	products.append([
		product["id"], # ID
		productSoup.find("h1",{"class":"product-name vis-desktop-pdp"}).get_text(), # Name
		"https:"+product.find("img",{"class":"js-tile-image tile-image"})["src"], # Image URL
		non_ascii_to_space(productSoup.find("div",{"itemprop":"description"}).get_text().strip()), # Description (ascii only)
		productSoup.find("span",{"itemprop":"priceCurrency"}).get_text()+productSoup.find("span",{"itemprop":"price"}).get_text() # Currency & Price
	])

print("Writing CSV...")
with open('products.csv',mode='w') as productsCSV: #Write data to CSV
	productsCSV = csv.writer(productsCSV,delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL)
	productsCSV.writerow(["ID","Name","Image URL","Description","Price"])
	for product in products:
		productsCSV.writerow(product)

print("Done!")
