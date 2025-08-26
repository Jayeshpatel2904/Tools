import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = "https://chatgpt.com/c/67c20cc6-5630-8000-b5e7-d7febc54f3e4"

# Send an HTTP GET request
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract all text
    text = soup.get_text(separator="\n", strip=True)
    
    # Print or save the scraped text
    print(text)
else:
    print("Failed to retrieve the webpage")
