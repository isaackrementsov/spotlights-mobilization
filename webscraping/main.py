from dotenv import load_dotenv
from twitter_scraper import TwitterScraper
import os

load_dotenv()

def test_api():
    scraper = TwitterScraper(
        gecko_path='C:\Program Files\gecko\geckodriver',
        api_key=os.environ["API_KEY"],
        api_secret=os.environ["API_SECRET"],
        token=os.environ["TOKEN"],
        token_secret=os.environ["TOKEN_SECRET"],
        bearer_token=os.environ["BEARER_TOKEN"],
        headless=True
    )

    tweet = scraper.get_by_id("1566424397942083584")

def test_conversation():
    scraper = TwitterScraper(
        gecko_path='C:\Program Files\gecko\geckodriver',
        api_key=os.environ["API_KEY"],
        api_secret=os.environ["API_SECRET"],
        token=os.environ["TOKEN"],
        token_secret=os.environ["TOKEN_SECRET"],
        bearer_token=os.environ["BEARER_TOKEN"],
        headless=True
    )

    convo = scraper.get_conversation("1566424397942083584")  

def test_scraping():
    scraper = TwitterScraper(
        gecko_path='C:\Program Files\gecko\geckodriver',
        api_key=os.environ["API_KEY"],
        api_secret=os.environ["API_SECRET"],
        token=os.environ["TOKEN"],
        token_secret=os.environ["TOKEN_SECRET"],
        bearer_token=os.environ["BEARER_TOKEN"],
        headless=False
    )

    ids = scraper.keyword_search(
        keywords=['prison', 'abolition'],
        start_date='2022-09-01',
        end_date='2022-09-05',
        save_path='tweet_ids.txt'
    )

test_conversation()
