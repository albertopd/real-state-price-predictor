from pathlib import Path
import requests
import os
import random
from xml.etree import ElementTree as ET
from fake_headers import Headers

class ImmovlanSitemapScraper:
    """
    A class to scrape and parse property sitemaps from immovlan.be.

    This class downloads the main sitemap, finds all French property sitemaps
    for detailed listings, and then parses them to extract links for apartments
    and houses. The extracted URLs are then converted to their English versions
    and saved to separate text files.
    """

    def __init__(self, sitemaps_dir_path: Path):
        """Initializes the scraper with file paths and URLs."""
        self.base_url = "https://immovlan.be"
        self.sitemap_index_url = f"{self.base_url}/sitemap.xml"
        self.sitemap_xmlns = "http://www.sitemaps.org/schemas/sitemap/0.9"
        self.sitemaps_dir_path = sitemaps_dir_path
        self.main_sitemap_path = self.sitemaps_dir_path / "sitemap.xml"
        self.apartments_output_file = self.sitemaps_dir_path / "apartments_links.txt"
        self.houses_output_file = self.sitemaps_dir_path / "houses_links.txt"

    def _get_headers(self) -> dict:
        """
        Generate randomized, realistic HTTP headers to reduce request blocking.
        
        The function selects random combinations of browser and OS
        to generate diverse and legitimate-looking headers.
        """
        browsers = ["chrome", "firefox", "opera", "safari", "edge"]
        os_choices = ["win", "mac", "linux"]

        headers = Headers(
            browser=random.choice(browsers),
            os=random.choice(os_choices),
            headers=True
        )
        return headers.generate()

    def _download_file(self, url: str, file_path: Path) -> bool:
        """
        A helper method to download a file from a given URL and save it.

        Args:
            url (str): The URL of the file to download.
            file_path (str): The local path to save the file.
        """
        try:
            print(f"Downloading {url}...")

            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status() 

            with open(file_path, 'wb') as f:
                f.write(response.content)

            print(f"Successfully downloaded to {file_path}")
            return True
        
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
            return False

    def download_main_sitemap(self):
        """
        Downloads the main sitemap and saves it to the specified directory.
        """
        return self._download_file(self.sitemap_index_url, self.main_sitemap_path)

    def _get_property_sitemaps(self):
        """
        Parses the main sitemap to find all French property detail sitemaps.

        Returns:
            list: A list of URLs for the French property detail sitemaps.
        """
        if not os.path.exists(self.main_sitemap_path):
            print("Main sitemap not found. Please run download_main_sitemap() first.")
            return []

        sitemap_urls = []
        try:
            tree = ET.parse(self.main_sitemap_path)
            root = tree.getroot()
            ns = f"{{{self.sitemap_xmlns}}}"
            for sitemap in root.findall(f"{ns}sitemap"):
                loc_elem = sitemap.find(f"{ns}loc")
                if loc_elem is not None:
                    loc = loc_elem.text
                    if loc and "fr_property-detail" in loc:
                        sitemap_urls.append(loc)
        except ET.ParseError as e:
            print(f"Error parsing main sitemap XML: {e}")
            return []
        
        return sitemap_urls

    def parse_property_sitemaps(self, sitemap_urls: list):
        """
        Parses a list of property sitemaps to find apartment and house links.

        Args:
            sitemap_urls (list): A list of URLs to property sitemaps.
        """
        apartments = []
        houses = []
        total_properties = 0
        total_properties_rent = 0
        total_properties_sale = 0

        ns = f"{{{self.sitemap_xmlns}}}"

        for url in sitemap_urls:
            temp_sitemap_path = self.sitemaps_dir_path / os.path.basename(url)
            if not self._download_file(url, temp_sitemap_path):
                continue
            
            try:
                tree = ET.parse(temp_sitemap_path)
                root = tree.getroot()
                
                # Check for a single URL entry for verification
                url_elements = root.findall(f"{ns}url")
                if not url_elements:
                    print(f"No URLs found in {url}. Skipping.")
                    continue

                for url_element in url_elements:
                    loc_elem = url_element.find(f"{ns}loc")

                    if loc_elem is not None and loc_elem.text:
                        total_properties += 1
                        loc = loc_elem.text

                        if "/a-vendre/" in loc:
                            total_properties_sale += 1
                            if any(x in loc for x in ("/appartement/", "/studio/", "/duplex/", "/rez-de-chaussee/")):
                                apartments.append(loc.replace("/fr/", "/en/"))
                            elif any(x in loc for x in ("/maison/", "/villa/", "/bungalow/")):
                                houses.append(loc.replace("/fr/", "/en/"))
                        elif any(x in loc for x in ("/a-louer/", "/en-colocation/")):
                            total_properties_rent += 1
                        else:
                            print(f"Unknown listing type in URL: {loc}")

            except ET.ParseError as e:
                print(f"Error parsing {url}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred while processing {url}: {e}")

        # Store the lists as class attributes to be accessed later
        self.apartments = apartments
        self.houses = houses
        print(f"Total properties processed: {total_properties} - Total for sale: {total_properties_sale} - Total for rent: {total_properties_rent}")
        print(f"Found {len(self.apartments)} apartments and {len(self.houses)} houses.")

    def write_output_files(self):
        """
        Writes the collected links for apartments and houses to their respective files.
        """
        if not hasattr(self, 'apartments') or not hasattr(self, 'houses'):
            print("No links found. Please run parse_property_sitemaps() first.")
            return

        with open(self.apartments_output_file, 'w') as f:
            for link in self.apartments:
                f.write(f"{link}\n")
        print(f"Apartment links saved to {self.apartments_output_file}")

        with open(self.houses_output_file, 'w') as f:
            for link in self.houses:
                f.write(f"{link}\n")
        print(f"House links saved to {self.houses_output_file}")
    
    def scrape_sitemaps(self):
        """Orchestrates the entire scraping and parsing process."""
        print("Starting ImmoVlan sitemap scraping process.")
        
        # Step 1: Download the main sitemap
        if self.download_main_sitemap():
            
            # Step 2: Get the list of property sitemaps
            property_sitemaps = self._get_property_sitemaps()
            if property_sitemaps:
                print(f"Found {len(property_sitemaps)} French property sitemaps to process.")
                
                # Step 3: Parse the property sitemaps and collect links
                self.parse_property_sitemaps(property_sitemaps)
                
                # Step 4: Write the collected links to output files
                self.write_output_files()
            else:
                print("No French property sitemaps found. Exiting.")
        else:
            print("Failed to download the main sitemap. Exiting.")

if __name__ == "__main__":
    # Create an instance of the scraper and run the process
    scraper = ImmovlanSitemapScraper(Path("data/raw/sitemaps"))
    scraper.scrape_sitemaps()
