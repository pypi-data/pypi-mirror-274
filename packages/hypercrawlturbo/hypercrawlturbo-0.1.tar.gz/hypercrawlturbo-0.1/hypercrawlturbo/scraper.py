import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_urls(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all anchor tags <a> which contain href attribute
        links = soup.find_all('a', href=True)
        
        # Extract and print the URLs
        total_urls = 0
        for link in links:
            href = link['href']
            # Join the relative URL with the base URL
            absolute_url = urljoin(url, href)
            print(absolute_url)
            total_urls += 1
        
        print(f"Total URLs scraped: {total_urls}")
    else:
        print("Failed to fetch the page")
