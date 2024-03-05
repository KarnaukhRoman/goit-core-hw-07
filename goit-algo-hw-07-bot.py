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

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return f'Contact {name} added successfully'

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        return f'Contact {name} not found'
    record.edit_phone(old_phone, new_phone)
    return f'Contact {name} successfully changed"

@input_error
def show_phone(name, contacts):
    if name in contacts:
        return contacts[name]
    else:
        raise(IndexError)

def show_all(contacts):
    all_contacts = ''
    for name, phone in contacts.items():
        all_contacts+=name+' '+phone+'\n'
    return all_contacts

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    contacts = {}

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ['close','exit']:
            print('Good by!')
            break

        elif command == 'hello':
            print('How can I help you?')

        elif command == 'add':
            print(add_contact(args, book))
        elif command == 'change':
            print(change_contact(args, book))
        elif command == 'phone':
            if book:
                print(show_phone(args[0], book))
            else:
                print('Contacts is empty')

        elif command == 'all':
            if contacts:
                print(show_all(contacts))
            else:
                print('Contacts is empty')
        else:
            print('Invalid command.')


if __name__=="__main__":
    main()
