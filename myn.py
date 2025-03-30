
import json
import os
from datetime import datetime

class Animal:
    """Базовый класс для всех животных"""
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.type = self.__class__.__name__  # Для сохранения типа

    def make_sound(self):
        print(f"{self.name} издаёт звук")

    def eat(self):
        print(f"{self.name} ест")

    def __str__(self):
        return f"{self.type} {self.name}, возраст: {self.age}"


class Bird(Animal):
    """Класс птиц с размахом крыльев"""
    def __init__(self, name, age, wingspan):
        super().__init__(name, age)
        self.wingspan = wingspan

    def make_sound(self):
        print(f"{self.name} говорит: Чирик-чирик!")

    def fly(self):
        print(f"{self.name} летает с размахом крыльев {self.wingspan} см")


class Mammal(Animal):
    """Класс млекопитающих с цветом шерсти"""
    def __init__(self, name, age, fur_color):
        super().__init__(name, age)
        self.fur_color = fur_color

    def make_sound(self):
        print(f"{self.name} говорит: Рррр!")

    def run(self):
        print(f"{self.name} бегает")


class Reptile(Animal):
    """Класс рептилий с типом чешуи"""
    def __init__(self, name, age, scale_type):
        super().__init__(name, age)
        self.scale_type = scale_type

    def make_sound(self):
        print(f"{self.name} говорит: Шшшш!")

    def bask(self):
        print(f"{self.name} греется на солнце")


class ZooKeeper:
    """Класс смотрителя зоопарка"""
    def __init__(self, name, experience=0):
        self.name = name
        self.experience = experience
        self.type = self.__class__.__name__

    def feed_animal(self, animal):
        print(f"{self.name} кормит {animal.name}")
        animal.eat()

    def __str__(self):
        return f"Смотритель {self.name}, опыт: {self.experience} лет"


class Veterinarian:
    """Класс ветеринара"""
    def __init__(self, name, specialization="Общая"):
        self.name = name
        self.specialization = specialization
        self.type = self.__class__.__name__

    def heal_animal(self, animal):
        print(f"{self.name} лечит {animal.name}")

    def __str__(self):
        return f"Ветеринар {self.name} ({self.specialization})"


class Zoo:
    """Основной класс зоопарка с функциями сохранения"""
    def __init__(self, name="Мой зоопарк"):
        self.name = name
        self.animals = []
        self.staff = []
        self.last_fed = None

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"Добавлено животное: {animal}")

    def add_staff(self, staff):
        self.staff.append(staff)
        print(f"Добавлен сотрудник: {staff}")

    def show_info(self):
        print(f"\nИнформация о зоопарке '{self.name}':")
        print("\nЖивотные:")
        for animal in self.animals:
            print(f" - {animal}")
        print("\nСотрудники:")
        for person in self.staff:
            print(f" - {person}")
        if self.last_fed:
            print(f"\nПоследнее кормление: {self.last_fed}")

    def save_to_file(self, filename="zoo_data.json"):
        """Сохраняет данные зоопарка в файл"""
        data = {
            "zoo_name": self.name,
            "animals": [a.__dict__ for a in self.animals],
            "staff": [s.__dict__ for s in self.staff],
            "last_fed": self.last_fed
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\nДанные сохранены в файл {filename}")

    @classmethod
    def load_from_file(cls, filename="zoo_data.json"):
        """Загружает данные зоопарка из файла"""
        if not os.path.exists(filename):
            print("Файл с данными не найден, создан новый зоопарк")
            return cls()

        with open(filename, encoding="utf-8") as f:
            data = json.load(f)

        zoo = cls(data.get("zoo_name", "Мой зоопарк"))
        zoo.last_fed = data.get("last_fed")

        # Восстанавливаем животных
        animal_classes = {"Bird": Bird, "Mammal": Mammal, "Reptile": Reptile}
        for animal_data in data["animals"]:
            animal_type = animal_data.pop("type")
            if animal_type in animal_classes:
                animal = animal_classes[animal_type](**animal_data)
                zoo.animals.append(animal)

        # Восстанавливаем сотрудников
        staff_classes = {"ZooKeeper": ZooKeeper, "Veterinarian": Veterinarian}
        for staff_data in data["staff"]:
            staff_type = staff_data.pop("type")
            if staff_type in staff_classes:
                staff = staff_classes[staff_type](**staff_data)
                zoo.staff.append(staff)

        print(f"\nДанные загружены из файла {filename}")
        return zoo


def animal_sound(animals):
    """Демонстрация полиморфизма"""
    print("\nЗвуки животных:")
    for animal in animals:
        animal.make_sound()


def main():
    """Главная функция программы"""
    print("=== Система управления зоопарком ===")
    zoo = Zoo.load_from_file()

    # Если зоопарк новый, добавляем тестовые данные
    if not zoo.animals:
        zoo.add_animal(Bird("Попугай Кеша", 2, 15))
        zoo.add_animal(Mammal("Лев Симба", 5, "золотистый"))
        zoo.add_animal(Reptile("Змея Каа", 3, "гладкая"))
        zoo.add_staff(ZooKeeper("Иван Иванов", 5))
        zoo.add_staff(Veterinarian("Доктор Айболит", "Экзотические животные"))

    # Демонстрация работы
    zoo.show_info()
    animal_sound(zoo.animals)

    # Сохраняем данные перед выходом
    zoo.save_to_file()
    print("\nВсе изменения сохранены!")


if __name__ == "__main__":
    main()