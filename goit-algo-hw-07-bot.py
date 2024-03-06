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

def exit(args, book: AddressBook):
    return 'Good bye!'

def hello(args, book: AddressBook):
    return 'How can I help you?'

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
    commands = {
        'add': add_contact,
        'add-birthday': add_birthday,
        'all': show_all,
        'birthday': birthdays,
        'change': change_contact,
        'hello': hello,
        'phone': show_phone,
        'show-birthday': show_birthday, 
    }
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ['close', 'exit']:
            print('Good by!')
            break
        else:
            try:
                print(commands[command](args, book))
            except KeyError:
                print('Invalid command.')


if __name__ == "__main__":
    main()
