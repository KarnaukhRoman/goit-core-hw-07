from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)  

class Name(Field):
   def __init__(self, value):
       super().__init__(value)
                 

class Phone(Field):
    # реалізація класу
     def __init__(self, number):
         if len(number) != 10 or not number.isdigit():
            raise ValueError
         self.number = number
         super().__init__(number)
       
class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

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
       return f"Contact name: {str(self.name)}, phones: {'; '.join(str(p.value) for p in self.phones)}"

class AddressBook(UserDict):
    # реалізація класу
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if self.find(name):
            del self.data[name]

    def find(self, name):
        return self.data.get(name)



if __name__=="__main__":
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
