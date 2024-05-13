from satellite_position_service import get_tle
from utils import print_satellite_info, display_spinner
from map import map_ui
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
        selections.append(questionary.Choice(title="View map", value="map"))
        selections.append(questionary.Choice(title="Back to selection", value="selection"))
        selections.append(questionary.Choice(title="Exit", value="exit"))
        
        satellite = questionary.select(
            "",
            choices=selections
        ).ask()

        if satellite == "map":
            os.system(command)
            map_ui(norad_number)
        elif satellite == "selection":
            os.system(command)
            return
        elif satellite == "exit":
            os.system(command)
            exit(0)
        else:
            info_ui(satellite)
