from InputData import MENU, resources,coins, DrinkIcon, DrumrollIcon,maintenance_options
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
def format_resource(resource_key):
    # Apply formatting to Value
    if resource_key in ["water", "milk"]:
        resource = "{:}ml".format(resources[resource_key])
    elif resource_key == "coffee":
        resource = "{:}g".format(resources[resource_key])
    elif resource_key == "money":
        resource = "${:,.2f}".format(resources[resource_key])
    else:
        resource = resources[resource_key]
    return resource
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
def run_report():
    for key in resources:
        # Apply formatting to Value
        resource = format_resource(key)
        print(f"{key}: {resource}")
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
def AmendResources(resource_choice,add_or_remove,amount):
    """Will either add or remove resource from resources"""
    resource_value = resources[resource_choice]
    if add_or_remove == "add":
        resources[resource_choice] += amount
    elif add_or_remove == "remove":
        if resource_value >= amount:
            resources[resource_choice] -= amount
        else:
            # Cap reduction to resource_value
            print(f"Removal capped at current resource amount of {format_resource(resource_choice)}")
            resources[resource_choice] = 0
        print(f"{resource_choice} balance: {format_resource(resource_choice)}.")
    else:
        # Invalid action
        pass
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
def run_maintenance():
    pass
    # Store maintenance tasks in string
    strMaintenanceTasks = ""
    for task in maintenance_options:
        if len(strMaintenanceTasks) == 0:
            strMaintenanceTasks += task
        else:
            strMaintenanceTasks += ", " + task
    strMaintenanceTasks = "(" + strMaintenanceTasks + ")"
    # Store resources in string
    strResources = ""
    for key in resources.keys():
        if len(strResources) == 0:
            strResources += key
        else:
            strResources += ", " + key
    strResources = "(" + strResources + ")"
    # Prompt user by asking what they want
    Maintenance_Complete = False
    while not Maintenance_Complete:
        User_Selection = input(f"What would you like to do? {strMaintenanceTasks}: ").lower()
        Task_Complete = False
        while not Task_Complete:
            if User_Selection in ["add", "remove"]:
                resource_selection = input(f"Select Resource: {strResources} or 'exit' to exit: ").lower()
                if resource_selection != "exit":
                    Unit_Amendment = float(input(f"How much do you wish to {User_Selection}: "))
                    AmendResources(resource_selection,User_Selection,Unit_Amendment)
                else:
                    Task_Complete = True
            elif User_Selection == "exit":
                Task_Complete=True
                Maintenance_Complete = True
                pass
            else:
                # Input a valid task
                print("Invalid task. Input a valid task.")
                pass


def Initialise_CoinInput():
    CoinList = list(coins.keys())
    CoinDict = {item: 0 for item in CoinList}
    return CoinDict


def check_resources(drink_choice):
    """Checks whether there are enough resources to make drink selection"""
    strMissingResources = ""
    for ingredient in MENU[drink_choice]["ingredients"]:
        if resources[ingredient] >= MENU[drink_choice]["ingredients"][ingredient]:
            # There's enough of strIngredient for drink
            pass
        else:
            if len(strMissingResources) == 0:
                strMissingResources = ingredient
            else:
                strMissingResources += ", " + ingredient
    if len(strMissingResources) == 0:
        return True
    else:
        print(f"Sorry there is not enough {strMissingResources}.")
        return False


def InsertCoins(CoinInput_dict, drink_choice, drink_cost):
    """Processes input coins and returns change if applicable"""
    MoneyInput = 0
    # Calculate total money inserted
    for coin in CoinInput_dict.keys():
        MoneyInput += coins[coin] * CoinInput_dict[coin]
    if MoneyInput >= drink_cost:
        # Enough money has been inserted
        resources["money"] += drink_cost
        # Return Change if any exists
        Change = MoneyInput - drink_cost
        RefundChange(Change)
        # Make Drink
        MakeDrink(drink_choice, drink_cost)

    else:
        # Not enough money has been inserted
        print("Sorry that's not enough money. Money refunded.")
        Change = MoneyInput


def RefundChange(change_amount):
    strChange = "${:,.2f}".format(change_amount)
    if change_amount > 0:
        print(f"Here is {strChange} in change.")


def MakeDrink(drink_choice, resources_dict):
    """Makes selected drink and depletes used resources"""
    for ingredient in MENU[drink_choice]["ingredients"]:
        resources[ingredient] -= MENU[drink_choice]["ingredients"][ingredient]
    print(f"Making your drink {DrumrollIcon}")
    print(f"Here is your {drink_choice} {DrinkIcon} Enjoy!")

def CoffeeMachineProgram():

    blnOperational = True

    while blnOperational:

        # Store Menu in string
        strMenu = ""
        for key in MENU.keys():
            if len(strMenu) == 0:
                strMenu += key
            else:
                strMenu += ", " + key
        strMenu = "(" + strMenu + ")"
        # Prompt user by asking what they want
        User_Selection = input(f"What would you like? {strMenu}: ").lower()
        # Process User_Action
        if User_Selection == "off":
            print("Coffee Machine powering down.")
            blnOperational = False
        elif User_Selection == "report":
            run_report()
        elif User_Selection == "maintenance":
            run_maintenance()
        elif User_Selection in list(MENU.keys()):
            # Check there are valid resources
            DrinkAvailable = check_resources(User_Selection)
            if DrinkAvailable:
                drink_cost = MENU[User_Selection]["cost"]
                strDrink_Cost = "${:,.2f}".format(drink_cost)
                print(f"{User_Selection} will cost {strDrink_Cost}.\nPlease insert coins.")
                CoinInput = Initialise_CoinInput()
                for coin in CoinInput.keys():
                    CoinInput[coin] = int(input(f"How many {coin}s: "))
                InsertCoins(CoinInput, User_Selection, drink_cost)
            else:
                # Drink not available
                pass


#Run Program
CoffeeMachineProgram()

