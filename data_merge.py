import pandas as pd
from data_processing import final_data_csv


def merge_extracted_data(
    data_pappers_path="./data∕scraped_companies_pappers.csv",
    data_linkedin_path="./data∕scraped_profiles_linkedin.csv",
    data_118712_path="./data∕scraped_companies_phone_number.csv",
    data_websites_path="./data∕scraped_websites.csv",
):

    data_pappers = pd.read_csv(data_pappers_path, delimiter=";", index_col=0)
    data_linkedin = pd.read_csv(data_linkedin_path, delimiter=";", index_col=0)
    data_118712 = pd.read_csv(data_118712_path, delimiter=";", index_col=0)
    data_websites = pd.read_csv(data_websites_path, delimiter=";", index_col=0)

    data_pappers_and_118712 = pd.merge(
        data_pappers, data_118712, how="inner", on="entreprise"
    )

    data_linkedin_and_websites = pd.merge(
        data_linkedin, data_websites, how="inner", on="entreprise"
    )

    final_data = pd.merge(
        data_linkedin_and_websites,
        data_pappers_and_118712,
        how="inner",
        on="entreprise",
    )
    print(final_data)

    final_data_csv(final_data, "./data∕all_data_scraped.csv")
    print("all_data_scraped was saved successfully!")
