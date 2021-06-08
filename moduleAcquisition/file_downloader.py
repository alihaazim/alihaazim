import re
import os
import requests

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

url1 = "https://sante.sec.gouv.sn/taxonomy/term/14"
url2 = "https://sante.sec.gouv.sn/taxonomy/term/14?page="


def run_acq_code():
    def getSoup(link):
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        web_byte = urlopen(req).read()
        webpage = web_byte.decode('utf-8')
        return BeautifulSoup(webpage, "html.parser")

    list_of_pdf = set()

    soup1 = getSoup(url1)
    # on recupere le lien vers la derniere page du site
    last_li = soup1.select('ul .pager-last a')
    last_page_anchor = ''
    for i in last_li:
        last_page_anchor = i.attrs["href"]
    # numero de la derniere page
    last_page_number = re.findall('[0-9]+', last_page_anchor)

    subs1 = ['coronavirus', 'covid']
    subs2 = 'communiqué'

    pages_anchors = []
    pdf_page_links = []

    # for i in range(int(last_page_number[1]) + 1):  # obtention des liens des page contenant les pdf
    for i in range(2):  # obtention des liens des page contenant les pdf
        soup2 = getSoup(url2 + str(i))
        pages_anchors = soup2.select('article > h2 > a')
        for j in pages_anchors:  # obtention des liens des docs pdf
            if any(x in j.string.lower() for x in
                   subs1) and subs2 in j.string.lower():  # verification si le document est lie au covid19
                pdf_page_links.append('https://sante.sec.gouv.sn' + j.attrs["href"])

    pdf_links = []
    # recuperation des liens des pdf
    for i in range(len(pdf_page_links)):
        soup3 = getSoup(pdf_page_links[i])
        anchor = soup3.select('.file a')
        for j in anchor:
            pdf_links.append(j.attrs["href"])

    # telechargement des PDFs
    inc = '0'
    path = '../files/pdf'
    agent = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    for i in pdf_links:
        filename = os.path.join(path, 'doc' + inc + '.pdf')
        r = requests.get(i, headers=agent)
        with open(filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)
            print('telechargement '+i)
            copy = int(inc)
            copy += 1
            inc = str(copy)
