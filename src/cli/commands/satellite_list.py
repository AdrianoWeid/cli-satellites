import os
import questionary
from src.cli.utils import display_spinner
from  src.libs.satellite_search_service import get_satellites
from info import info_ui 

def list_ui():
    current_page = 1
    os.system("clear")
    display_spinner("Searching...")
    satellites = get_satellites(None,current_page,None)
    print(satellites)
    if not satellites:
        print("No satellites available.")
        return

    selections = [questionary.Choice(title=sat.name, value=sat) for sat in satellites]
    selections.append(questionary.Choice(title="Cancel", value=None))

    satellite = questionary.select(
        "Select a satellite to get more information",
        choices=selections
    ).ask()

    if satellite:
        info_ui(satellite)
    else:
        print("Cancelled.")
