"""
A Table View with edition and navigation.
"""

import pyto_ui as ui

import webbrowser

import os

import seasons




motw_seasons = seasons.read_json(filename=(seasons.SRC_DIR / 'motw_episodes.json'))


all_items = { s.as_section_view(): s for s in motw_seasons}

def selected(section, cell_index):
    section.table_view.deselect_row()
    item = all_items[section].episodes[cell_index]

    wview = ui.WebView()
    
    section.table_view.push(wview)
    
    wview.load_url(item.url)

def deleted(section, cell_index):
    all_items[section].pop(cell_index)

for section in all_items.keys():
    section.did_select_cell = selected
    section.did_delete_cell = deleted

table_view = ui.TableView(sections=all_items.keys())
table_view.button_items = [table_view.edit_button_item]
ui.show_view(table_view, ui.PRESENTATION_MODE_SHEET)
