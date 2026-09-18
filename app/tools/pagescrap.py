# Page scraping tooling
from trafilatura import fetch_url, extract

def get_text(url: str) -> str:
  """Get the text of a web page given a url
  
  Args:
    url: the url of the page

  Returns:
    A string containing the text of the web page
  """
  page = fetch_url(url)
  result = extract(page)
  return str(result)