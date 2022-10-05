from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

Path.mkdir(Path('outputs'), exist_ok=True)

main_page = 'https://www.sec.gov/litigation/litreleases.htm'


# collect all the historical Litigation Releases for SEC Press
def create_historical_LR_index(archive_url: str = main_page):
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
    LR_urls = []
    for url in archive_urls:
        browser.get(url)
        all_LRs = browser.find_elements(By.XPATH, '//a[contains(text(),"LR-")]')
        for element in all_LRs:
            url = element.get_attribute(name='href')
            LR_urls.append(url)

    with open('outputs/litigation_releases_index.txt', mode='w') as index_file:
        for url in LR_urls:
            index_file.write(url+"\n")

# collect Litigation Releases of interest
def collect_historical_LRs(keyword: str = 'Twitter'):
    for

if __name__ == '__main__':
    # open browser
    browser_options = webdriver.ChromeOptions()
    browser_service = Service(executable_path=ChromeDriverManager().install())
    browser = webdriver.Chrome(service=browser_service)

    # browser.close()
