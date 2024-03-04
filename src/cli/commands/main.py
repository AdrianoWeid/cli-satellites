import os
import questionary
def main_menu():
    os.system('clear')
    
    while True: 
        selection = questionary.select(
        "Please select an Option",
        choices=[
            "View List",
            "Exit"
        ]).ask()

        if selection == "View List":
            os.system('clear')
            list
        elif selection == "Exit":
            return
main_menu()