import csv
from re import search, template
from ssl import Options
from unittest import result
from webbrowser import get
from bs4 import BeautifulSoup

# Firefox and Chrome
from selenium import webdriver

#starting up the webdriver for  Chrome
driver = webdriver.Chrome()


# Provide URL of target web page 
url = 'https://www.amazon.in'

driver.get(url)

def get_url(search_term):
    """Generate an URL from search term"""
    template = 'https://www.amazon.in/s?k=()&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ','+')
    return template.format(search_term)

driver.get(url)


#Extraction of results
soup = BeautifulSoup(driver.page_source, 'html.parser')
results = soup.find_all('div',{'data-component-type':'s-search-result'})

len(results)


# record prototyping
item = results[0]
atag = item.h2.a
description = atag.text.strip()
url = 'https://www.amazon.in' + atag.get('href')
price_parent = item.find('span','a-price')
price = price_parent.find('span','a-offscreen').text
rating = item.i.text
review_count = item.find('span',{'class': 'a-size-base','dir':'auto'}).text

#Pattern Generalization
def extract_record(item):
    """Extract and retun data from single record """

    #Description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.in' + atag.get('href')

    price_parent = item.find('span', 'a-price')
    price = price_parent.find('span','a-offscreen').text

    # rank and rating
    rating = item.i.text
    review_count = item.find('span',{'class': 'a-size-base','dir':'auto'}).text

    result = {description, price, rating, review_count, url}

    return result

records = []
results = soup.find_all('div', {'data-component-type': 's-search-result'})

for item in results:
    record = extract_record(item)
    if record :
        records.append(record)


# Error Handling for ratings
def extract_record(item):
    """Extract and retun data from single record """

    #Description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.in' + atag.get('href')


    try:
        #price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span','a-offscreen').text

    except AttributeError:
        return

    try:
        # rank and rating
        rating = item.i.text
        review_count = item.find('span',{'class': 'a-size-base','dir':'auto'}).text
    except AttributeError:
        rating = ''
        review_count = ''

    result = {description, price, rating, review_count, url}

    return result

for row in records:
    print(row[1])

#Scroll through 20 pages
def get_url(search_term):
    """Generate an URL from search term"""
    template = 'https://www.amazon.in/s?k=()&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ','+')

    #addterm query
    url = template.format(search_term)

    # add page query
    url += '&page{}'
    return url

# Main Function
def main(search_term):
    #starup the webdriver
    options.use_chromium = True


    record = []
    url = get_url(search_term)


    for page in range(1,21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
    
    driver.close()

    # save date to csv
    with open('results.csv','w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating','ReviewCount','Url'])
        writer.writerows(records)

# Enter Search Term main('')
