import pandas as pd
import requests
from bs4 import BeautifulSoup

# Function to scrape and clean the text from a company's homepage
def scrape_and_clean_homepage(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove unwanted elements such as headers, footers, and advertisements
        unwanted_tags = ['header', 'footer', 'aside', 'nav', 'script']  # Add any other tags you want to remove
        for tag in unwanted_tags:
            for element in soup.find_all(tag):
                element.decompose()

        # Extract and clean the text content from the main content area
        cleaned_text = soup.get_text(separator='\n')  # Preserve line breaks for readability
        cleaned_text = ' '.join(cleaned_text.split())  # Remove extra whitespace

        return cleaned_text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Read the CSV file
df = pd.read_csv('intern.csv')

# Iterate over each row of the DataFrame
for index, row in df.iterrows():
    company_name = row['Company Name']
    company_url = row['companywebsite']

    # Scrape and clean the text from the company's homepage
    cleaned_text = scrape_and_clean_homepage(company_url)

    # Store the cleaned text in the third column of the DataFrame
    df.at[index, 'Scraped and formated homepage data'] = cleaned_text

# Save the updated DataFrame to a new CSV file
df.to_csv('intern_cleaned.csv', index=False)
