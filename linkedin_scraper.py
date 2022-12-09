import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import config
from data_processing import (
    del_linkedin_member,
    final_data_csv,
    del_linkedin_member,
    recover_space,
    replace_space,
)
import pandas as pd


def scrape_profils_linkedin(companies):

    companies = replace_space(companies)

    driver = webdriver.Chrome("./chromedriver")
    driver.maximize_window()

    # get to the sign in link
    driver.get("https://www.linkedin.com/uas/login")

    # enter email and password and log in
    email_field = driver.find_element(By.CSS_SELECTOR, "input#username")
    password_field = driver.find_element(By.CSS_SELECTOR, "input#password")
    time.sleep(1)
    email_field.send_keys(config.email)
    password_field.send_keys(config.modpass)
    password_field.submit()
    time.sleep(2)

    infos = {}
    company = []
    name = []
    position = []
    location = []

    for comp in companies:
        ########################### click on the first the company
        driver.get(
            f"https://www.linkedin.com/search/results/companies/?keywords={comp}"
        )
        time.sleep(2)
        try:
            Xpath_company = "/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/ul/li[1]/div/div/div[2]/div[1]/div[1]/div/span/span"
            driver.find_element_by_xpath(Xpath_company).click()
        except:
            Xpath_company = "/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/ul/li[1]/div/div/div[2]/div[1]/div[1]/div/span/span"
            driver.find_element_by_xpath(Xpath_company).click()
        time.sleep(2)
        ########################### click on the link showing people working in that company
        try:
            Xpath_people = "/html/body/div[6]/div[3]/div/div[2]/div/div[2]/main/div[1]/section/div/div[2]/div[1]/div[2]/div/div/a[2]"
            driver.find_element_by_xpath(Xpath_people).click()
        except:
            pass
        try:
            Xpath_people = "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[1]/section/div/div[2]/div[1]/div[2]/div/div/a[2]"
            driver.find_element_by_xpath(Xpath_people).click()
        except:
            pass
        try:
            Xpath_people = "/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[1]/section/div/div[2]/div[1]/div[2]/div/a"
            driver.find_element_by_xpath(Xpath_people).click()
        except:
            pass
        try:
            Xpath_people = "/html/body/div[6]/div[3]/div/div[2]/div/div[2]/main/div[1]/section/div/div[2]/div[1]/div[2]/div/a"
            driver.find_element_by_xpath(Xpath_people).click()
        except:
            pass
        time.sleep(2)

        ########################### get the text relatif to each employee on the list
        for i in range(1, 11):
            try:
                try:
                    Xpath_infos = f"/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/ul/li[{i}]/div/div/div[2]/div[1]"
                    infos_non_processed = driver.find_element_by_xpath(
                        Xpath_infos
                    ).get_attribute("innerText")
                except:
                    try:
                        Xpath_infos = f"/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/ul/li[{i}]/div/div/div[2]/div[1]"
                        infos_non_processed = driver.find_element_by_xpath(
                            Xpath_infos
                        ).get_attribute("innerText")
                    except:
                        try:
                            Xpath_infos = f"/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/ul/li[{i}]/div/div/div[2]/div"
                            infos_non_processed = driver.find_element_by_xpath(
                                Xpath_infos
                            ).get_attribute("innerText")
                        except:
                            Xpath_infos = f"/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/ul/li[{i}]/div/div/div[2]/div"
                            infos_non_processed = driver.find_element_by_xpath(
                                Xpath_infos
                            ).get_attribute("innerText")

                infos_processed = infos_non_processed.split("\n")

                ########################### fill the lists by te comp name, emp name, emp position, emp location
                company.append(comp)
                name.append(infos_processed[0])
                position.append(infos_processed[-2])
                location.append(infos_processed[-1])

            except:
                print("No more profiles")
                break
    time.sleep(1)
    driver.quit()
    print("Scraping finished !")
    
    company = recover_space(company)
    companies = recover_space(companies)

    infos["entreprise"] = company
    infos["nom"] = name
    infos["post"] = position
    infos["region"] = location

    data = pd.DataFrame(infos)
    data = del_linkedin_member(data)
    print(data)

    final_data_csv(data, "scraped_profiles_linkedin.csv")
