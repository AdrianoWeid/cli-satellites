from satellite_position_service import get_tle
from utils import print_satellite_info, display_spinner
import questionary
import os

def info_ui(satellite):
    norad_number, satellitename = satellite
    tle = get_tle(norad_number)
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)
    print_satellite_info(satellitename, tle)

    while True:
        selections = [] 
        selections.append(questionary.Choice(title="Back to selection", value="more"))
        selections.append(questionary.Choice(title="Back to Main Menu", value="main_menu"))
        selections.append(questionary.Choice(title="Exit", value="exit"))
        
        satellite = questionary.select(
            "",
            choices=selections
        ).ask()

        if satellite == "more":
            current_page += 1
        elif satellite == "main_menu":
            return
        elif satellite == "exit":
            exit(0)
        else:
            info_ui(satellite)
