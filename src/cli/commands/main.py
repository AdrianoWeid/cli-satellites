#!/usr/bin/env python3
import os
import questionary
import satellite_list

def main_menu():
    os.system('clear')
    
    while True: 
        selection = questionary.select(
        "Please select an Option",
        choices=[
            "View List",
            "Search",
            "Exit"
        ]).ask()

        if selection == "View List":
            os.system('clear')
            list.list_ui()
        elif selection == "Search":
            os.system('clear')


        elif selection == "Exit":
            return
        
if __name__ == "__main__":
    main_menu()