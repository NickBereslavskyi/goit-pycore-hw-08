from collections import UserDict
from datetime import datetime, timedelta

import pickle

def save_data(book, filename='addressbook.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(book, f)

def load_data(filename='addressbook.pkl'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    #реалізація класу
        pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Phone number must be exactly 10 digits.')
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            value = datetime.strptime(value, "%Y-%m-%d").date()
            if value < datetime.today().date():
                self.value = value
            else:
                raise ValueError('Birthday cannot be in the future.')
        except ValueError:
            raise ValueError("Incorrect format. Please enter the date in YYYY-MM-DD format.")
 

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone_number):
        new_phones = []
        for phone in self.phones:
            if phone.value != phone_number:
                new_phones.append(phone)
        self.phones = new_phones

    def edit_phones(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                return
        raise ValueError('Phone number not found.')
    
    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        for key, record in self.data.items():
            if key == name:
                return record
        return None
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]


def get_upcoming_birthdays(self):
    today = datetime.today().date()
    end_date = today + timedelta(days=7)
    upcoming_birthdays = []

    for record in self.data.values():
        if record.birthday:
            birthday = record.birthday.value.replace(year=today.year)
            if birthday < today:
                birthday = birthday.replace(year=today.year + 1)

            if today <= birthday <= end_date:
                if birthday.weekday() in [5,6]:
                    birthday += timedelta(days=(7 - birthday.weekday()))

                upcoming_birthdays.append({"name": record.name.value, "congratulation_date": birthday.strftime("%Y-%m-%d")})
    
    return upcoming_birthdays

    
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Error: not enough input arguments", []
        except ValueError:
            return "Error: wrong value format", []
        except Exception as e:
            return f"Unexpected error: {e}", []
    return wrapper


@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phones(old_phone, new_phone)
        return "Phone number updated."
    return "Contact not found."


@input_error
def show_phones(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return f"Phones: {', '.join(p.value for p in record.phones)}"
    return "Contact not found."


@input_error
def show_all(book):
    if not book:
        return "Address book is empty."
    return "\n".join(str(record) for record in book.values())


@input_error
def add_birthday(args, book):
    name, bday = args
    record = book.find(name)
    if record:
        record.add_birthday(bday)
        return "Birthday added."
    return "Contact not found."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}"
    return "Birthday not found for this contact."


@input_error
def birthdays(args, book):
    upcoming = get_upcoming_birthdays(book)
    if not upcoming:
        return "No birthdays in the next 7 days."
    
    result = []
    for item in upcoming:
        result.append(f"{item['name']} - {item['congratulation_date']}")
    return "\n".join(result)


@input_error
def parse_input(user_input):
    parts = user_input.strip().split()
    #if not parts:
    #    raise ValueError('No coommand provided')
    command = parts[0].lower()
    return command, parts[1:]


def main():
    book = load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        
        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phones(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()