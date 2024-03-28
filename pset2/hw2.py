import psycopg2
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Establish database connection
con = psycopg2.connect(host="127.0.0.1",
                       port="5432",
                       user="alizameller",
                       password="",
                       database="hw2")

# Get a database cursor
cur = con.cursor()

# if running for the first time
cur.execute("CREATE TABLE half_time(id INT PRIMARY KEY, name VARCHAR, abv FLOAT NULL, color_rating INT, hop_rating INT NULL, brewery VARCHAR, state VARCHAR, style VARCHAR, food_pairing VARCHAR NULL);")

# otherwise, truncate table before inserting newer information
#cur.execute("TRUNCATE half_time;")

# Iterate over all pages in the "craft beers" tab on https://halftimebeverage.com
page = 1
beers = []
links = []
while page != 16:
      url = f"https://halftimebeverage.com/new-arrivals-new-craft-beer?p={page}&product_list_limit=80"
      response = requests.get(url)
      html = response.content
      soup = BeautifulSoup(html, 'html.parser')
      for beer in soup.findAll('a', class_='product-item-link'):
            beers.append(beer.get_text(strip=True))
            links.append(beer['href'])
      page = page + 1

# Iterate over each link in links which are the product info pages for each beer
i = 1
for (beer, link) in (zip(beers, tqdm(links))):
    # print(str(i) + "\t" + beer)
    content = {"id":None, "name":None, "ABV":None, "Color Rating":None, "Hop Rating":None, "Brewery":None, "State":None, "Style":None, "Food Pairing":None}
    content["name"] = beer
    content["id"] = i

    response = requests.get(link)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    additional_attributes = soup.findAll(class_='product-attribute-value')
    for attr in additional_attributes:
        if attr["data-th"] == "Color Rating":
            img = attr.find('img', alt=True)
            content[attr["data-th"]] = (img['alt']).replace("Color Rating ", "")
            print(content[attr["data-th"]])
        elif attr["data-th"] == "Hop Rating":
            img = attr.find('img', alt=True)
            content[attr["data-th"]] = (img['alt']).replace("Hop Rating of ", "")
            print(content[attr["data-th"]])
        else: 
            content[attr["data-th"]] = (attr.get_text(strip=True))
    # weird inconsistency on the website, color rating for these is 'Cider' which is an invalid input to database -- manually override
    if content["Color Rating"] == 'Cider':
        content["Color Rating"] = None

    print(content)

    cur.execute("""
        INSERT INTO half_time (id, name, abv, color_rating, hop_rating, brewery, state, style, food_pairing)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, 
        (content["id"], content["name"], (content["ABV"]), (content["Color Rating"]), (content["Hop Rating"]), content["Brewery"], content["State"], content["Style"], content["Food Pairing"])
        )
    
    i = i + 1

# Commit the data
con.commit()

# Close our database connections
cur.close()
con.close()