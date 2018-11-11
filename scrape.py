#import dependancies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from urllib.parse import urlparse
import requests

#Start browser
def start_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\\Users\\SWATI KHARKAR\\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

# Find out hostname from url
def parse_url(url):
    parsed_uri = urlparse(url)
    result = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    #print(result)
    return result

# Get the latest news
def latest_mars_news():
    scrape_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser = start_browser();
    
    browser.visit(scrape_url)
    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "lxml")
    
    all_news_details = soup.find_all('li', class_="slide")
    #pick the top news
    top_news = all_news_details[0]
    #collect the elements
    external_div = top_news.find_all('div', class_="list_text")
    news_list = []
    for div in external_div:
        title = div.find('a').get_text()
        text = div.find('div', class_="article_teaser_body").get_text()
        data = {'title' : title, 'text' : text}
        news_list.append(data)
    #print(news_list)    
    # close browser
    browser.quit()
    
    #return results
    return news_list

# Get url for featured Image
def jpl_featured_image():
	scrape_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser = start_browser();

	browser.visit(scrape_url)
	time.sleep(1)

	#Scrape page into Soup
	page = browser.html
	soup = bs(page, "lxml")

	featured_image = soup.find('div', class_="carousel_container")
	#collect the elements
	article = featured_image.find('article', class_="carousel_item")
	#print(article.get('style').split('background-image:'))
	val = article.get('style').split("('", 1)[1].split("')")[0]
	#print(val)
	uri = parse_url(scrape_url);
	img_url = uri + val

	# close browser
	browser.quit()

	#return results
	return {"img_url" : img_url}

# Get Mars facts in panda table
def mars_facts():
	url = "https://space-facts.com/mars/"
	table = pd.read_html(url)
	#print(table)
	#prepare data
	df = table[0]
	df.columns = ["Key", "Value"]
	df.set_index('Key', inplace=True)
	fact_data = []
	for row in df.iterrows():
		tu = {"key" : row[0], "value" : row[1].Value}
		fact_data.append(tu)
	print(fact_data)
	return fact_data

# Get latest weather from Mars Twitter Handle
def mars_weather():
	url = "https://twitter.com/marswxreport?lang=en"
	browser = start_browser()

	browser.visit(url)
	time.sleep(1)
	html = browser.html
	soup = bs(html, "lxml")
	tweets = soup.find_all('div', class_="js-tweet-text-container")
	#get latest temp
	latest_temp = tweets[0]
	print (latest_temp.find('p').get_text())
	weather = latest_temp.find('p').get_text()

	# close browser
	browser.quit()
	return weather
    
# Get Mars Hemisphere Images by first getting list of pages to get the full image.
def mars_hemisphere_images():
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser = start_browser()
    
    browser.visit(url)
    time.sleep(1)
    
    html = browser.html
    soup = bs(html, "lxml")
    
    all_image_elements = soup.find_all('div', class_='item')
    
    #print(all_image_elements)
    complete_list = []
    for data in all_image_elements:
        title = data.find('h3').get_text()
        link = data.find('a', class_="product-item").get('href')
        #print(f"Title - {title} Detail Link - {link}")
        uri = parse_url(url);
        detail_url = uri + link
        print(detail_url)
        # Retrieve page with the requests module
        response = requests.get(detail_url)
        # Create BeautifulSoup object; parse with 'lxml'
        img_soup = bs(response.text, 'lxml')
        outer = img_soup.find_all('li')
        #print(outer)
        
        for li in outer:
            if (li.find('a').get('target') is not None):
                img = li.find('a').get('href')
                print(img)
                data = {"title" : title, "img_url" : img}
                complete_list.append(data)
                break;

    browser.quit()
    return complete_list

def scrape_data():
	# get latest mars news
	latest_news = latest_mars_news()

	# featured Image
	featured_image = jpl_featured_image()

	# latest weater
	current_weather = mars_weather()

	# mars facts
	fact_table = mars_facts()

	#hemisphere images
	images = mars_hemisphere_images()

	mars_scrape = {
		"planet" : "mars",
		"latest_news" : latest_news,
		"featured_image" : featured_image,
		"weather" : current_weather,
		"facts" : fact_table,
		"images" : images
	}

	print(mars_scrape)
	return mars_scrape