"""
get_vorrat.py:  EXTRACTS VORRAT FROM SHERLOCK HOLMES PAGE.
date:           2024-05-02
"""

import requests
from bs4 import BeautifulSoup

SHERLOCK_HOLMES_GESELLSCHAFT    = "https://sherlock-holmes-gesellschaft.de/product/"
BAKER_STREET_CHRONICLE_01_48    = "ausgabe-"
BAKER_STREET_CHRONICLE_49_MAX   = "baker-street-chronicle-nr-"

BAKER_STREET_CHRONICLE_SWITCH   = 49
BAKER_STREET_CHRONICLE_MAX      = 52    # CHANGE ME!

HTML_P_TAG_PREFIX               = "<p class=\"stock in-stock\">"

def extract_number_from_ptag(ptag):
    n = len(HTML_P_TAG_PREFIX)
    cut = ptag[n:]
    i = 0
    for c in cut:
        if c == " ":
            return cut[:i]
        i += 1
    return cut

def get_vorrat(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup    = BeautifulSoup(response.content, 'html.parser')
        ptag   = soup.find('p', class_='stock in-stock')
        if ptag:
            return int(extract_number_from_ptag(str(ptag)))
    return -1

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
STATUS_1_TEXT   = "- ALARM ALARM -"
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
    for i in range(1, BAKER_STREET_CHRONICLE_MAX+1):
        url = SHERLOCK_HOLMES_GESELLSCHAFT
        url += BAKER_STREET_CHRONICLE_01_48 \
                if (i < BAKER_STREET_CHRONICLE_SWITCH) \
                else BAKER_STREET_CHRONICLE_49_MAX
        url += leading_zero(i)
        
        vorrat = get_vorrat(url)
        print(color_text(
            ausverkauft_status_color(vorrat),
            "Baker Street Chronicle Nr. " + leading_zero(i) + ":\t"
            + str(vorrat) + "\t "
            + ausverkauft_status_text(vorrat) + " \t\t ("
            + url + ")"
        ))
    pass

if __name__ == "__main__":
    main()
