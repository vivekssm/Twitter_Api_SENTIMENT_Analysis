from bs4 import BeautifulSoup
import pandas as pd
import requests
html_text=requests.get('http://books.toscrape.com/catalogue/category/books/travel_2/index.html')
soup=BeautifulSoup(html_text.content,'html.parser')
table = soup.findAll('li', attrs = {'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
out=[]
for i in range(len(table)):
    book_details=[]
    temp=str(table[i].find('a')).split('"')[1][9:]
    product_page_url= 'http://books.toscrape.com/catalogue/'+temp
    html_text_hyperlink=requests.get(product_page_url)
    soup_hyperlink=BeautifulSoup(html_text_hyperlink.content,'html.parser')
    title=soup_hyperlink.find('div',attrs={'class':'col-sm-6 product_main'}).find('h1').text
    rating=soup_hyperlink.find('div',attrs={'class':'col-sm-6 product_main'}).findAll('p')[2]
    rating=str(rating).split('>')[0]
    review_rating=rating.split(' ')[2]
    table_in=soup_hyperlink.find('table',attrs={'class':'table table-striped'}).text
    table_content=table_in.split('\n')
    table_content = [i for i in table_content if i != '']
    universal_product_code=table_content[0][3:]
    price_including_tax=table_content[3].split(')')[1]
    price_excluding_tax=table_content[2].split(')')[1]
    number_available=table_content[6].split('(')[1].split(" ")[0]
    book_details.extend([product_page_url,title,universal_product_code,price_including_tax,price_excluding_tax,number_available,'Travel',review_rating])
    out.append(book_details)

df=pd.DataFrame(out, columns = ['product_page_url','title','universal_product_code','price_including_tax','price_excluding_tax','number_available','category','review_rating'])
df.to_csv("submission.csv",index=False)