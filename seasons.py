from dataclasses import dataclass, asdict, field
import json
from typing import List, Optional
from pathlib import Path

import pyto_ui as ui

SRC_DIR = Path(__file__).parent


@dataclass
class EpisodeInfo:

    season: int = field(hash=True)
    episode: int = field(hash=True)
    title: str
    url: str

    def as_cell_view(self):
        cell = ui.TableViewCell(ui.TABLE_VIEW_CELL_STYLE_SUBTITLE)
        cell.text_label.text = f"Ep. {self.episode:02d}: {self.title}"
        cell.detail_text_label.text = self.url
        cell.accessory_type = ui.ACCESSORY_TYPE_DISCLOSURE_INDICATOR
        cell.removable = True
        return cell

    def __str__(self):

        return f's{self.season:02d}ep{self.episode:02d}: "{self.title}"'


@dataclass
class Season:

    number: int

    episodes: List[EpisodeInfo] = field(default_factory=list)

    @classmethod
    def new_season(cls, number):

        return cls(number=number)

    @classmethod
    def from_json(cls, *, number, episodes):

        ret = Season.new_season(number=number)

        for ep_dict in episodes:
            assert ep_dict.get("season") == number
            ret.episodes.append(EpisodeInfo(**ep_dict))

        return ret

    def add_episode(self, *, episode, title, url):
        ep = EpisodeInfo(season=self.number, episode=episode, title=title, url=url)
        self.episodes.append(ep)

        return ep

    def as_section_view(self):

        cells = [ep.as_cell_view() for ep in self.episodes]

        return ui.TableViewSection(f"Season {self.number}", cells)


def write_json(*, seasons: List[Season], filename: Path):

    filename.write_text(
        json.dumps(dict(seasons=[asdict(s) for s in seasons]), indent=2)
    )


def read_json(*, filename: Path):

    show = json.loads(filename.read_text())

    return [Season.from_json(**s) for s in show.get("seasons", [])]
