# Page scraping tooling
from trafilatura import fetch_url, extract

def get_text(url: str):
  page = fetch_url(url)
  result = extract(page)
  return str(result)