from flask import Blueprint, jsonify
import requests
from bs4 import BeautifulSoup

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def get_scraped_data():
    URL = 'https://www.livescore.cz/?d=-1'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    yesterday_main = soup.find("div", {"id": "score-data"})
    all_rem = soup.find_all(['h4', 'img', 'span', 'br'])
    for i in all_rem:
        i.extract()
    a_tags = yesterday_main.find_all('a')
    for a in a_tags:
        a.replaceWith("-%s/" % a.string)
    yesterday_main.replaceWith("%s" % yesterday_main.string)
    URL = 'https://www.livescore.cz/index.php'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    today_main = soup.find("div", {"id": "score-data"})
    all_rem = soup.find_all(['h4', 'img', 'span', 'br'])
    for i in all_rem:
        i.extract()
    a_tags = today_main.find_all('a')
    for a in a_tags:
        a.replaceWith(",%s\n" % a.string)
    today_main.replaceWith("%s" % today_main.string)
    merged = str(yesterday_main) + str(today_main)
    matches = merged.split("/")
    final = []
    for m in matches:
        print(m)
        teams = m.split('-')
        if(len(teams) > 2):
            home = teams[0].strip()
            away = teams[1].strip()
            score = teams[2].split(":")
            if(score[0].isnumeric() and score[1].isnumeric()):
                final_result = "1" if int(score[0]) > int(score[1]) else "2" if int(score[1]) > int(score[0]) else "X"
                total = "O" if int(score[0]) + int(score[1]) > 2.5 else "U"
                final.append({
                    "home": home,
                    "away": away,
                    "final_result": final_result,
                    "total": total
                })
    return jsonify(final)