import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

from data_processing import *

def Xpath():
    Xpath_NomEntreprise= "/html/body/div/div[3]/div[2]/div[1]/h1"
    Xpath_InfosHeader = "/html/body/div/div[3]/div[2]/table/tbody"
    Xpath_InfosJuridiques = "/html/body/div/div[4]/section[1]/div[2]/table/tbody"
    Xpath_TabFinances = "/html/body/div/div[4]/section[4]/div/div/div[1]"
    Xpath = [Xpath_NomEntreprise, Xpath_InfosHeader, Xpath_InfosJuridiques, Xpath_TabFinances]
    return Xpath
    

def scrape_pappers_companies(companies):

    companies = replace_space(companies)

    L = []

    driver = webdriver.Chrome("./chromedriver")
    driver.maximize_window()

    for comp in companies:
    #try:
        driver.get(f"https://www.pappers.fr/recherche?q={comp}")
        time.sleep(2)
        try:
            Xpath_button = "/html/body/div/div/div[3]/div[2]/div/a/button"
            driver.find_element_by_xpath(Xpath_button).click()
        except:
            Xpath_button = "/html/body/div/div/div[3]/div[2]/div[1]/a/button"
            driver.find_element_by_xpath(Xpath_button).click()

        time.sleep(2)
        print(Xpath()[0], Xpath()[1], Xpath()[2], Xpath()[3])
        # Get the text content of each element
        NomEntreprise = (
            driver.find_element_by_xpath(Xpath()[0])
            .get_attribute("innerText")
            .replace("\n", " ")
            .replace(".", "")
        )
        
        InfosHeader = driver.find_element_by_xpath(Xpath()[1]).get_attribute(
            "innerText"
        )
        InfosJuridiques = driver.find_element_by_xpath(Xpath()[2]).get_attribute(
            "innerText"
        )
        TabFinances = driver.find_element_by_xpath(Xpath()[3]).get_attribute(
            "innerText"
        )

        # InfosHeader
        try:
            InfosHeader = InfosHeader.replace("\t", " ")
            # Abbreviate some words
            InfosHeader = abbrev_Header(InfosHeader)
            # The result in list format
            InfosHeader = txt_to_list(InfosHeader)
            # Convert to dataframe
            data_infos_header = infos_to_df(
                InfosHeader,
                InfosHeader,
                InfosJuridiques,
                TabFinances,
                NomEntreprise,
            )
        except:
            print("InfosHeader was not found for : ", NomEntreprise)
            InfosHeader = pd.DataFrame(index=range(1), columns=range(6))
        # InfosJuridiques
        try:
            InfosJuridiques = InfosJuridiques.replace("\t", " ")
            # Abbreviate some words
            InfosJuridiques = abbrev_InfosJuridiques(InfosJuridiques)
            # The result in list format
            InfosJuridiques = txt_to_list(InfosJuridiques)
            # Convert to dataframe
            data_infos_jurid = infos_to_df(
                InfosJuridiques,
                InfosHeader,
                InfosJuridiques,
                TabFinances,
                NomEntreprise,
            )
        except:
            print("InfosJuridiques was not found for : ", NomEntreprise)
            InfosJuridiques = pd.DataFrame(index=range(1), columns=range(8))

        # TabFinances
        try:
            TabFinances = TabFinances.replace("\t", " ")
            TabFinances = TabFinances.replace(":", ";")
            TabFinances = TabFinances.replace(" 1 an", " un an")
            # Abbreviate some words
            TabFinances = abbrev_TabFinances(TabFinances)
            # The result in list format
            TabFinances = txt_to_list(TabFinances)
            # Delete redundants same as annee to keep juste one column annee in TabFianances
            TabFinances = del_redundants(TabFinances, TabFinances)
            # Convert to dataframe
            data_tab_fin = infos_to_df(
                TabFinances,
                InfosHeader,
                InfosJuridiques,
                TabFinances,
                NomEntreprise,
            )
        except:
            print("TabFinances was not found for :", NomEntreprise)
            data_tab_fin = pd.DataFrame(index=range(1), columns=range(1000))

        L.append(
            concat_data_entreprise(
                data_infos_header, data_infos_jurid, data_tab_fin
            )
        )
    #except:
        #print(comp, "was not found")

    driver.quit()
    
    print("Scraping finished !")
    companies = recover_space(companies)
    final_data = pd.concat([data for data in L], axis=0)
    final_data.insert(0, "entreprise", companies, True)
    final_data = final_data.reset_index()
    final_data = final_data[
        [
            "entreprise",
            "activite",
            "effectif",
            "creation",
            "dirigeants",
            "SIREN",
            "SIRET",
            "CA(€)_2021",
            "CA(€)_2020",
            "CA(€)_2019",
        ]
    ]
    print(final_data)

    final_data_csv(final_data, "scraped_companies_pappers.csv")
