from apify_client import ApifyClient
import requests
from readability import Document
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv
import os

load_dotenv("keys.env")

apify_key = os.getenv("APIFY_API_KEY")

client = ApifyClient(apify_key)


def extract_website_data(job_posting_url: str) -> str:

    run = client.actor("aYG0l9s7dbB7j3gbS").call(
    run_input={
            "startUrls": [{"url": job_posting_url}],
                "maxCrawlDepth": 0,
        "maxCrawlPages": 1,
            "maxResults": 1,
            "htmlTransformer": "readableText"
            "memory_mbytes"=2048
    }
    )

    if isinstance(run, dict):
        dataset_id = run['defaultDatasetId']
    else:
        dataset_id = run.default_dataset_id

    for item in client.dataset(dataset_id).iterate_items():
        return item.get("text", "")

    return ""



if __name__ == "__main__":
    job_posting_url = input("Enter the job posting URL: ")
    start = time.perf_counter()

    website_text = extract_website_data(job_posting_url)

    print(website_text)
    print("TIME TAKEN =", time.perf_counter() - start)