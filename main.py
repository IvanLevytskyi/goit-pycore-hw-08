import pickle
from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        # Validation: the phone number must consist of exactly 10 digits
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            # Check the format and convert the string into a datetime object
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if not phone_to_edit:
            raise ValueError(f"Phone number {old_phone} not found.")
        # Create a new Phone object to validate the new number
        new_phone_obj = Phone(new_phone)
        phone_to_edit.value = new_phone_obj.value

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, birthday_string):
        self.birthday = Birthday(birthday_string)

    def __str__(self):
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today().date()
        
        for record in self.data.values():
            if not record.birthday:
                continue
            
            birthday = record.birthday.value
            # Shift the birthday to the current year
            birthday_this_year = birthday.replace(year=today.year)
            
            # If the birthday has already passed this year, consider the next year
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            
            # Check if the birthday falls within the next 7 days (including today)
            if today <= birthday_this_year <= today + timedelta(days=6):
                # If the birthday falls on a weekend, move the congratulation to Monday
                congratulation_date = birthday_this_year
                if congratulation_date.weekday() == 5:    # Saturday
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:  # Sunday
                    congratulation_date += timedelta(days=1)
                
                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                })
                
        return upcoming_birthdays
    
# --- Functions for working with pickle ---

def save_data(book, filename="addressbook.pkl"):
    """Saves the address book to a file."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    """Loads the address book from a file. If the file doesn't exist, creates a new one."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Returns an empty book if the file has not been created yet

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Enter user name and phone/birthday number."
        except KeyError:
            return "Contact not found."
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        raise ValueError("Give me name, old phone and new phone please.")
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated successfully."
    else:
        raise KeyError

@input_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Enter user name.")
    name = args[0]
    record = book.find(name)
    if record:
        return f"Phones for {name}: {', '.join(p.value for p in record.phones)}"
    else:
        raise KeyError

@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "Address book is empty."
    return "\n".join(str(record) for record in book.data.values())

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Give me name and birthday (DD.MM.YYYY) please.")
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    else:
        raise KeyError

@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Enter user name.")
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return f"{name}'s birthday: {record.birthday}"
        return f"No birthday set for {name}."
    else:
        raise KeyError

@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays in the next week."
    
    result = "Upcoming birthdays for the next week:\n"
    for item in upcoming:
        result += f"{item['name']}: congratulation date -> {item['congratulation_date']}\n"
    return result.strip()

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

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
            print(show_phone(args, book))

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
