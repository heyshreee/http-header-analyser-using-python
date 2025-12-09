import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .utils import normalize_url

def fetch_headers(url: str, method="GET", follow_redirects=True, timeout=10):
    """
    Fetches headers from the target URL.
    Returns a dictionary containing headers, status code, and URL.
    """
    target_url = normalize_url(url)
    
    # Configure retry logic (3 attempts)
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        response = session.request(
            method=method,
            url=target_url,
            allow_redirects=follow_redirects,
            timeout=timeout,
            headers={"User-Agent": "HeaderScan-Tool/1.0"} # Polite User-Agent
        )
        
        return {
            "success": True,
            "url": response.url,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "http_version": response.raw.version
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "url": target_url,
            "error": str(e)
        }
        
        