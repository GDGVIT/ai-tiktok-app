# Function to get images from external api and store them in server/server/taketext/pics

import requests
import os
# https://www.slingacademy.com/article/sample-photos-free-fake-rest-api-for-practice/


async def search_images(api_key, keywords, per_page=1):
    """
    Search for images based on keywords using the Pexels API.

    Parameters:
    - api_key (str): Pexels API key for authorization.
    - keywords (list): List of keywords for image search.
    - per_page (int): Number of images per page.

    Returns:
    - list: List of image URLs.
    """
    url = "https://api.pexels.com/v1/search"
    headers = {
        "Authorization": api_key,
    }

    image_urls = []

    for keyword in keywords:
        params = {
            "query": keyword,
            "per_page": per_page,
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            photos = data.get("photos", [])

            if not photos:
                print(f"No photos found for keyword: {keyword}")
            else:
                # Get the first photo's original image URL for each keyword
                image_urls.append(photos[0]["src"]["original"])

        else:
            print(f"Error for keyword {keyword}: {response.status_code}")

    return image_urls


async def download_images(url_list, out_dir):
    """
    Download images from a list of URLs and save them to the specified directory.

    Parameters:
    - url_list (list): List of image URLs to download.
    - out_dir (str): Output directory to save the downloaded images.

    Returns:
    - None
    """
    # Create the output directory if it doesn't exist
    os.makedirs(out_dir, exist_ok=True)

    for url in url_list:
        response = requests.get(url)

        if response.status_code == 200:
            # Get the file name from the URL
            filename = os.path.join(out_dir, os.path.basename(url))

            # Save the image to the specified output directory
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Image downloaded: {filename}")
        else:
            print(
                f"Failed to download image from {url}. Status code: {response.status_code}"
            )
