# Testing page scraping tooling
from trafilatura import fetch_url, extract

url = "https://www.linkedin.com/jobs/view/4464317865/"
page = fetch_url(url)

result = extract(page)
print(result)