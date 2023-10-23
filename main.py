import requests
import json
import secrets
import string
import os


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

print("Login to Nebula Account")

username_request = input("Enter your EmailID: ")
password_request = input("Enter the Password: ")
data_token["username"] = username_request
data_token["password"] = password_request
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

with open("response.json", "w") as json_file:
    json.dump(response_data, json_file, indent=4)
print("Option - 1 : Buy C-Stacks")
print("Option - 2 : Custom Buy")
print("Option - 3 : Heist Favors")
print("Option - 4 : Import Customized Save Game")
print("Option - 5 : Free Inventory Slots")

options = {
    1: "Option - 1 : Buy C-Stacks",
    2: "Option - 2 : Custom Buy",
    3: "Option - 3 : Heist Favors",
    4: "Option - 4 : Modded Save",
    5: "Option - 5 : Free Inventory"
}
with open("response.json", "r") as config_file:
   config_data = json.load(config_file)
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
    "Game-Client-Version": "1.0.0.0",
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
weapon_slot = {
        "weaponInSlotEntitlementId": None,
        "weaponInSlotAccelByteItemId": None,
        "weaponInSlotAccelByteItemSku": "",
        "weaponInventorySlotType": "Configurable",
        "weaponConfigInventorySlot": {
            "equippableConfig": {
                "equippableData": "None",
                "modDataMap": {}
            },
            "payedWeaponPartAttachmentItemIdArray": []
        },
        "weaponPresetConfigInventorySlot": {
            "weaponPresetConfigData": "None"
        },
        "itemInventorySlotAvailability": "Available",
        "configSlotEntitlementId": None,
        "configSlotItemId": None
}

mask_slot = {
        "maskInSlotEntitlementId": None,
        "maskInSlotAccelByteItemId": None,
        "maskInventorySlotType": "Configurable",
        "maskConfig": {
            "maskData": "None",
            "modDataMap": {}
        },
        "maskPresetConfig": {
            "maskPresetData": "None"
        },
        "itemInventorySlotAvailability": "Available",
        "configSlotEntitlementId": None,
        "configSlotItemId": None
}

suit_slot = {
        "suitInSlotEntitlementId": None,
        "suitInSlotAccelByteItemId": None,
        "suitInventorySlotType": "Configurable",
        "suitConfig": {
            "suitData": "None",
            "suitBaseData": "None",
            "modDataMapArray": [
                {
                    "modDataMap": {}
                },
                {
                    "modDataMap": {}
                },
                {
                    "modDataMap": {}
                }
            ]
        },
        "suitPresetConfig": {
            "suitPresetData": "None"
        },
        "itemInventorySlotAvailability": "Available",
        "configSlotEntitlementId": None,
        "configSlotItemId": None
}

gloves_slot = {
        "gloveInSlotEntitlementId": "683E9A4127474014BFAF98464E1A865F",
        "gloveInSlotAccelByteItemId": "638BF75BA8394A508E05B52117ECEEE4",
        "gloveData": "None",
        "itemInventorySlotAvailability": "Available",
        "configSlotEntitlementId": None,
        "configSlotItemId": None
}

with open('modded_save_data.json', 'r') as json_file:
    request_headers_data = json.load(json_file)
sava_data_profile = request_headers_data

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"The file '{file_path}' does not exist.")

def get_valid_currencycode():

    while True:
        currency_custom = input("Enter currency: ").strip()
        if currency_custom.isalpha():
            return currency_custom.upper()
        else:
            print("Invalid input.")            
while True:
    try:
        choice = int(input("Enter the option: "))
        if choice in options:
            break
        else:
            print("Invalid choice. Please enter a valid option.")
    except ValueError:
        print("Invalid input. Please enter a valid option.")

if choice == 1:
    repeat_request = int(input("Enter the total number of times you want the request to send: "))  
    for _ in range(repeat_request):
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
        repeat_request = int(input("Enter the total number of times you want the request to send: "))  
        for _ in range(repeat_request):
            response = requests.post(url, json=data, headers=headers)
            print(f"Custom Item Purchased - {_ + 1}")
        delete_file("response.json") 

elif choice == 3:
    with open('Payday3_offsets.json', 'r') as json_file:
        item_id_json = json.load(json_file)
        all_items = [item for group in item_id_json["groups"] for item in group["items"]]

        counter = 1
        for group in item_id_json["groups"]:
            print(f"{group['name']}:")
            for item in group["items"]:
                print(f"{counter}. {item['alias']} | {item['itemId']} | 1000")  # You can modify this format as needed
                counter += 1
            print()
        print("Select 0 to buy All")
        selection = int(input("Enter the number of the item you want to select: "))
        repeat_request = int(input("Enter the total number of times you want the request to send: "))  
        for _ in range(repeat_request):
            if selection == 0:
                for item in all_items:
                    if item['itemId'] == "65a355215bb8473bbf9d3f2661211899":
                        data["itemId"] = item['itemId']
                        data["price"] = 1999
                        data["discountedPrice"] = 1999
                        data["currencyCode"] = "CASH"
                        print(f"Item Purchased = {item['alias']}")
                        response = requests.post(url, json=data, headers=headers)
                        #print(response.content.decode('utf-8'))                                    
                    else:
                        data["itemId"] = item['itemId']
                        data["price"] = 1000
                        data["discountedPrice"] = 1000
                        data["currencyCode"] = "CASH"
                        print(f"Item Purchased = {item['alias']}")
                        response = requests.post(url, json=data, headers=headers)
                        #print(response.content.decode('utf-8'))
            elif 1 <= selection <= len(all_items):
                selected_item = all_items[selection - 1]
                print(f"Selected Item ID: {selected_item['itemId']}")
                data["itemId"] = selected_item['itemId']  # Assign the selected item's ID
                data["price"] = 1000
                data["discountedPrice"] = 1000
                data["currencyCode"] = "CASH"
                print(f"Item Purchased = {item['alias']}")
                response = requests.post(url, json=data, headers=headers)
                #print(response.content.decode('utf-8'))
            else:
                print("Invalid selection. Please choose a valid number.")
        delete_file(response.json) 

elif choice == 4:
    response = requests.post(url_save_data, json=sava_data_profile, headers=headers)
    #with open('response_save_data.txt', 'w') as text_file:
        #text_file.write(response.text)
    print("Modded Save loaded!")
    delete_file("response.json") 
elif choice == 5:
    delete_file("response.json")
    print("Choose the data to generate:")
    print("1. Weapon Inventory")
    print("2. Mask Inventory")
    print("3. Suite Inventory")
    print("4. Gloves Inventory")

    inventory = int(input("Enter the number: "))
    json_filename = "inventory_slot.json"
    with open(json_filename, "w") as json_file:
        json_file.write("")

    repeat_request = int(input("Enter the total number of times you want the request to send: "))  

    if inventory == 1:
        for _ in range(repeat_request):
            create_data_dictionary()
            weapon_slot["weaponInSlotEntitlementId"] = weaponInSlotEntitlementId
            weapon_slot["weaponInSlotAccelByteItemId"] = weaponInSlotAccelByteItemId
            weapon_slot["configSlotEntitlementId"] = configSlotEntitlementId
            weapon_slot["configSlotItemId"] = configSlotItemId

            with open(json_filename, "a") as json_file:
               json.dump(weapon_slot, json_file, indent=2)
               json_file.write(",\n")

    elif inventory == 2:
        for _ in range(repeat_request):
            create_data_dictionary()
            mask_slot["maskInSlotEntitlementId"] = weaponInSlotEntitlementId
            mask_slot["maskInSlotAccelByteItemId"] = weaponInSlotAccelByteItemId
            mask_slot["configSlotEntitlementId"] = configSlotEntitlementId
            mask_slot["configSlotItemId"] = configSlotItemId

            with open(json_filename, "a") as json_file:
                json.dump(mask_slot, json_file, indent=2)
                json_file.write(",\n")
    elif inventory == 3:
        for _ in range(repeat_request):
            create_data_dictionary()
            suit_slot["suitInSlotEntitlementId"] = weaponInSlotEntitlementId
            suit_slot["suitInSlotAccelByteItemId"] = weaponInSlotAccelByteItemId
            suit_slot["configSlotEntitlementId"] = configSlotEntitlementId
            suit_slot["configSlotItemId"] = configSlotItemId

            with open(json_filename, "a") as json_file:
                json.dump(suit_slot, json_file, indent=2)
                json_file.write(",\n")
    elif inventory == 4:
        for _ in range(repeat_request):
            create_data_dictionary()
            gloves_slot["configSlotEntitlementId"] = configSlotEntitlementId
            gloves_slot["configSlotItemId"] = configSlotItemId

            with open(json_filename, "a") as json_file:
                json.dump(gloves_slot, json_file, indent=2)
                json_file.write(",\n")