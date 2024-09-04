import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def authenticate_operator(people, first_name, last_name):
    for person in people:
        if person['first_name'] == first_name and person['last_name'] == last_name:
            return person
    return None

def get_residents_and_devices_by_unit(data, unit):
    residents = [person for person in data['people'] if person['unit'] == str(unit)]
    devices = {
        "thermostats": [device for device in data['devices']['thermostats'] if device['unit'] == unit],
        "lights": [device for device in data['devices']['lights'] if device['unit'] == unit],
        "locks": [device for device in data['devices']['locks'] if device['unit'] == unit]
    }
    return residents, devices

def move_in(data, first_name, last_name, unit):
    new_resident = {
        "first_name": first_name,
        "last_name": last_name,
        "unit": str(unit),
        "roles": ["Resident"]
    }
    data['people'].append(new_resident)
    return data

def move_out(data, first_name, last_name):
    data['people'] = [person for person in data['people'] if not (person['first_name'] == first_name and person['last_name'] == last_name)]
    return data

def main():
    data = load_json('property_data.json')

    # Step 1: Authenticate Operator
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")

    operator = authenticate_operator(data['people'], first_name, last_name)
    if not operator:
        print("Operator not found!")
        return

    # Step 2: Present options based on roles
    if "Admin" in operator['roles']:
        # Admin options
        print("""
        1. Move in a new resident
        2. Move out an old resident
        3. View all residents and devices in a unit
        4. Retrieve user information""")

        choice = int(input("Select an option: "))
        if choice == 1:
            first_name = input("Enter the first name: ")
            last_name = input("Enter the last name: ")
            unit = input("Enter the unit number: ")
            data = move_in(data, first_name, last_name, unit)
            save_json(data, 'property_data_changes.json')
        elif choice == 2:
            first_name = input("Enter the first name: ")
            last_name = input("Enter the last name")
            data = move_out(data, first_name, last_name)
            save_json(data, 'property_data_changes.json')
        elif choice == 3:
            unit = int(input("Enter the unit number: "))
            residents, devices = get_residents_and_devices_by_unit(data, unit)
            print("Residents:", residents)
            print("Devices:", devices)
        elif choice == 4:
            first_name = input("Enter the first name: ")
            last_name = input("Enter the last name: ")
            user = authenticate_operator(data['people'], first_name, last_name)
            print("User Info:", user)

    elif "Resident" in operator['roles']:
        # Resident options
        print("1. View my information")
        print("2. See devices associated with my unit")

        choice = int(input("Select an option: "))
        if choice == 1:
            print("Your Info:", operator)
        elif choice == 2:
            unit = operator['unit']
            residents, devices = get_residents_and_devices_by_unit(data, unit)
            print("Devices in your unit:", devices)

if __name__ == "__main__":
    main()
    
