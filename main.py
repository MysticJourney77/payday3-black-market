import requests
import json
import secrets
import string
import os
from dotenv import set_key, find_dotenv , load_dotenv


url_token = f"https://nebula.starbreeze.com/iam/v3/oauth/token"
string_length = 32
random_bytes = secrets.token_bytes(16)

random_string = ''.join(secrets.choice(string.hexdigits) for i in range(string_length))

def generate_random_hex_string(string_length):
    return ''.join(secrets.choice(string.hexdigits) for _ in range(string_length))

def create_data_dictionary():
    global configSlotEntitlementId
    global configSlotItemId
    global weaponInSlotEntitlementId
    global weaponInSlotAccelByteItemId

    weaponInSlotAccelByteItemId = generate_random_hex_string(string_length)
    weaponInSlotEntitlementId = generate_random_hex_string(string_length)
    configSlotEntitlementId = generate_random_hex_string(string_length)
    configSlotItemId = generate_random_hex_string(string_length)
    return

def get_valid_currencycode():
    while True:
        currency_custom = input("Enter currency: ").strip()
        if currency_custom.isalpha():
            return currency_custom.upper()
        else:
            print("Invalid input.") 

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"The file '{file_path}' does not exist.")

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    
def write_json_file(file_path, data):
    try:
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    
def append_to_json(json_filename, data_to_append):
    try:
        with open(json_filename, "a") as json_file:
            if os.path.getsize(json_filename) > 0:
                json_file.write(",\n")
            json.dump(data_to_append, json_file, indent=4)
    except Exception as e:
        print(f"Error appending data to {json_filename}: {e}")

def clear_json_file(filename):
    with open(filename, 'w') as file:
        file.truncate(0)
       
token_header = {
        "Host": "nebula.starbreeze.com",
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Basic MGIzYmZkZjVhMjVmNDUyZmJkMzNhMzYxMzNhMmRlYWI6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Electron/25.8.3 Safari/537.36",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US",
}
data_token = {
    "username": None,
    "password": None,
    "grant_type": "password",
    "client_id": random_string,
    "extend_exp": "true"
}

print("Login to Nebula")
load_dotenv(find_dotenv())
username = os.getenv("PD3USERNAME")
password = os.getenv("PD3PASSWORD")

if username and password:
    print("Autologin with the following credentials:")
    print(f"Username: {username}")
    masked_password = '*' * len(password)
    print(f"Password: {masked_password}")

    choice = input("Do you want to enter new login credentials? (y/n): ")
    if choice.lower() == 'y':
        username = None

else:
    print("No login credentials found.")
    choice = input("Do you want to enter new login credentials? (y/n): ")
    if choice.lower() == 'y':
        username = None
if not username:
    print("Please enter new login credentials:")
    username = input("Username: ")
    password = input("Password: ")
    set_key(".env", "PD3USERNAME", username)
    set_key(".env", "PD3PASSWORD", password)
    print("Login credentials have been saved.")

data_token["username"] = username
data_token["password"] = password
response_token_value = requests.post(url_token, headers=token_header, data=data_token)

while True:
    try:
        if response_token_value.status_code == 200:
            response_data = {
                "user_id": response_token_value.json().get("user_id", ""),
                "token": response_token_value.json().get("access_token", "")
            }
            break
        else:
            print("Invalid Login. Please enter a again.")
            exit(0)
    except ValueError:
        print("Invalid input.")


while True :
    print("Thanks for using Payday3 Black Market")
    write_json_file("response.json",response_data)
    print("Option - 1 : Buy C-Stacks")
    print("Option - 2 : Custom Buy")
    print("Option - 3 : Buy Heist Favors")
    print("Option - 4 : Import Customized Save Game")
    print("Option - 5 : Free Guns and Inventory Slots")
    print("Option - 6 : Buy Outfits")
    print("Option - 7 : Buy Paint Scheme")
    print("Option - 8 : Buy Inventory")
    print("Option - 9 : Buy Paint")
    print("Option - 0 : Exit")

    options = {
    0: "Option - 0 : Exit",    
    1: "Option - 1 : Buy C-Stacks",
    2: "Option - 2 : Custom Buy",
    3: "Option - 3 : Heist Favors",
    4: "Option - 4 : Save Data",
    5: "Option - 5 : Inventory",
    6: "Option - 6 : Dress",
    7: "Option - 7 : Paint Scheme",
    8: "Option - 8 : Inventory",
    9: "Option - 9 : Paint"
   }
    config_data = read_json_file("response.json")
    account_id = config_data.get("user_id", "")
    authorization_token = config_data.get("token", "")

    url = f"https://nebula.starbreeze.com/platform/public/namespaces/pd3/users/{account_id}/orders" 
    url_save_data = f"https://nebula.starbreeze.com/cloudsave/v1/namespaces/pd3/users/{account_id}/records/progressionsavegame"

    headers = {
    "Accept-Encoding": "deflate, gzip",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {authorization_token}",
    "Namespace": "pd3",
    "Game-Client-Version": "1.0.0.1",
    "AccelByte-SDK-Version": "21.0.3",
    "AccelByte-OSS-Version": "0.8.11",
    "User-Agent": "PAYDAY3/++UE4+Release-4.27-CL-0 Windows/10.0.19045.1.256.64bit",
   }
    data = {
    "itemId": None,  
    "quantity": 1,
    "price": None,
    "discountedPrice": None,
    "currencyCode": None,
    "region": "SE",
    "language": "en-US",
    "returnUrl": "http://127.0.0.1"
    }
    save_data_profile = read_json_file("modded_save_data.json")
    non_modded_save_data = read_json_file("non_modded_save_data.json")
    
    while True:
        try:
            choice = int(input("Enter the option: "))
            if choice in options:
                break
            else:
                print("Invalid choice. Please enter a valid option.")
        except ValueError:
            print("Invalid input. Please enter a valid option.")
    if choice == 0:
        break

    elif choice == 1:
        repeat_request_cstack = int(input("Enter the total number of times you want the request to send: "))
        for _ in range(repeat_request_cstack):
            data["itemId"] = "dd693796e4fb4e438971b65eecf6b4b7"
            data["price"] = 90000
            data["discountedPrice"] = 90000
            data["currencyCode"] = "CASH"
            response = requests.post(url, json=data, headers=headers)
            print(f"C-Stacks Bought successfully - {_ + 1}")
        delete_file("response.json")

    elif choice == 2:
        item_id_custom = input("Enter itemID: ")
        price_custom = int(input("Enter price: "))
        discounted_custom = int(input("Enter discountedprice: "))
        currency_custom = get_valid_currencycode()
        data["itemId"] = item_id_custom
        data["price"] = price_custom
        data["discountedPrice"] = discounted_custom
        data["currencyCode"] = currency_custom
        repeat_request_custom = int(input("Enter the total number of times you want the request to send: "))  
        for _ in range(repeat_request_custom):
            response = requests.post(url, json=data, headers=headers)
            print(f"Custom Item Purchased - {_ + 1}")
        delete_file("response.json")

    elif choice == 3:
        item_id_json = read_json_file("Payday3_offsets.json")
        heistfav = item_id_json["Heistfav"]
        heist_list = []
        counter = 1
        for heist_group in heistfav:
            for heist_alias, heist_data in heist_group.items():
                for heist_info in heist_data:
                    print("\n" f"{heist_alias}: ")
                    for key, value in heist_info.items():
                        print(f"{counter}. {key}: {value["price"]}$")
                        heist_list.append((key,value))
                        counter += 1
        print()
        heist_added_inv = []
        while True:
            print("Enter 0 to Exit!")
            print("Enter 40 to buy all")
            selection = int(input("Enter the number of the item you want to select: "))
            if selection == 0:
                break
            elif 1 <= selection <= counter:
                heist_add = heist_list[selection - 1]
                heist_added_inv.append(heist_add)
                print(f"Added {heist_add[0]} to cart")
            elif selection == 40:
                repeat_request_heistfav_1 = int(input("Enter the total number of times you want the request to send: "))
                for item_name, item_data in heist_list:
                    item_id = item_data['itemId']
                    price = item_data['price']
                    for _ in range(repeat_request_heistfav_1):
                        data["itemId"] = item_id
                        data["price"] = price
                        data["discountedPrice"] = price
                        data["currencyCode"] = "CASH"
                        response = requests.post(url, json=data, headers=headers)
                    print(f"Item Purchased")
                        
            else:
                print("Invalid selection. Please choose a valid number.")
        repeat_request_heistfav_2 = int(input("Enter the total number of times you want the request to send: "))
        for _ in range(repeat_request_heistfav_2):
            for heist_add in heist_added_inv:
                heist_id = heist_added_inv[0]
                heist_details = heist_id[1]
                item_id = heist_details['itemId']
                data["itemId"] = heist_id[1]['itemId']
                data["price"] = heist_id[1]["price"]
                data["discountedPrice"] = heist_id[1]["price"]
                data["currencyCode"] = "CASH"
                response = requests.post(url, json=data, headers=headers)
                print(f"Item Purchased = {heist_add[0]}")
        delete_file("response.json")

    elif choice == 4:
        print("1. Modded Save")
        print("2. Non Modded Save")
        save = int(input("Enter the option: "))
        if save == 1:
            response = requests.post(url_save_data, json=save_data_profile, headers=headers)
            print("Modded Save loaded!")
        elif save == 2:
            response = requests.post(url_save_data, json=non_modded_save_data, headers=headers)
            print("Non Modded Save loaded!")
        else:
            print("Invalid Input")
            continue

    elif choice == 5:
        delete_file("response.json")
        print("Choose the data to generate:")
        print("1. Guns")
        print("2. Inventory")
        options_select = int(input("Enter the Option: "))
        if options_select == 1:
            delete_file("response.json")
            json_filename_weapons = "weapons.json"
            clear_json_file(json_filename_weapons)
            item_id_json = read_json_file("Payday3_offsets.json")
            weapons = item_id_json["weapons"]
            weapon_list = []
            counter = 1
            for weapon_group in weapons:
                for weapon_alias, weapon_data in weapon_group.items():
                    for weapon_info in weapon_data:
                        print(f"{counter}. {weapon_alias}")
                        weapon_list.append((weapon_alias, weapon_info))
                        counter += 1
            selected_weapons = [] 
            while True:
                print("Enter 0 to Exit!")
                weapon_select = int(input("Enter the number of the item you want to select: "))
                if weapon_select == 0:
                    break  
                elif 1 <= weapon_select <= counter:
                    selected_weapon = weapon_list[weapon_select - 1]
                    selected_weapons.append(selected_weapon)
                    print(f"Added {selected_weapon[0]} to Cart.")
                else:
                    print("Invalid selection. Please choose a valid option.")
            for selected_weapon in selected_weapons:
                create_data_dictionary()
                data = read_json_file("Payday3_offsets.json")
                primary_weapons = data["Inventory"][1]["weapon_slot"][0]
                primary_weapons["weaponInSlotAccelByteItemSku"] = selected_weapon[1]["weaponInSlotAccelByteItemSku"]
                data["Inventory"][1]["weapon_slot"][0]["weaponConfigInventorySlot"]["equippableConfig"]["equippableData"] = selected_weapon[1]["equippableData"]
                primary_weapons["itemInventorySlotAvailability"] = selected_weapon[1]["itemInventorySlotAvailability"]
                primary_weapons["weaponInSlotEntitlementId"] = weaponInSlotEntitlementId
                primary_weapons["weaponInSlotAccelByteItemId"] = weaponInSlotAccelByteItemId
                primary_weapons["configSlotEntitlementId"] = configSlotEntitlementId
                primary_weapons["configSlotItemId"] = configSlotItemId

                append_to_json("weapons.json" , primary_weapons)
                print(f"Added {selected_weapon[0]} to the Weapons.json file.")
            print("Finished selecting and appending weapons.")
        elif options_select == 2:
            print("1. Weapon Inventory")
            print("2. Mask Inventory")
            print("3. Suite Inventory")
            print("4. Gloves Inventory")
            inventory = int(input("Enter the number: "))
            json_filename_inv = "inventory_slot.json"
            clear_json_file(json_filename_inv)
            repeat_request_inventory = int(input("Enter the total number of times you want the request to send: "))  

            if inventory == 1:
                data = read_json_file("Payday3_offsets.json")
                for _ in range(repeat_request_inventory):
                    create_data_dictionary()
                    weapon_slot = data["Inventory"][1]["weapon_slot"][0]
                    weapon_slot["weaponInSlotEntitlementId"] = weaponInSlotEntitlementId
                    weapon_slot["weaponInSlotAccelByteItemId"] = weaponInSlotAccelByteItemId
                    weapon_slot["configSlotEntitlementId"] = configSlotEntitlementId
                    weapon_slot["configSlotItemId"] = configSlotItemId

                    append_to_json("inventory_slot.json", weapon_slot)
                print("Weapons slot added to inventory_slot.json")

            elif inventory == 2:
                data = read_json_file("Payday3_offsets.json")
                for _ in range(repeat_request_inventory):
                    create_data_dictionary()
                    mask_slot = data["Inventory"][2]["mask_slot"][0]
                    mask_slot["maskInSlotEntitlementId"] = weaponInSlotEntitlementId
                    mask_slot["maskInSlotAccelByteItemId"] = weaponInSlotAccelByteItemId
                    mask_slot["configSlotEntitlementId"] = configSlotEntitlementId
                    mask_slot["configSlotItemId"] = configSlotItemId

                    append_to_json("inventory_slot.json", mask_slot)
                print("Mask slot added to inventory_slot.json")
            elif inventory == 3:
                with open('Payday3_offsets.json', 'r') as json_file:
                    data = json.load(json_file)
                for _ in range(repeat_request_inventory):
                    create_data_dictionary()
                    suit_data = data["Inventory"][0]["suit"][0]
                    suit_data["suitInSlotEntitlementId"] = weaponInSlotEntitlementId
                    suit_data["suitInSlotAccelByteItemId"] = weaponInSlotAccelByteItemId
                    suit_data["configSlotEntitlementId"] = configSlotEntitlementId
                    suit_data["configSlotItemId"] = configSlotItemId

                    append_to_json("inventory_slot.json", suit_data)
                print("Suit slot added to inventory_slot.json")
            elif inventory == 4:
                with open('Payday3_offsets.json', 'r') as json_file:
                    data = json.load(json_file)
                for _ in range(repeat_request_inventory):
                    create_data_dictionary()
                    gloves_slot = data["Inventory"][3]["glove_slot"][0]
                    gloves_slot["configSlotEntitlementId"] = configSlotEntitlementId
                    gloves_slot["configSlotItemId"] = configSlotItemId

                    append_to_json("inventory_slot.json", gloves_slot)
                print("Gloves slot added to inventory_slot.json")
        else:
            print("Invalid Input")
            continue

    elif choice == 6:
        item_id_json = read_json_file("Payday3_offsets.json")
        suite = item_id_json["Suits"]
        suite_list = []
        counter = 1
        for suite_group in suite:
            for suite_alias, suite_data in suite_group.items():
                for suite_info in suite_data:
                    print("\n" f"{suite_alias}: ")
                    for key, value in suite_info.items():
                        print(f"{counter}. {key}: {value["price"]}$")
                        suite_list.append((key, value))
                        counter += 1                        
        print()
        suit_added_inv = []
        while True:
            print("Enter 0 to Exit!")
            suite_select = int(input("Enter the number of suite to purchase: "))
            if suite_select == 0:
                break
            elif 1 <= suite_select <= counter:
                newsuite_add = suite_list[suite_select - 1]
                suit_added_inv.append(newsuite_add)
                print(f"Added {newsuite_add[0]} to Cart.")
            else:
                print("Invalid selection. Please choose a valid option.")

        for newsuite_add in suit_added_inv:
            suit_id = suit_added_inv[0]
            suite_details = suit_id[1]
            item_id = suite_details['id']
            data["itemId"] = suit_id[1]["id"]
            data["price"] = suit_id[1]["price"]
            data["discountedPrice"] = suit_id[1]["price"]
            data["currencyCode"] = "CASH"
            response = requests.post(url, json=data, headers=headers)
            print(f"Item Bought Successfully - {newsuite_add[0]}")
    
    elif choice  == 7:
        item_id_json = read_json_file("Payday3_offsets.json")
        weapon_paint = item_id_json["Weapon Paint Schemes"]
        weapon_paint_list = []
        counter = 1
        for weapon_paint_info in weapon_paint:
            for key, value in weapon_paint_info.items():
                print(f"{counter}. {key}: {value['price']}$")
                weapon_paint_list.append((key, value))
                counter += 1
        print()
        weapon_paint_inv = []
        while True:
            print("Enter 0 to Exit!")
            weapon_paint_select = int(input("Enter the number of paint to purchase: "))
            if weapon_paint_select == 0:
                break
            elif 1 <= weapon_paint_select <= counter:
                weapon_paint_add = weapon_paint_list[weapon_paint_select - 1]
                weapon_paint_inv.append(weapon_paint_add)
                print(f"Added {weapon_paint_add[0]} to Cart.")
            else:
                print("Invalid selection. Please choose a valid option.")
        for weapon_paint_add in weapon_paint_inv:
            paint_id = weapon_paint_inv[0]
            paint_details = paint_id[1]
            item_id = paint_details["itemId"]
            data["itemId"] = paint_id[1]["itemId"]
            data["price"] = paint_id[1]["price"]
            data["discountedPrice"] = paint_id[1]["price"]
            data["currencyCode"] = paint_id[1]["currency"]
            response = requests.post(url, json=data, headers=headers)
            print(response.content.decode('utf-8'))
            print(f"Item Bought Successfully - {weapon_paint_add[0]}")

    elif choice == 8:
        item_id_json = read_json_file("Payday3_offsets.json")
        inventory_slots = item_id_json["Inventory Slots"]
        inventory_slots_list = []
        counter = 1
        for inventory_slots_info in inventory_slots:
            for key, value in inventory_slots_info.items():
                print(f"{counter}. {key}: {value["price"]}$")
                inventory_slots_list.append((key, value))
                counter += 1
        print()
        inventory_slots_inv = []
        while True:
            print("Enter 0 to Exit!")
            inventory_slots_select = int(input("Enter the number of paint to purchase: "))
            if inventory_slots_select == 0:
                break
            elif 1<= inventory_slots_select <= counter:
                inventory_slots_add = inventory_slots_list[inventory_slots_select - 1]
                inventory_slots_inv.append(inventory_slots_add)
                print(f"Added {inventory_slots_add[0]} to Cart.")
            else:
                print("Invalid selection. Please choose a valid option.")
        inputuser_inventory = int(input("Enter the total number of times you want the request to send: "))
        for _ in range(inputuser_inventory):
            for inventory_slots_add in inventory_slots_inv:
                inventory_id = inventory_slots_inv[0]
                inventory_details = inventory_id[1]
                item_id = inventory_details["itemId"]
                data["itemId"] = inventory_id[1]["itemId"]
                data["price"] = inventory_id[1]["price"]
                data["discountedPrice"] = inventory_id[1]["price"]
                data["currencyCode"] = inventory_id[1]["currency"]
                response = requests.post(url, json=data, headers=headers)
                print(f"Item Bought Successfully - {inventory_slots_add[0]} {_ + 1}")

    elif choice == 9:
        item_id_json = read_json_file("Payday3_offsets.json")
        color_paint = item_id_json["Paint Schemes_All"]
        color_list = []
        counter = 1
        for color_group in color_paint:
            for color_alias, color_data in color_group.items():
                for color_info in color_data:
                    name = color_info["name"]
                    itemId = color_info["itemId"]
                    price = color_info["price"]
                    print(f"{counter}. {name}  : {price}$")
                    color_list.append((name, itemId, price))
                    counter += 1
        print()
        color_added_inv = []
        while True:
            print("Enter 0 to Exit!")
            colorselect = int(input("Enter the number of the item you want to select: "))
            if colorselect == 0:
                break
            elif 1 <= colorselect <= counter:
                color_add = color_list[colorselect - 1]
                color_added_inv.append(color_add)
                print(f"Added {color_add[0]} to cart")
            else:
                print("Invalid selection. Please choose a valid number.")
        repeat_request_paint = int(input("Enter the total number of times you want the request to send: "))
        for _ in range(repeat_request_paint):
                for color_add in color_added_inv:
                    color_id = color_added_inv[0]
                    color_details = color_id[1]
                    item_id = color_details["itemId"]
                    data["itemId"] = color_id[1]['itemId']
                    data["price"] = color_id[1]["price"]
                    data["discountedPrice"] = color_id[1]["price"]
                    data["currencyCode"] = color_id[1]["currency"]
                    response = requests.post(url, json=data, headers=headers)
                    print(f"Item Purchased = {color_add[0]}")