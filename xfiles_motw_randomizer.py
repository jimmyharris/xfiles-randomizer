import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path

from parse import parse

import seasons

html = requests.get("https://x-files.fandom.com/wiki/Monster_of_the_Week")

soup = BeautifulSoup(html.text, features="lxml")

rows = soup.find("table", attrs={"class": "wikitable"}).find_all("tr")

season = None
motw_list = []

for row in rows:

    headers = row.find_all("th", attrs={"colspan": "3"})

    if headers:
        season = seasons.Season.new_season(
            parse("Season {season:d}", headers[0].text.strip())["season"]
        )
        motw_list.append(season)

    cells = row.find_all("td")

    if cells:
        ep = season.add_episode(
            episode=int(cells[0].text),
            title=cells[1].a.text,
            url=f'https://x-files.fandom.com{cells[1].a.get("href")}',
        )
        print(repr(ep))

if __name__ == "__main__":
    print("Saving file")

    seasons.write_json(seasons=motw_list, filename=(seasons.SRC_DIR / "motw_episodes.json"))

    import code

    code.interact(local=dict(motw=motw_list))
