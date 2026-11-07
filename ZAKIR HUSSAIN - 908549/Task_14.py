# Task 14 - Command-Line Contact Manager

import json


CONTACT_FILE = "contacts.json"


def load_contacts():
    try:
        with open(CONTACT_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Contact file must contain a list")
        return data

    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, OSError) as error:
        print("Contact file could not be read. Please fix it first.")
        raise ValueError("Could not read contacts.json safely") from error


def save_contacts(contacts):
    with open(CONTACT_FILE, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)


def add_contact(contacts, contact):
    for old_contact in contacts:
        if old_contact["id"] == contact["id"]:
            raise ValueError("Contact ID already exists")

    if not contact["name"].strip():
        raise ValueError("Name cannot be empty")

    contacts.append(contact)
    save_contacts(contacts)


def search_contacts(contacts, name):
    found = []

    for contact in contacts:
        if name.lower() in contact["name"].lower():
            found.append(contact)

    return found


def update_contact(contacts, contact_id, new_details):
    for contact in contacts:
        if contact["id"] == contact_id:
            contact.update(new_details)
            save_contacts(contacts)
            return True

    return False


def delete_contact(contacts, contact_id):
    for contact in contacts:
        if contact["id"] == contact_id:
            contacts.remove(contact)
            save_contacts(contacts)
            return True

    return False


def main():
    try:
        contacts = load_contacts()
    except ValueError as error:
        print(error)
        print("Fix the JSON file before using the contact manager.")
        return

    while True:
        print("\\n1. Add  2. Search  3. Update  4. Delete  5. List  6. Exit")
        choice = input("Choose: ")

        try:
            if choice == "1":
                contact = {
                    "id": input("ID: ").strip(),
                    "name": input("Name: ").strip(),
                    "phone": input("Phone: ").strip(),
                    "email": input("Email: ").strip()
                }
                add_contact(contacts, contact)
                print("Contact added.")

            elif choice == "2":
                name = input("Name to search: ")
                for contact in search_contacts(contacts, name):
                    print(contact)

            elif choice == "3":
                contact_id = input("ID to update: ").strip()
                details = {
                    "name": input("New name: ").strip(),
                    "phone": input("New phone: ").strip(),
                    "email": input("New email: ").strip()
                }
                if update_contact(contacts, contact_id, details):
                    print("Contact updated.")
                else:
                    print("Contact not found.")

            elif choice == "4":
                contact_id = input("ID to delete: ").strip()
                if delete_contact(contacts, contact_id):
                    print("Contact deleted.")
                else:
                    print("Contact not found.")

            elif choice == "5":
                for contact in contacts:
                    print(contact)

            elif choice == "6":
                break

            else:
                print("Please choose a number from 1 to 6.")

        except (ValueError, OSError) as error:
            print("Error:", error)


if __name__ == "__main__":
    main()