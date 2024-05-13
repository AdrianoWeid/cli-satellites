import os
import questionary
from utils import display_spinner
from  satellite_search_service import get_satellites_list
from info import info_ui 

def list_ui():
    command = "cls" if os.name == "nt" else "clear"
    current_page = 1
    
    while True:
        
    
        display_spinner("Loading Satellites...")
        satellites = get_satellites_list(current_page)
        if satellites.empty:
            print("No satellites available.")
        
        selections = [questionary.Choice(title=f"NORAD_Number: {row["NORAD Number"]},  Satellite: {row["Current Official Name of Satellite"]}", value= (row["NORAD Number"], row["Current Official Name of Satellite"])) for index, row in satellites.iterrows()]
        selections.append(questionary.Choice(title="Load more", value="more"))
        selections.append(questionary.Choice(title="Back to Main Menu", value="main_menu"))
        selections.append(questionary.Choice(title="Exit", value="exit"))
        
        satellite = questionary.select(
            "Select a satellite to get more information",
            choices=selections
        ).ask()

        if satellite == "more":
            os.system(command)
            current_page += 1
        elif satellite == "main_menu":
            return
        elif satellite == "exit":
            os.system(command)
            exit(0)
        else:
            info_ui(satellite)

if __name__ =="__main__":
    list_ui()