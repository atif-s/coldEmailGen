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
'''def fallback(text):
    if len(text) < 1000:
        return True
    job_keywords = ['responsibility' , 'responsibilities' , 'experience' , 'education' , 'skills' , 'experience' , 'qualifications' , 'qualification']
    if not any(k in text.lower() for k in job_keywords):
        return True
    js_fail = ['enable javascript' , 'login to continue']
    if any(x in text.lower() for x in js_fail):
        return True
    return False'''

def extract_website_data(job_posting_url: str) -> str:
    '''headers = {
            "User-Agent": "Mozilla/5.0"
        }
    response = requests.get(job_posting_url,headers = headers , timeout = 5)
    response.raise_for_status()
    doc = Document(response.text)
    doc = doc.summary()

    soup = BeautifulSoup(doc,"html.parser")
    text = soup.get_text(separator = " " , strip = True)

    if fallback(text):'''
    run = client.actor("aYG0l9s7dbB7j3gbS").call(
    run_input={
            "startUrls": [{"url": job_posting_url}],
                "maxCrawlDepth": 0,
        "maxCrawlPages": 1,
            "maxResults": 1,
            "htmlTransformer": "readableText"
    }
    )

    for item in client.dataset(run['defaultDatasetId']).iterate_items():
         return item.get("text", "")

    return ""



if __name__ == "__main__":
    job_posting_url = input("Enter the job posting URL: ")
    start = time.perf_counter()

    website_text = extract_website_data(job_posting_url)

    print(website_text)
    print("TIME TAKEN =", time.perf_counter() - start)