import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from tweepy import Client

DATE_FORMAT = '%Y-%m-%d'
LOGIN_URL = 'https://twitter.com/i/flow/login'
DELAY = 1
MAX_SCROLL_GAP = 10
MAX_RANGE_DAYS = 7

class TwitterScraper:

    def __init__(self, gecko_path, api_key, api_secret, token, token_secret, bearer_token, headless=True):
        driver_options = webdriver.FirefoxOptions()
        driver_options.headless = headless

        self.driver = webdriver.Firefox(options=driver_options, executable_path=gecko_path)
        self.api_client = Client(bearer_token, api_key, api_secret, token, token_secret)

    def close(self):
        self.driver.quit()

    def wait(self, ecs):
        WebDriverWait(self.driver, DELAY).until(ecs)

    def wait_for_elem(self, *args):
        self.wait(expected_conditions.presence_of_element_located(args))

    def wait_for_url(self, url):
        self.wait(expected_conditions.url_to_be(url))

    def scrolled_to_bottom(self):
        distance = float(self.driver.execute_script("return document.body.scrollHeight - (window.innerHeight + window.scrollY)"))
        return distance < MAX_SCROLL_GAP

    def scrolled_to_top(self):
        scrollY = float(self.driver.execute_script("return window.scrollY"))
        return scrollY == 0

    def search_url(self, keywords, start_date, end_date):
        start_str = start_date.strftime(DATE_FORMAT)
        end_str = end_date.strftime(DATE_FORMAT)
        q = '%20'.join(keywords)

        return f'https://twitter.com/search?f=live&q={q}%20until%3A{end_str}%20since%3A{start_str}&src=typed_query'

    def keyword_search(self, keywords, start_date, end_date, save_path=None, max_range_days=MAX_RANGE_DAYS):
        start_date = datetime.strptime(start_date, DATE_FORMAT)
        end_date = datetime.strptime(end_date, DATE_FORMAT)

        try:
            return self._keyword_search(keywords, start_date, end_date, save_path, max_range_days)
        except Exception as e:
            print("Keyword search failed:", e)
        finally:
            self.close()

    def _keyword_search(self, keywords, start_date, end_date, save_path, max_range_days):
        time_diff = end_date - start_date

        if time_diff.days > MAX_RANGE_DAYS:
            midpoint = start_date + time_diff / 2
            self._keyword_search(keywords, start_date, midpoint, save_path, max_range_days)
            self._keyword_search(keywords, midpoint, end_date, save_path, max_range_days)
        else:
            TWEET_LINK_CLASS = '.css-4rbku5.css-18t94o4.css-901oao.r-1bwzh9t.r-1loqt21.r-xoduu5.r-1q142lx.r-1w6e6rj.r-37j5jr.r-a023e6.r-16dba41.r-9aw3ui.r-rjixqe.r-bcqeeo.r-3s2u2q.r-qvutc0'
            search_url = self.search_url(keywords, start_date, end_date)
            self.driver.get(search_url)

            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

                time.sleep(1)
                if self.scrolled_to_bottom():
                    break

            ids = set()

            while not self.scrolled_to_top():
                tweets = self.driver.find_elements(By.TAG_NAME, 'article')
                for tweet in tweets:
                    tweet_link = tweet.find_element(By.CSS_SELECTOR, TWEET_LINK_CLASS)
                    id = tweet_link.get_attribute('href').split('/')[-1]
                    ids.add(id)

                self.driver.execute_script("window.scrollBy(0, -document.body.offsetHeight)")
                time.sleep(1)

            if save_path is not None:
                with open(save_path, 'w') as f:
                    for id in ids:
                        f.write(f'{id}\n')
            
            return ids

    def get_by_id(self, id, expansions=None):
        return self.api_client.get_tweet(id, expansions=expansions)

    def id_search(self, ids):
        return [self.get_by_id(id) for id in ids]

    def get_conversation(self, id):
        tweet = self.get_by_id(id, expansions="author_id")
        author = tweet.includes['users'][0].username
        conversation_url = f"https://twitter.com/{author}/status/{id}"
        print(conversation_url)
        self.driver.get(conversation_url)
        el = self.driver.find_element("xpath", "//tag[contains(text(), 'word')]")
        print(el)