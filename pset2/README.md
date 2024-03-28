## Files
#### hw2.py 
- This file is the web-scraping script. It scrapes all products from the **craft beer** tab on [half time beverage's site](https://halftimebeverage.com/new-arrivals-new-craft-beer) and inserts the relevant information into the desired database. 
#### half_time.sql
- I used the "export data" feature in DBeaver to export the data in a .sql file. This is essentially a snapshot of what the data looked like at the time that I was writing the queries so that you can use that data to compare against the queries in queries.py.  
#### queries.py
- This file is the code for making queries to the database. It uses an ORM to represent the schema and performs a few tests against some SQL statements to check that it works properly. It also displays the output in STDOUT. 
#### output.txt
- This file contains the output from the queries I did in queries.py so that you can re-run the script and compare the results.

## Flow of Scraping the Site
  - Starting at the first page of the **craft beer** tab, the script requests the html from each of the 16 pages and extracts the product links and names of each beer on each page.  
  - After collecting all the links and names, the script requests the html from each product link (i.e. it requests each beer's product info page) and collects the "additional information" listed on the bottom of the product page for each beer.
  - This information is then inserted into the database, after which the connection is then closed.

Example:
- Starting URL is: https://halftimebeverage.com/new-arrivals-new-craft-beer?p=1&product_list_limit=80
  - Note that in the script the url is in a for loop to iterate over each page
- Using BeautifulSoup, iterate over all the beers on the page and grab the links for each one which are part of the class called 'product-item-link' and listed as hyperlink (\<a\>) items 
- Request next page URL (https://halftimebeverage.com/new-arrivals-new-craft-beer?p=2&product_list_limit=80) and repeat the above step
- After all beer names and hyperlinks are extracted, make a request to each hyperlink (ex: https://halftimebeverage.com/second-fiddle-67819) and extract relevant information from the information listed in the class 'product-attribute-value' 
- Insert information into database

## Data Storage
- This is the CREATE TABLE statement:
```
  CREATE TABLE half_time(
      id INT PRIMARY KEY, 
      name VARCHAR, 
      abv FLOAT NULL, 
      color_rating INT, 
      hop_rating INT NULL, 
      brewery VARCHAR, 
      state VARCHAR, 
      style VARCHAR, 
      food_pairing VARCHAR NULL);
```
- All the data is stored in one table. The primary key is the 'id' which is manually provided by the scraping code which I used for debugging the scraping code and came in handy to use as the primary key -- in the event that two beers had the same name (Which is why I chose not to use the name as the primary key). Some values are optionally NULL because some beers did not have that information on their pages. 
- The data is queried as a typical SQL table's data would be queried. Example: 
```
SELECT * FROM half_time;
```
## Results
See output.txt for interesting results.
I think the most useful and fun queries for beginner beer drinkers are the queries that select beers that contain a certain food item in the "food pairing" suggestions. As an example, a user can query all beers that pair well with salmon. 