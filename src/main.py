#!/usr/bin/env python3
import os
import questionary
from list import list_ui


def main_menu():
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)
    
    while True: 
        selection = questionary.select(
        "Please select an Option",
        choices=[
            "View List",
            "Search",
            "Exit"
        ]).ask()

        if selection == "View List":
            os.system(command)
            list_ui()
        elif selection == "Search":
            os.system(command)
        elif selection == "Exit":
            break
        
    print("Program finished successfully.")
        
if __name__ == "__main__":
    main_menu()