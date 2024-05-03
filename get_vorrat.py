"""
get_vorrat.py:  EXTRACTS VORRAT FROM SHERLOCK HOLMES PAGE.
date:           2024-05-02
"""

import requests
from bs4 import BeautifulSoup
import webbrowser

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

SHERLOCK_HOLMES_GESELLSCHAFT    = "https://sherlock-holmes-gesellschaft.de/product/"
BAKER_STREET_CHRONICLE_01_48    = "ausgabe-"
BAKER_STREET_CHRONICLE_49_MAX   = "baker-street-chronicle-nr-"

BAKER_STREET_CHRONICLE_SWITCH   = 49
BAKER_STREET_CHRONICLE_MAX      = 52    # CHANGE ME!

HTML_P_TAG_PREFIX               = "<p class=\"stock in-stock\">"

def cut_until_ws(s):
    i = 0
    for c in s:
        if c == " ":
            return s[:i]
        i += 1
    return s

def extract_number_from_ptag(ptag):
    return cut_until_ws(ptag[len(HTML_P_TAG_PREFIX):])

def get_vorrat_using_selenium(url):
    options             = Options()
    options.headless    = True
    driver  = webdriver.Firefox(options=options)
    driver.get(url)
    vorrat  = -1
    try:
        select_element = driver.find_element(By.CLASS_NAME, "mfn-vr-select")
        select = Select(select_element)
        select.select_by_value("mit Beilage")
        p_tag   = driver.find_element(By.CSS_SELECTOR, "p.stock.in-stock")
        vorrat  = int(cut_until_ws(p_tag.text))
        driver.quit()
        return vorrat
    except:
        driver.quit()
        return vorrat

def get_vorrat(url):
    response = requests.get(url)
    # search on sites without "Beilage" using bs4
    if response.status_code == 200:
        soup    = BeautifulSoup(response.content, "html.parser")
        ptag   = soup.find("p", class_="stock in-stock")
        if ptag:
            return int(extract_number_from_ptag(str(ptag))), False
        select  = soup.find("select", class_="mfn-vr-select attribute_beilage")
        if select:
            return get_vorrat_using_selenium(url), True
    return -1, False

def leading_zero(n):
    if n >= 0 and n < 10:
        return "0" + str(n)
    return str(n)

COL_GREY    = "\033[90m"
COL_RED     = "\033[91m"
COL_YELLOW  = "\033[93m"
COL_RESET   = "\033[0m"

def color_text(col, text):
    return col + text + COL_RESET

STATUS_0_VAL    = 0
STATUS_1_VAL    = 5
STATUS_2_VAL    = 10

STATUS_0_TEXT   = "- AUSVERKAUFT -"
STATUS_1_TEXT   = "-    ALARM    -"
STATUS_2_TEXT   = "-   WARNUNG   -"
STATUS_3_TEXT   = "               "

STATUS_0_COL    = COL_GREY
STATUS_1_COL    = COL_RED
STATUS_2_COL    = COL_YELLOW
STATUS_3_COL    = COL_RESET

def ausverkauft_status_text(vorrat):
    if vorrat < STATUS_0_VAL:
        return STATUS_0_TEXT
    if vorrat <= STATUS_1_VAL:
        return STATUS_1_TEXT
    if vorrat <= STATUS_2_VAL:
        return STATUS_2_TEXT
    return STATUS_3_TEXT

def ausverkauft_status_color(vorrat):
    if vorrat < STATUS_0_VAL:
        return STATUS_0_COL
    if vorrat <= STATUS_1_VAL:
        return STATUS_1_COL
    if vorrat <= STATUS_2_VAL:
        return STATUS_2_COL
    return STATUS_3_COL

def main():
    firefox_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))

    for i in range(1, BAKER_STREET_CHRONICLE_MAX+1):
        url = SHERLOCK_HOLMES_GESELLSCHAFT
        url += BAKER_STREET_CHRONICLE_01_48 \
                if (i < BAKER_STREET_CHRONICLE_SWITCH) \
                else BAKER_STREET_CHRONICLE_49_MAX
        url += leading_zero(i)
        
        vorrat, mit_beilage = get_vorrat(url)
        print(color_text(
            ausverkauft_status_color(vorrat),
            "Baker Street Chronicle Nr. " + leading_zero(i)
            + (" (B):" if mit_beilage else ":    ") + "\t"
            + str(vorrat) + "\t"
            + ausverkauft_status_text(vorrat) + " \t("
            + url + ")"
        ))
        #if ausverkauft_status_text(vorrat) == STATUS_0_TEXT:
        #    webbrowser.get("firefox").open(url)

if __name__ == "__main__":
    main()

