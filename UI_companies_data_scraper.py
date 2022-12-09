import tkinter as tk
from turtle import heading
from linkedin_scraper import scrape_profils_linkedin
from pappers_scraper import scrape_pappers_companies
from phone_number_scraper import scrape_phone_number
from data_merge import merge_extracted_data
from website_scraper import scrape_companies_website

companies = []


def add():
    L = e1.get().split(",")
    L = [comp.strip() for comp in L]
    for comp in L:
        companies.append(comp)
    print(companies)
    e1.delete(0, "end")

def clear():
    companies.clear()
    print(companies)
    e1.delete(0, "end")


def openProgram_Linkedin():
    master.quit
    scrape_profils_linkedin(companies)


def openProgram_Pappers():
    master.quit
    scrape_pappers_companies(companies)


def openProgram_118712():
    master.quit
    scrape_phone_number(companies)


def openProgram_DuckDuckGo():
    master.quit
    scrape_companies_website(companies)


def mergeData():
    master.quit
    merge_extracted_data()


master = tk.Tk()
master.title("Companies Data Scraper")


tk.Label(master, text="Company name:").grid(row=0)

e1 = tk.Entry(master, width=100)

e1.grid(row=0, column=2, pady=8, padx=8)


tk.Button(master, text="Add companies", command=add).grid(
    row=2, column=1, sticky=tk.W, pady=2
)

tk.Button(master, text="Clear companies", command=clear).grid(
    row=2, column=2, sticky=tk.W, pady=4
)

tk.Button(master, text="Run Pappers Scraper", command=openProgram_Pappers).grid(
    row=2, column=3, sticky=tk.W, pady=4
)

tk.Button(master, text="Run LinkedIn Scraper", command=openProgram_Linkedin).grid(
    row=2, column=4, sticky=tk.W, pady=4
)

tk.Button(master, text="Run 118712 Scraper", command=openProgram_118712).grid(
    row=2, column=5, sticky=tk.W, pady=4
)

tk.Button(master, text="Run Websites Scraper", command=openProgram_DuckDuckGo).grid(
    row=2, column=6, sticky=tk.W, pady=4
)

tk.Button(master, text="Get Final Data", command=mergeData).grid(
    row=2, column=7, sticky=tk.W, pady=4
)

tk.Button(master, text="Quit", command=master.destroy).grid(
    row=2, column=8, sticky=tk.W, pady=4
)

tk.mainloop()
