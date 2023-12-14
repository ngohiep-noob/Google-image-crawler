from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import requests
import time
import os
import base64


class GoogleImageCrawler:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        print("Chrome driver is initialized.")
        self.time_sleep = 5

        self.url = f"https://www.google.com/imghp?hl=en"

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
        for img in soup.find_all("img", class_="rg_i Q4LuWd"):
            if img.has_attr("src"):
                img_urls.append(img["src"])
            elif img.has_attr("data-src"):
                img_urls.append(img["data-src"])
            else:
                print("No image url found!")
        return img_urls

    def save_imgs(self, img_url, file_name):
        img = requests.get(img_url)
        with open(file_name, "wb") as f:
            f.write(img.content)

    def get_img_urls_from_keyword(self, keyword, scroll_num=1):
        url = self.get_url(keyword)
        self.driver.get(url)

        search_box = self.driver.find_element(By.CLASS_NAME, "gLFyf")
        search_box.send_keys(keyword)
        submit_button = self.driver.find_element(By.CLASS_NAME, "Tg7LZd")
        submit_button.click()
        time.sleep(self.time_sleep)

        self.scroll(scroll_num)
        soup = self.get_soup()
        img_urls = self.get_img_urls(soup)
        return img_urls

    def terminate(self):
        self.driver.quit()
        print("Chrome driver is terminated.")

    def save_images(self, img_urls, save_path):
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            print(f'Path "{save_path}" does not exist, a new folder is created!')

        for idx, img_url in enumerate(img_urls):
            with open(f"{save_path}/{idx}.jpg", "wb") as f:
                if img_url.startswith("data:image"):
                    img_content = base64.b64decode(img_url.split(",")[1])
                    f.write(img_content)
                else:
                    img = requests.get(img_url)
                    f.write(img.content)

        print(f'Saved {len(img_urls)} images to "{save_path}"')
