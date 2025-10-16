# document_downloader.py
import os
import time
import requests
from urllib.parse import urljoin, urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

def initialize_driver():
    """Initializes and returns a Selenium WebDriver instance."""
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return None

def download_documents_from_url(driver, url, output_folder="results/documents"):
    """
    Navigates to a given URL and downloads any .pdf, .xls, or .rar files.
    
    Args:
        driver: A Selenium WebDriver instance.
        url: The URL to scrape for documents.
        output_folder: The directory where downloaded files will be saved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    try:
        print(f"Navigating to URL: {url}")
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        # Find all links on the page that end with our target extensions
        document_links = driver.find_elements(
            By.XPATH, 
            "//a[contains(@href, '.pdf') or contains(@href, '.xls') or contains(@href, '.rar')]"
        )
        
        if not document_links:
            print("No documents with .pdf, .xls, or .rar extensions found on this page.")
            return
            
        print(f"Found {len(document_links)} potential document links. Starting download...")
        
        for link in document_links:
            href = link.get_attribute('href')
            if href:
                full_url = urljoin(url, href)
                filename = os.path.basename(urlparse(full_url).path)
                file_path = os.path.join(output_folder, filename)
                
                try:
                    # Use the requests library to download the file content
                    print(f"  -> Downloading '{filename}'...")
                    response = requests.get(full_url, stream=True)
                    response.raise_for_status()
                    
                    with open(file_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"  -> Downloaded '{filename}' to {file_path}")
                except Exception as e:
                    print(f"  (!) Failed to download {full_url}: {e}")
    except Exception as e:
        print(f"(!) An error occurred while processing the URL: {e}")

    finally:
        # It's good practice to keep the driver open for multiple downloads
        # but for a simple script, quitting it at the end is fine.
        pass

def main():
    """Main function to run the downloader."""
    # List of URLs to process. Replace these with your actual URLs.
    # The script will work with both tender listing pages and detail pages.
    urls_to_process = [
        "https://etenders.gov.in/eprocure/app/app.html",
        # Add other URLs here as needed
        # "https://www.iocletenders.nic.in/nicgep/app"
    ]
    
    driver = initialize_driver()
    if not driver:
        return
        
    for target_url in urls_to_process:
        download_documents_from_url(driver, target_url)

    driver.quit()
    print("\nAll downloads complete.")

if __name__ == "__main__":
    main()