from collections import UserDict
from datetime import datetime
import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def is_valid(self, value):
        return True

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.is_valid(value):
            self.__value = value
        else:
            raise ValueError

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def is_valid(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except:
            return False

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.is_valid(value):
            self.__value = datetime.strptime(value, "%d.%m.%Y")
        else:
            raise ValueError


class Name(Field):
    def is_valid(self, value):
        return bool(value)
                 

class Phone(Field):
    def is_valid(self, value):
        return len(value) == 10 and value.isdigit()
       

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    # реалізація класу
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def edit_phone(self, old_phone, new_phone):
        if self.find_phone(old_phone):
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
        else:
            raise ValueError

    def find_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone:
                return ph
            return None
    
    def remove_phone(self, phone):
        ph = self.find_phone(phone)
        self.phones.remove(ph)

    def __str__(self):
        return f"Contact name: {str(self.name)}, phones: {'; '.join(str(p.value) for p in self.phones)}, birthday: {str(self.birthday)}"


class AddressBook(UserDict):
    # реалізація класу
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if self.find(name):
            del self.data[name]

    def find(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self):
        curent_date = datetime.today().date()
        birthdays = []
        for user in self.data:
            birthday_date = str(curent_date.year) + str(user["birthday"])[4:]
            birthday_date = datetime.strptime(birthday_date,"%Y.%m.%d").date()
            week_day_bdate = birthday_date.isoweekday()
            days_between = (birthday_date - curent_date).days
            if 0 <= days_between < 7:
                match week_day_bdate:
                    case 6:
                        birthdays.append({'name': user['name'],
                                          'congratulation_date': (birthday_date + datetime.timedelta(days=2)).strftime(
                                              "%Y.%m.%d")})
                    case 7:
                        birthdays.append({'name': user['name'],
                                          'congratulation_date': (birthday_date + datetime.timedelta(days=1)).strftime(
                                              "%Y.%m.%d")})
                    case _:
                        birthdays.append(
                            {'name': user['name'], 'congratulation_date': birthday_date.strftime("%Y.%m.%d")})

        return birthdays

    def __str__(self):
       return f"Contacts: {'; '.join(str(record) for record in self.data.values())}"


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
