from selenium import webdriver
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import requests
import time
import os


class PinterestCrawler:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=options)
        print("Chrome driver is initialized.")
        self.time_sleep = 5

        self.url = f"https://www.pinterest.com/search/pins/?"

    def get_url(self, keyword):
        params = {
            "q": keyword,
            "rs": "typed",
        }
        url = self.url + urlencode(params)
        return url

    def scroll(self, num_scroll=1):
        for _ in range(num_scroll):
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(self.time_sleep)

    def get_soup(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def get_img_urls(self, soup):
        img_urls = []
        for img in soup.find_all("img", class_="hCL kVc L4E MIw"):
            img_urls.append(img["src"])
        return img_urls

    def save_imgs(self, img_url, file_name):
        img = requests.get(img_url)
        with open(file_name, "wb") as f:
            f.write(img.content)

    def get_img_urls_from_keyword(self, keyword, scroll_num=1):
        url = self.get_url(keyword)
        self.driver.get(url)
        self.scroll(scroll_num)
        soup = self.get_soup()
        img_urls = self.get_img_urls(soup)

        self.driver.close()
        return img_urls

    def save_images(self, img_urls, save_path):
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            print(f"Path {save_path} does not exist, a new folder is created!")

        for idx, img_url in enumerate(img_urls):
            img = requests.get(img_url)
            with open(f"{save_path}/{idx}.jpg", "wb") as f:
                f.write(img.content)

        print(f"Saved {len(img_urls)} images to {save_path}")
