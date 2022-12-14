from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
from time import sleep
from random import randrange
from tqdm import tqdm

Path('outputs').mkdir(exist_ok=True)

main_page = 'https://www.sec.gov/litigation/litreleases.htm'


# collect all the historical Litigation Releases for SEC Press
def create_historical_lr_index(archive_url: str = main_page):
    # Go to SEC Litigation Releases
    browser.get(archive_url)
    archives = browser.find_element(By.ID,
                                    value='archive-links').find_elements(By.TAG_NAME,
                                                                         value='a')
    # get all archive links for all years
    archive_urls: list = []
    for element in archives:
        url = element.get_attribute(name='href')
        archive_urls.append(url)

    # find all Litigation Releases in each year (LR)
    lr_urls = []
    for url in archive_urls:
        browser.get(url)
        all_lrs = browser.find_elements(By.XPATH, '//a[contains(text(),"LR-")]')
        for element in all_lrs:
            url = element.get_attribute(name='href')
            lr_urls.append(url)

    with open('outputs/litigation_releases_index.txt', mode='w') as index_file:
        for url in lr_urls:
            index_file.write(url + "\n")


# collect Litigation Releases of interest
def collect_lrs(path_to_index_file: str):
    Path('outputs', 'litigation_releases_text').mkdir(parents=True, exist_ok=True)
    with open(path_to_index_file) as index_file:
        index_file = index_file.read().split()

    print(f'There are {len(index_file)} urls in the index file.')
    print('starting keyword search...')
    for url in tqdm(index_file):
        litigation_release = url.split('/')[-1].split(".")[0]
        year = url.split('/')[-2]
        try:
            year = int(year)
        except ValueError:
            pass
        if not isinstance(year, int):
            year = 'Before 2006'

        browser.get(url)
        lr_text: str = browser.find_element(By.TAG_NAME, value='body').text
        Path('outputs', 'litigation_releases_text', f'{year}').mkdir(parents=True, exist_ok=True)
        with open(f'outputs/litigation_releases_text/{year}/{litigation_release}.txt', mode='w') as text_file:
            text_file.write(lr_text)
        sleep(randrange(1, 5))


if __name__ == '__main__':
    # open browser
    browser_options = webdriver.ChromeOptions()
    browser_options.add_argument('--headless')
    browser_service = Service(executable_path=ChromeDriverManager().install())
    browser = webdriver.Chrome(service=browser_service, options=browser_options)

    collect_lrs(path_to_index_file='outputs/litigation_releases_index.txt')

    browser.close()
