import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from data_processing import *
import numpy as np


def scrape_phone_number(companies):
    driver = webdriver.Chrome("./chromedriver")
    driver.maximize_window()

    companies_phone_number = {}
    list_comp_phone_number = []

    companies = replace_space_duckduckgo(companies)

    for comp in companies:
        try:
            # search for the company in 118712 link
            driver.get(f"https://annuaire.118712.fr/en/?s={comp}")
            time.sleep(1)
            ########################### click on the first the company
            if comp == companies[0]:
                Xpath_professionals_button = (
                    "/html/body/section/div[5]/div[1]/div[2]/div[2]/label[2]/span[3]"
                )
                driver.find_element_by_xpath(Xpath_professionals_button).click()
            Xpath_company_phn = "/html/body/section/div[5]/div[2]/div[2]/article[1]/div[1]/div/div[2]/div[3]/a[2]/span[2]"
            comp_phone_number = driver.find_element_by_xpath(
                Xpath_company_phn
            ).get_attribute("innerText")

            list_comp_phone_number.append(comp_phone_number)
        except:
            list_comp_phone_number.append(np.nan)

    companies = recover_space_duckduckgo(companies)
    companies_phone_number["entreprise"] = companies
    companies_phone_number["phone_number"] = list_comp_phone_number

    time.sleep(1)
    driver.quit()
    print("Scraping finished !")

    final_data = pd.DataFrame(companies_phone_number)
    print(final_data)
    final_data_csv(final_data, "scraped_companies_phone_number.csv")
