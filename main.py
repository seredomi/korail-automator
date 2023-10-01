from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import service
from selenium.webdriver.firefox.service import Service


def main():
    with webdriver.Firefox(service=Service('/usr/bin/geckodriver')) as driver:
        driver.get("https://www.letskorail.com/ebizbf/EbizbfForeign_pr16100.do?gubun=1")
        title = driver.title
        driver.implicitly_wait(0.5)
        driver.find_element(By.XPATH, "//*[@id=\"resrv_info\"]/ul/li/a").click()

        print("yoo")

        while(True):
            i = 1

if __name__ == "__main__":
    main()
