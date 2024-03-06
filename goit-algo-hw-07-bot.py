from classes import AddressBook, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not exist"
        except IndexError:
            return "Contact not found"

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_birthday(birthday)
    return f'Birthday {birthday} to contact {name} added'


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = f'Contact {name} update successfully'
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f'Contact {name} added successfully'
    if phone:
        record.add_phone(phone)
    return message


@input_error
def birthdays(args, book: AddressBook):
    return book.get_upcoming_birthdays()


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        return f'Contact {name} not found'
    record.edit_phone(old_phone, new_phone)
    return f'Contact {name} successfully changed'


def show_all(args, book: AddressBook):
    return book


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        return f'Contact {name} not found'
    return record.birthday


@input_error
def show_phone(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if not record:
        return f'Contact {name} not found'
    return '; '.join(str(phone) for phone in record.phones)


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ['close', 'exit']:
            print('Good by!')
            break

        elif command == 'hello':
            print('How can I help you?')

        elif command == 'add':
            print(add_contact(args, book))
        elif command == 'change':
            print(change_contact(args, book))
        elif command == 'phone':
            print(show_phone(args, book))
        elif command == 'all':
            print(show_all(args, book))
        elif command == 'birthday':
            print(show_birthday(args, book))
        elif command == 'add-birthday':
            print(add_birthday(args, book))
        elif command == 'show-birthday':
            print(birthdays(args, book))

        else:
            print('Invalid command.')


if __name__ == "__main__":
    main()
