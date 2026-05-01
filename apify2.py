from apify_client import ApifyClient


client = ApifyClient('apify_api_nFo0ErbZExVP08c1ozdhQQHgEBkss40HAJ9E')
job_posting_url = input('Enter the job posting URL: ')
run = client.actor("aYG0l9s7dbB7j3gbS").call(
    run_input={
        "startUrls": [{"url": job_posting_url}],
        "maxCrawlDepth": 0,
        "maxCrawlPages": 1,
        "maxResults": 1,
        "htmlTransformer": "readableText"
    }
)

items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
global result
for item in items:
   result = item['text']
