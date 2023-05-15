import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin

def collect_amsterdam(arg):
    pass

def collect_rivm(arg):
    pass


def collect_all(arg):
    pass



def collect_subpages(url_base, path):
    url_list = []

    response = requests.get(url_base)
    soup = BeautifulSoup(response.content, "html.parser") ########### check pdf ###############
    links = soup.find_all("a", href=lambda href: href)
    url_list.append((base_url, response.content))

    time.sleep(random.uniform(1, 3))


    for link in links:
        if str(path) in link["href"]:

            # Join the linked URL path with the base URL to create the full URL
            linked_url = urljoin(base_url, link["href"])

            # Send a GET request to the full URL
            linked_response = requests.get(linked_url)

            # Wait for a random amount of time to avoid overwhelming the server
            time.sleep(random.uniform(2, 8))

            # Create a BeautifulSoup object from the response content
            linked_soup = BeautifulSoup(linked_response.content, "html.parser")

            # Find all <a> tags with an href that contains the base URL
            linked_links = linked_soup.find_all("a", href=lambda href: href and base_url in href)

            # Append the linked URL and its HTML content to the list
            url_list.append((linked_url, linked_response.content))

            print(linked_url)

            # Loop through all the links found in the linked URL's HTML content
            for linked_link in linked_links:

                # Check if the nested URL path contains "/afval-gebruik"
                if "/afval-hergebruik" in linked_link["href"]:

                    # Join the nested URL path with the base URL to create the full URL
                    nested_url = urljoin(base_url, linked_link["href"])

                    # Send a GET request to the full URL
                    nested_response = requests.get(nested_url)

                    # Wait for a random amount of time to avoid overwhelming the server
                    time.sleep(random.uniform(2, 8))

                    # Append the nested URL and its HTML content to the list
                    url_list.append((nested_url, nested_response.content))

                    #print(nested_url)
    
    return (url_list) ####### add more content #######





######################## afval-en-hergebruik ###########################
import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin

url_list = []


base_url = "https://www.amsterdam.nl/afval-en-hergebruik"

# Send a GET request to the base URL
response = requests.get(base_url)

# Wait for a random amount of time to avoid overwhelming the server
time.sleep(random.uniform(2, 8))

# Create a BeautifulSoup object from the response content
soup = BeautifulSoup(response.content, "html.parser")

# Find all <a> tags with an href that contains the base URL
links = soup.find_all("a", href=lambda href: href)

# Append the base URL and its HTML content to the list
print(base_url)
url_list.append((base_url, response.content))

# Loop through all the links found in the base URL's HTML content
for link in links:

    # Check if the linked URL path contains "/afval-gebruik"
    if "/afval-hergebruik" in link["href"]:

        # Join the linked URL path with the base URL to create the full URL
        linked_url = urljoin(base_url, link["href"])

        # Send a GET request to the full URL
        linked_response = requests.get(linked_url)

        # Wait for a random amount of time to avoid overwhelming the server
        time.sleep(random.uniform(2, 8))

        # Create a BeautifulSoup object from the response content
        linked_soup = BeautifulSoup(linked_response.content, "html.parser")

        # Find all <a> tags with an href that contains the base URL
        linked_links = linked_soup.find_all("a", href=lambda href: href and base_url in href)

        # Append the linked URL and its HTML content to the list
        url_list.append((linked_url, linked_response.content))

        print(linked_url)

        # Loop through all the links found in the linked URL's HTML content
        for linked_link in linked_links:

            # Check if the nested URL path contains "/afval-gebruik"
            if "/afval-hergebruik" in linked_link["href"]:

                # Join the nested URL path with the base URL to create the full URL
                nested_url = urljoin(base_url, linked_link["href"])

                # Send a GET request to the full URL
                nested_response = requests.get(nested_url)

                # Wait for a random amount of time to avoid overwhelming the server
                time.sleep(random.uniform(2, 8))

                # Append the nested URL and its HTML content to the list
                url_list.append((nested_url, nested_response.content))

                print(nested_url)
