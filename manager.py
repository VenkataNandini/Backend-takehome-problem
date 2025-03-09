import csv
import os
import json
from datetime import datetime, timedelta


def read_contacts_from_csv(filename="contacts.csv"):
    contacts = []

    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                contact = unflatten_contact(row)
                contacts.append(contact)
    except FileNotFoundError:
        print(f"No such file: {filename}")
    except Exception as e:
        print(f"Error reading file: {e}")

    return contacts


def write_contacts_to_csv(contacts, filename="contacts.csv"):
    if not contacts:
        return

    fieldnames = [
        "name",
        "mobile_phone",
        "group",
        "company_name",
        "company_occupation",
        "company_address",
        "company_web_page",
        "other_phones_mobile_phone_2",
        "other_phones_mobile_phone_3",
        "other_phones_home_phone",
        "other_phones_office_phone",
        "emails_private_email_1",
        "emails_private_email_2",
        "emails_office_email",
        "melody",
        "other_address",
        "other_birth_day",
        "other_notes",
        "other_spouse_name",
        "other_spouse_birthday",
        "other_spouse_notes",
        "other_children",
    ]

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for contact in contacts:
                flattened_contact = flatten_contact(contact)
                writer.writerow(flattened_contact)
            csvfile.flush()
    except Exception as e:
        print(f"Error writing to file: {e}")


def flatten_contact(contact):
    flattened_contact = {
        "name": contact["name"],
        "mobile_phone": contact["mobile_phone"],
        "group": contact["group"],
        "company_name": contact["company"]["name"],
        "company_occupation": contact["company"]["occupation"],
        "company_address": contact["company"]["address"],
        "company_web_page": contact["company"]["web_page"],
        "other_phones_mobile_phone_2": contact["other_phones"]["mobile_phone_2"],
        "other_phones_mobile_phone_3": contact["other_phones"]["mobile_phone_3"],
        "other_phones_home_phone": contact["other_phones"]["home_phone"],
        "other_phones_office_phone": contact["other_phones"]["office_phone"],
        "emails_private_email_1": contact["emails"]["private_email_1"],
        "emails_private_email_2": contact["emails"]["private_email_2"],
        "emails_office_email": contact["emails"]["office_email"],
        "melody": contact["melody"],
        "other_address": contact["other"]["address"],
        "other_birth_day": contact["other"]["birth_day"],
        "other_notes": contact["other"]["notes"],
        "other_spouse_name": contact["other"]["spouse"]["name"],
        "other_spouse_birthday": contact["other"]["spouse"]["birthday"],
        "other_spouse_notes": contact["other"]["spouse"]["notes"],
        "other_children": contact["other"]["children"],
    }
    return flattened_contact


def unflatten_contact(flat_contact):
    contact = {
        "name": flat_contact["name"],
        "mobile_phone": flat_contact["mobile_phone"],
        "group": flat_contact["group"],
        "company": {
            "name": flat_contact["company_name"],
            "occupation": flat_contact["company_occupation"],
            "address": flat_contact["company_address"],
            "web_page": flat_contact["company_web_page"],
        },
        "other_phones": {
            "mobile_phone_2": flat_contact["other_phones_mobile_phone_2"],
            "mobile_phone_3": flat_contact["other_phones_mobile_phone_3"],
            "home_phone": flat_contact["other_phones_home_phone"],
            "office_phone": flat_contact["other_phones_office_phone"],
        },
        "emails": {
            "private_email_1": flat_contact["emails_private_email_1"],
            "private_email_2": flat_contact["emails_private_email_2"],
            "office_email": flat_contact["emails_office_email"],
        },
        "melody": flat_contact["melody"],
        "other": {
            "address": flat_contact["other_address"],
            "birth_day": flat_contact["other_birth_day"],
            "notes": flat_contact["other_notes"],
            "spouse": {
                "name": flat_contact["other_spouse_name"],
                "birthday": flat_contact["other_spouse_birthday"],
                "notes": flat_contact["other_spouse_notes"],
            },
            "children": json.loads(flat_contact["other_children"]),
        },
    }
    return contact


def read_from_file(filename):
    data = []

    if not os.path.exists(filename):
        return data

    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            for line in file.readlines():
                name, count = line.strip().split(",")
                data.append({"name": name, "count": int(count)})
    except Exception as e:
        print(f"Error reading from file: {e}")

    return data


def write_to_file(data, filename):
    try:
        with open(filename, mode="w", encoding="utf-8") as file:
            for item in data:
                file.write(f"{item['name']},{item['count']}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")


def add_melody(melodies):
    print("Current melodies:")
    if not melodies:
        print("No melodies available.")
    else:
        for index, melody in enumerate(melodies):
            print(f"{index + 1}. {melody['name']}")

    try:
        melody_name = input(
            "Enter the name of the new melody (or press Enter to return to the main menu): "
        )
        if melody_name == "":
            print("Returning to main menu.")
        else:
            melodies.append({"name": melody_name, "count": 0})
            write_to_file(melodies, "melodies.txt")
            print(f"Melody '{melody_name}' has been added.")
    except EOFError:
        print("Unexpected input error. Please try again.")

    return melodies


def show_melodies(melodies):
    print("\nMelodies:")
    for index, melody in enumerate(melodies):
        print(f"{index + 1}. {melody['name']} (used by {melody['count']} contact(s))")
    print("\nPress Enter to return to the main menu.")

    while True:
        try:
            user_input = input()
            if user_input == "":
                break
            else:
                print("Please press Enter to return to the main menu.")
        except EOFError:
            print(
                "Unexpected input error. Please press Enter to return to the main menu."
            )


def delete_melody(melodies):
    print("Available melodies:")
    if not melodies:
        print("No melodies available.")
    else:
        for index, melody in enumerate(melodies):
            print(f"{index + 1}. {melody['name']}")

        valid_input = False
        while not valid_input:
            try:
                melody_index = (
                    int(
                        input(
                            "Enter the number of the melody you want to delete (or enter '0' to return to the main menu): "
                        )
                    )
                    - 1
                )
                if melody_index == -1:
                    print("Returning to main menu.")
                    return melodies
                elif 0 <= melody_index < len(melodies):
                    valid_input = True
                else:
                    print(
                        "Invalid input. Please enter a number corresponding to an available melody."
                    )
            except ValueError:
                print("Invalid input. Please enter a valid number.")
            except EOFError:
                print("Unexpected input error. Please try again.")

        melody = melodies[melody_index]

        if melody["count"] == 0:
            melodies.pop(melody_index)
            write_to_file(melodies, "melodies.txt")
            print(f"Melody '{melody['name']}' has been deleted.")
        else:
            print(
                f"Cannot delete melody '{melody['name']}'. {melody['count']} contact(s) are using it."
            )
    return melodies


def add_group(groups):
    print("Current groups:")
    if not groups:
        print("No groups available.")
    else:
        for index, group in enumerate(groups):
            print(f"{index + 1}. {group['name']}")

    try:
        group_name = input(
            "Enter the name of the new group (or press Enter to return to the main menu): "
        )
        if group_name == "":
            print("Returning to main menu.")
        else:
            groups.append({"name": group_name, "count": 0})
            write_to_file(groups, "groups.txt")
            print(f"Group '{group_name}' has been added.")
    except EOFError:
        print("Unexpected input error. Please try again.")

    return groups


def show_groups(groups):
    print("\nGroups:")
    for index, group in enumerate(groups):
        print(f"{index + 1}. {group['name']} (contains {group['count']} contact(s))")
    print("\nPress Enter to return to the main menu.")

    while True:
        try:
            user_input = input()
            if user_input == "":
                break
            else:
                print("Please press Enter to return to the main menu.")
        except EOFError:
            print(
                "Unexpected input error. Please press Enter to return to the main menu."
            )


def delete_group(groups):
    print("Available groups:")
    if not groups:
        print("No groups available.")
    else:
        for index, group in enumerate(groups):
            print(f"{index + 1}. {group['name']}")

        valid_input = False
        while not valid_input:
            try:
                group_index = (
                    int(
                        input(
                            "Enter the number of the group you want to delete (or enter '0' to return to the main menu): "
                        )
                    )
                    - 1
                )
                if group_index == -1:
                    print("Returning to main menu.")
                    return melodies
                elif 0 <= group_index < len(groups):
                    valid_input = True
                else:
                    print(
                        "Invalid input. Please enter a number corresponding to an available group."
                    )
            except ValueError:
                print("Invalid input. Please enter a valid number.")
            except EOFError:
                print("Unexpected input error. Please try again.")

        group = groups[group_index]

        if group["count"] == 0:
            groups.pop(group_index)
            write_to_file(groups, "groups.txt")
            print(f"Group '{group['name']}' has been deleted.")
        else:
            print(
                f"Cannot delete group '{group['name']}'. {group['count']} contact(s) are in it."
            )
    return groups


def main():
    contacts = read_contacts_from_csv()
    melodies = read_from_file("melodies.txt")
    groups = read_from_file("groups.txt")

    while True:
        try:
            print_menu()
            user_input = input("Please enter the number of your choice (0 to exit): ")

            if user_input == "0":
                print("Exiting the program.")
                break
            elif user_input == "1":
                contacts, groups, melodies = add_contact(contacts, groups, melodies)
                write_to_file(groups, "groups.txt")
                write_to_file(melodies, "melodies.txt")
                write_contacts_to_csv(contacts)
            elif user_input == "2":
                contacts, groups, melodies = update_contact(contacts, groups, melodies)
                write_to_file(groups, "groups.txt")
                write_to_file(melodies, "melodies.txt")
                write_contacts_to_csv(contacts)
            elif user_input == "3":
                contacts = delete_contact(contacts)
                write_contacts_to_csv(contacts)
            elif user_input == "4":
                search_contact(contacts)
            elif user_input == "5":
                groups = add_group(groups)
            elif user_input == "6":
                show_groups(groups)
            elif user_input == "7":
                groups = delete_group(groups)
            elif user_input == "8":
                contacts, groups = manage_group_subscription(contacts, groups)
                write_contacts_to_csv(contacts)
                write_to_file(groups, "groups.txt")
            elif user_input == "9":
                manage_birthday_reminders(contacts)
            elif user_input == "10":
                print_contact_list(contacts)
            elif user_input == "11":
                print_contact_details(contacts)
            elif user_input == "12":
                melodies = add_melody(melodies)
            elif user_input == "13":
                show_melodies(melodies)
            elif user_input == "14":
                melodies = delete_melody(melodies)
            else:
                print("Invalid input. Please enter a number between 0 and 14.")
        except Exception as e:
            print(f"Error: {e}")
            continue


def print_menu():
    print("\nContact Book Manager Menu")
    print("1. Add a new contact")
    print("2. Update contact details")
    print("3. Delete a contact")
    print("4. Search for a contact")
    print("5. Create a contact group")
    print("6. Show all contact groups")
    print("7. Delete a contact groups")
    print("8. Manage group subscriptions")
    print("9. Manage birthday reminders")
    print("10. Print contact list")
    print("11. Print contact")
    print("12. Add a melody")
    print("13. Show melodies")
    print("14. Delete a melody")
    print("0. Exit the program")


def create_contact(
    name,
    mobile_phone,
    group=None,
    company={},
    other_phones={},
    emails={},
    melody={},
    other={},
):
    contact = {
        "name": name,
        "mobile_phone": mobile_phone,
        "group": group,
        "company": {
            "name": company.get("name", None),
            "occupation": company.get("occupation", None),
            "address": company.get("address", None),
            "web_page": company.get("web_page", None),
        },
        "other_phones": {
            "mobile_phone_2": other_phones.get("mobile_phone_2", None),
            "mobile_phone_3": other_phones.get("mobile_phone_3", None),
            "home_phone": other_phones.get("home_phone", None),
            "office_phone": other_phones.get("office_phone", None),
        },
        "emails": {
            "private_email_1": emails.get("private_email_1", None) if emails else None,
            "private_email_2": emails.get("private_email_2", None) if emails else None,
            "office_email": emails.get("office_email", None) if emails else None,
        },
        "melody": melody,
        "other": {
            "address": other.get("address", None) if other else None,
            "birth_day": other.get("birth_day", None) if other else None,
            "notes": other.get("notes", None) if other else None,
            "spouse": {
                "name": other.get("spouse", {}).get("name", None),
                "birthday": other.get("spouse", {}).get("birthday", None),
                "notes": other.get("spouse", {}).get("notes", None),
            },
            "children": other.get("children", {}),
        },
    }
    return contact


def input_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ["y", "n"]:
            return answer
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")


def add_contact(contacts, groups, melodies):
    print("Adding a new contact.")
    name = input("Enter name: ")
    mobile_phone = input("Enter mobile phone: ")

    group = None
    if (
        groups
        and input_yes_no("Do you want to add the contact to a group? (y/n): ") == "y"
    ):
        print("Available groups:")
        for index, group_item in enumerate(groups):
            print(f"{index + 1}. {group_item['name']}")
        group_index = int(input("Enter the number of the desired group: ")) - 1
        group = groups[group_index]["name"]
        groups[group_index]["count"] += 1

    melody = "default"
    if melodies and input_yes_no("Do you want to add a melody? (y/n): ") == "y":
        print("Available melodies:")
        for index, melody_item in enumerate(melodies):
            print(f"{index + 1}. {melody_item['name']}")
        melody_index = int(input("Enter the number of the desired melody: ")) - 1
        melody = melodies[melody_index]["name"]
        melodies[melody_index]["count"] += 1

    company = {}
    if input_yes_no("Do you want to add company details? (y/n): ") == "y":
        company_name = input("Enter company name: ")
        occupation = input("Enter occupation: ")
        address = input("Enter company address: ")
        web_page = input("Enter company web page: ")
        company = {
            "name": company_name,
            "occupation": occupation,
            "address": address,
            "web_page": web_page,
        }

    other_phones = {}
    if input_yes_no("Do you want to add other phone numbers? (y/n): ") == "y":
        mobile_phone_2 = input("Enter mobile phone 2: ")
        mobile_phone_3 = input("Enter mobile phone 3: ")
        home_phone = input("Enter home phone: ")
        office_phone = input("Enter office phone: ")
        other_phones = {
            "mobile_phone_2": mobile_phone_2,
            "mobile_phone_3": mobile_phone_3,
            "home_phone": home_phone,
            "office_phone": office_phone,
        }

    emails = {}
    if input_yes_no("Do you want to add email addresses? (y/n): ") == "y":
        private_email_1 = input("Enter private email 1: ")
        private_email_2 = input("Enter private email 2: ")
        office_email = input("Enter office email: ")
        emails = {
            "private_email_1": private_email_1,
            "private_email_2": private_email_2,
            "office_email": office_email,
        }

    other = {}
    if input_yes_no("Do you want to add other details? (y/n): ") == "y":
        address = input("Enter address: ")
        birth_day = input("Enter birth day: ")
        notes = input("Enter notes: ")

        spouse = {}
        if input_yes_no("Do you want to add spouse details? (y/n): ") == "y":
            spouse_name = input("Enter spouse name: ")
            spouse_birthday = input("Enter spouse birthday: ")
            spouse_notes = input("Enter spouse notes: ")
            spouse = {
                "name": spouse_name,
                "birthday": spouse_birthday,
                "notes": spouse_notes,
            }

        children = []
        if input_yes_no("Do you want to add children details? (y/n): ") == "y":
            while True:
                child_name = input("Enter child name (or type 'q' to finish): ")
                if child_name.lower() == "q":
                    break
                child_birthday = input("Enter child birthday: ")
                child_notes = input("Enter child notes: ")
                child = {
                    "name": child_name,
                    "birthday": child_birthday,
                    "notes": child_notes,
                }
                children.append(child)

        other = {
            "address": address,
            "birth_day": birth_day,
            "notes": notes,
            "spouse": spouse,
            "children": children,
        }

    contact = create_contact(
        name,
        mobile_phone,
        group=group,
        melody=melody,
        company=company,
        other_phones=other_phones,
        emails=emails,
        other=other,
    )

    contacts.append(contact)

    return contacts, groups, melodies


def update_contact(contacts, groups, melodies):
    if not contacts:
        print("No contacts to update.")
        return contacts

    print("Select a contact to update or press 0 to return to the main menu:")
    for index, contact in enumerate(contacts):
        print(f"{index + 1}. {contact['name']} ({contact['mobile_phone']})")

    try:
        selected_index = int(input("Enter the contact's number: ")) - 1
        if selected_index == -1:
            return contacts
        if selected_index < 0 or selected_index >= len(contacts):
            print("Invalid contact number.")
            return contacts

        updated_contact, groups, melodies = add_contact([], groups, melodies)
        contacts[selected_index] = updated_contact[0]
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return contacts

    return contacts, groups, melodies


def delete_contact(contacts):
    if not contacts:
        print("No contacts to delete.")
        return contacts

    print("Select a contact to delete or press 0 to return to the main menu:")
    for index, contact in enumerate(contacts):
        print(f"{index + 1}. {contact['name']} ({contact['mobile_phone']})")

    try:
        selected_index = int(input("Enter the contact's number: ")) - 1
        if selected_index == -1:
            return contacts
        if selected_index < 0 or selected_index >= len(contacts):
            print("Invalid contact number.")
            return contacts

        del contacts[selected_index]
        print("Contact deleted.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return contacts

    return contacts


def search_contact(contacts):
    if not contacts:
        print("No contacts to search.")
        return

    try:
        search_query = input("Enter a search query (name or mobile phone): ").lower()
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled search.")
        return

    matching_contacts = [
        contact
        for contact in contacts
        if search_query in contact["name"].lower()
        or search_query in contact["mobile_phone"]
    ]

    if not matching_contacts:
        print("No contacts found matching your search query.")
        return

    print("Matching contacts:")
    for contact in matching_contacts:
        print(f"{contact['name']} ({contact['mobile_phone']})")


def manage_group_subscription(contacts, groups):
    if not contacts:
        print("No contacts available to manage group subscriptions.")
        return contacts, groups

    try:
        contact_mobile_phone = input(
            "Enter the mobile phone of the contact you want to manage: "
        )
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled group subscription management.")
        return contacts, groups

    selected_contact = None
    for contact in contacts:
        if contact["mobile_phone"] == contact_mobile_phone:
            selected_contact = contact
            break

    if not selected_contact:
        print("No contact found with the provided mobile phone number.")
        return contacts, groups

    print(f"Managing group subscription for: {selected_contact['name']}")

    if not groups:
        print("No groups available.")
    else:
        print("Available groups:")
        for group in groups:
            print(f"{group['name']}: {group['count']} contacts")

    try:
        action = input(
            "Enter 'add' to add the contact to a group or 'remove' to remove the contact from a group: "
        ).lower()
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled group subscription management.")
        return contacts, groups

    if action == "add":
        try:
            group_name = input(
                "Enter the name of the group you want to add the contact to: "
            )
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled group subscription management.")
            return contacts, groups

        group = next((group for group in groups if group["name"] == group_name), None)
        if not group:
            print(f"No group with the name {group_name} found.")
            return contacts, groups

        if selected_contact["group"] == group_name:
            print(f"{selected_contact['name']} is already in the group {group_name}.")
        else:
            if selected_contact["group"]:
                old_group = next(
                    (
                        group
                        for group in groups
                        if group["name"] == selected_contact["group"]
                    ),
                    None,
                )
                if old_group:
                    old_group["count"] -= 1

            selected_contact["group"] = group_name
            group["count"] += 1
            print(
                f"{selected_contact['name']} has been added to the group {group_name}."
            )

    elif action == "remove":
        if not selected_contact["group"]:
            print(f"{selected_contact['name']} is not in any group.")
        else:
            group_name = selected_contact["group"]
            group = next(
                (group for group in groups if group["name"] == group_name), None
            )
            if group:
                group["count"] -= 1

            selected_contact["group"] = None
            print(
                f"{selected_contact['name']} has been removed from the group {group_name}."
            )
    else:
        print("Invalid action. Please enter 'add' or 'remove'.")

    return contacts, groups


def manage_birthday_reminders(contacts):
    today = datetime.today()
    ten_days_from_today = today + timedelta(days=10)

    upcoming_birthdays = []

    for contact in contacts:
        birthday_str = contact["other"]["birth_day"]
        if not birthday_str:
            continue

        try:
            birthday = datetime.strptime(birthday_str, "%Y-%m-%d")
        except ValueError:
            print(
                f"Invalid date format for {contact['name']}'s birthday: {birthday_str}"
            )
            continue

        birthday = birthday.replace(year=today.year)

        if today <= birthday <= ten_days_from_today:
            upcoming_birthdays.append(contact)

    if upcoming_birthdays:
        print("Upcoming birthdays within 10 days:")
        for contact in upcoming_birthdays:
            print(f"{contact['name']} - {contact['other']['birth_day']}")
    else:
        print("No upcoming birthdays within 10 days.")


def print_contact_list(contacts):
    if not contacts:
        print("No contacts available.")
        return

    print("\nContacts summary:")
    print(
        "{:<20} {:<15} {:<20} {:<20}".format("Name", "Mobile Number", "Group", "Melody")
    )

    for contact in contacts:
        name = contact["name"]
        mobile_number = contact["mobile_phone"]
        group = contact["group"] if contact["group"] else "-"
        melody = contact["melody"] if contact["melody"] else "-"

        print("{:<20} {:<15} {:<20} {:<20}".format(name, mobile_number, group, melody))


def print_contact_details(contacts):
    if not contacts:
        print("No contacts available.")
        return

    for index, contact in enumerate(contacts):
        print(f"{index + 1}. {contact['name']} ({contact['mobile_phone']})")

    try:
        contact_number = int(input("Enter the contact number: ")) - 1
        if contact_number < 0 or contact_number >= len(contacts):
            print("Invalid contact number.")
            return

        selected_contact = contacts[contact_number]
        print("\nContact details:")

        selected_contact = contacts[contact_number]
        print("\nContact details:")

        print(f"Name: {selected_contact['name']}")
        print(f"Mobile phone: {selected_contact['mobile_phone']}")

        print(
            f"Group: {selected_contact['group'] if selected_contact['group'] else '-'}"
        )
        print(
            f"Melody: {selected_contact['melody'] if selected_contact['melody'] else '-'}"
        )

        for key, value in selected_contact.items():
            if key in ["name", "mobile_phone", "group", "melody"]:
                continue

            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    label = f"{key.capitalize()} {sub_key.capitalize()}:"
                    print(f"{label} {sub_value if sub_value else '-'}")
            else:
                print(f"{key.capitalize()}: {value if value else '-'}")

    except (ValueError, KeyboardInterrupt, EOFError):
        print("\nInvalid input or action canceled.")


if __name__ == "__main__":
    main()
