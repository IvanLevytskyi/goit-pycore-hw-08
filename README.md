# goit-pycore-hw-08
# Personal Assistant Bot (Address Book with Data Persistence)

This is a command-line interface (CLI) assistant bot designed to help you manage your contacts efficiently. The application allows you to store contact information, including phone numbers and birthdays, and features data persistence so your contacts are never lost when the program closes.

This project is the final part of the homework assignment for the GoIT Python Core course.

## Features

- **Data Persistence:** Automatically saves your address book to a file (`addressbook.pkl`) upon exit and restores it when you launch the application again.
- **Contact Management:** Add new contacts, change existing phone numbers, and display saved records.
- **Birthday Tracking:** Add birthdays to your contacts and check which upcoming birthdays are happening within the next 7 days.

## Technical Implementation

The project utilizes the following core Python concepts:
- **`pickle` module:** Used for data serialization and deserialization to save the state of the `AddressBook` object to a binary file.
- **Error Handling:** Built-in protection against missing files (`FileNotFoundError`) by automatically initializing a fresh address book on the first run.
- **Object-Oriented Programming (OOP):** Structures data using `AddressBook`, `Record`, `Field`, `Name`, `Phone`, and `Birthday` classes.

## Installation

1. Clone this repository to your local machine:
```bash
   git clone [https://github.com/YOUR_USERNAME/goit-pycore-hw-08.git](https://github.com/YOUR_USERNAME/goit-pycore-hw-08.git)
