from flask import Flask, request
from bs4 import BeautifulSoup
import requests
import re
import time
gupshup_api = 'https://api.gupshup.io/sm/api/v1/msg'

app = Flask(__name__)

@app.route('/',methods = ['GET', 'POST'])
def wikibot():
    url = "https://apersonbot.toolforge.org/pending-subs/"
    response = requests.get(url)
    response_text = response.text

    # getting the total number of submissions
    current_total = re.search(r"\b(window.pendingSubsDraftCount = (\d+))\b",response_text, re.IGNORECASE).group(2)
    # getting the current status of N2N
    current_status = re.search(r"(<td id='status-Draft:N2N-Services-Inc'>(\w+)</td></tr>)",response_text, re.IGNORECASE).group(2)

    soup = BeautifulSoup(response_text, "html.parser")

    table_tags = soup.find('table' ,attrs={'id':'result'}).find_all('td')

    pageName = []
    for link in table_tags:
        all_anchors = link.findAll('a', href=True)
        if len(all_anchors)!=0:
            all_anchors = str(all_anchors[0])
            try:
                dre = re.search(r'(>)(Draft:.+)(</a>)',all_anchors)
                pageName.append(dre.group(2))
            except:
                continue
            
    for name in range(len(pageName)):
        if pageName[name]== "Draft:N2N Services Inc":
            namepos = name+1

    message = "N2N services is currently under review and in position {} of {}. The review status is {}".format(namepos,current_total,current_status)
    return message

if __name__ == '__main__':
    app.run()