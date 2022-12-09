import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

from data_processing import *


def scrape_companies_website(companies):

    companies = replace_space_duckduckgo(companies)

    infos = {}
    websites = []

    driver = webdriver.Chrome("./chromedriver")
    driver.maximize_window()

    for comp in companies:
        driver.get(f"https://duckduckgo.com/?q={comp}+company&t=h_&ia=web")
        time.sleep(1)
        if comp == companies[0]:
            Xpath_button_set_france_region = (
                "/html/body/div[2]/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div"
            )
            driver.find_element(By.XPATH, Xpath_button_set_france_region).click()

        Xpath_siteweb = f"/html/body/div[2]/div[5]/div[3]/div/div[1]/div[5]/div[1]/article/div[1]/div/a/span"
        url_company_siteweb = driver.find_element(
            By.XPATH, Xpath_siteweb
        ).get_attribute("innerText")
        websites.append(url_company_siteweb)

    driver.quit()
    print("Scraping finished !")

    companies = recover_space_duckduckgo(companies)
    infos["entreprise"] = companies
    infos["siteweb_entreprise"] = websites

    final_data = pd.DataFrame(infos)
    print(final_data)

    final_data_csv(final_data, "scraped_websites.csv")
