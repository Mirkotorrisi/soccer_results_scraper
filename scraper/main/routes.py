from gevent import monkey
monkey.patch_all()

from flask import Blueprint, jsonify
import requests
from bs4 import BeautifulSoup

main = Blueprint('main', __name__)

yesterday_URL = 'https://www.livescore.cz/?d=-1'
today_URL = 'https://www.livescore.cz'

@main.route('/', methods=['GET'])
def get_data_and_format():
  merged = scrape_data_from_url(yesterday_URL) + scrape_data_from_url(today_URL)
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


def scrape_data_from_url(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    main = soup.find("div", {"id": "score-data"})
    all_rem = soup.find_all(['h4', 'img', 'span', 'br'])
    for i in all_rem:
        i.extract()
    a_tags = main.find_all('a')
    for a in a_tags:
        if(a['class'][0] == 'live'):
          a.replaceWith("-LIVE/")    
        else:
          a.replaceWith("-%s/" % a.string)    
    return main.decode_contents()