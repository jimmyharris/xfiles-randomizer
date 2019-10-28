import requests
from bs4 import BeautifulSoup
import os

from parse import parse

import pandas as pd

html = requests.get("https://x-files.fandom.com/wiki/Monster_of_the_Week")

soup = BeautifulSoup(html.text)

rows = soup.find("table", attrs={"class": "wikitable"}).find_all("tr")

season = None

motw_list = dict(season=[], episode=[], title=[], url=[])

for row in rows:

    headers = row.find_all("th", attrs={"colspan": "3"})

    if headers:
        season = parse("Season {season:d}", headers[0].text.strip())["season"]

    cells = row.find_all("td")

    if cells:
        episode_num = int(cells[0].text)
        title = cells[1].a.text
        wikia_link = f'https://x-files.fandom.com{cells[1].a.get("href")}'
        print(f's{season:02d}ep{episode_num:02d}: "{title}"')
        motw_list["season"].append(season)
        motw_list["episode"].append(episode_num)
        motw_list["title"].append(title)
        motw_list["url"].append(wikia_link)

motw_list = pd.DataFrame(motw_list)

motw_list.to_csv(os.path.join(os.path.dirname(__file__), "motw_files.csv"))
