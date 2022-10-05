from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

main_page = 'https://www.sec.gov/litigation/litreleases.htm'

if __name__ == '__main__':
    # open browser
    browser_options = webdriver.ChromeOptions()
    browser_service = Service(executable_path=ChromeDriverManager().install())
    browser = webdriver.Chrome(service=browser_service)

    # Go to SEC Litigation Releases
    browser.get(main_page)
    archives = browser.find_element(By.ID,
                                    value='archive-links').find_elements(By.TAG_NAME,
                                                                         value='a')

    # get all archive links
    archive_links: list = []
    for element in archives:
        url = element.get_attribute(name='href')
        archive_links.append(url)



    # browser.close()
