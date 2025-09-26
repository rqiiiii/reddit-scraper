import requests
import time
import json

def scrape_reddit(subreddit, pages, limit):
    """
    Steps:
    1. Base URL for the subreddit
    2. Fetches multiple "pages" of posts using the `after` cursor for pagination
    3. Filters posts to only include those with image URLs(.jpg, .png, .jpeg)
    4. Collects results (post_title + image_url) in a list.
    5. Saves the results and convert into a JSON file (`scraper_output.json`).
    """

    base_url = f"https://www.reddit.com/r/{subreddit}/.json"
    headers = {"User-Agent": "Mozilla/5.0 (reddit scraper)"}

    results = []
    after = None  

    
    for page in range(pages):
        url = f"{base_url}?limit={limit}"
        if after:
            url += f"&after={after}"
        print("page", page+1, ":", url)

        response = requests.get(url, headers=headers)
        data = response.json()
        posts = data["data"]["children"]

        for post in posts:
            post_data = post["data"]
            post_title = post_data.get("title")
            post_url = post_data.get("url")

            if post_url and post_url.lower().endswith((".jpg", ".png", ".jpeg")):
                results.append({"post_title": post_title, "image_url": post_url})

        after = data["data"].get("after")  

        if not after:
            print("[INFO] No more pages available.")
            break


    return results

#Get 2 post per page for 10 pages
get_posts = scrape_reddit(subreddit = "malaysia", pages = 10, limit = 5)
with open("scraper_output.json", "w", encoding="utf-8") as f:
        json.dump(get_posts, f, ensure_ascii=False, indent=4)