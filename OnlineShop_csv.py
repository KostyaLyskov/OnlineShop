import csv
import os
from datetime import datetime
import subprocess


class Car:
    def __init__(self, name, brand, price, year, mileage):
        self.name = name
        self.brand = brand
        self.price = int(price)
        self.year = int(year)
        self.mileage = int(mileage)

    def info(self, index=None):
        if index is not None:
            print(f"\nАвтомобіль №{index}")
        print("-" * 20)
        print(f"Модель: {self.name}")
        print(f"Виробник: {self.brand}")
        print(f"Ціна($): {self.price} $")
        print(f"Рік випуску: {self.year} р.")
        print(f"Пробіг: {self.mileage} км.")

    def to_dict(self):
        return {
            "name": self.name,
            "brand": self.brand,
            "price": self.price,
            "year": self.year,
            "mileage": self.mileage,
        }


base_dir = os.path.dirname(os.path.abspath(__file__))


class OnlineShop:
    cars_list = os.path.join(base_dir, "cars_list.csv")

    def __init__(self):
        self.cars = []
        self.load_from_csv()

    def save_to_csv(self):
        with open(self.cars_list, "wt", newline="", encoding="utf-8-sig") as fwriting:
            fieldnames_cars = ["name", "brand", "price", "year", "mileage"]
            writer = csv.DictWriter(
                fwriting, fieldnames=fieldnames_cars, delimiter=";")
            writer.writeheader()
            for car in self.cars:
                writer.writerow(car.to_dict())

    def load_from_csv(self):
        if not os.path.exists(self.cars_list):
            self.save_to_csv()
            return

        with open(self.cars_list, "rt", encoding="utf-8-sig") as freading:
            reader = csv.DictReader(freading, delimiter=";")
            self.cars = [
                Car(
                    row["name"],
                    row["brand"],
                    row["price"],
                    row["year"],
                    row["mileage"],
                )
                for row in reader
            ]

    def show_cars(self):
        if not self.cars:
            print("Каталог порожній.")
            return

        for i, car in enumerate(self.cars, start=1):
            car.info(index=i)

    def add_car(self):
        name = input("Введіть модель автомобіля: ").strip()
        brand = input("Введіть виробника: ").strip()
        price = type_check("Введіть ціну($): ")
        year = year_check("Введіть рік випуску: ")
        mileage = type_check("Введіть пробіг (км.): ")

        car = Car(name, brand, price, year, mileage)
        self.cars.append(car)
        self.save_to_csv()
        print("-" * 20)
        print("Автомобіль було успішно додано.")

    def search_cars(self):
        print("-" * 20)
        min_price = type_check("Мінімальна ціна($): ", is_empty=True)
        max_price = type_check("Максимальна ціна($): ", is_empty=True)
        brand = input("Виробник: ").strip()
        year = year_check("Рік випуску: ", is_empty=True)
        min_mileage = type_check("Мінімальний пробіг(км.): ", is_empty=True)
        max_mileage = type_check(
            "Максимальний пробіг(км.): ", is_empty=True)

        found_cars = []

        for car in self.cars:
            if min_price is not None and car.price < min_price:
                continue
            if max_price is not None and car.price > max_price:
                continue
            if brand and brand.lower() != car.brand.lower():
                continue
            if year is not None and car.year != year:
                continue
            if min_mileage is not None and car.mileage < min_mileage:
                continue
            if max_mileage is not None and car.mileage > max_mileage:
                continue
            found_cars.append(car)

        print("-" * 20)
        if not found_cars:
            print("За вказаними параметрами автомобілей не знайдено.")
        else:
            print(
                f"За параметрами знайдено {len(found_cars)} автомобілей.")

            for i, car in enumerate(found_cars, start=1):
                car.info(index=i)

    def del_car(self):
        while True:
            if not self.cars:
                print("Каталог порожній.")
                return

            print("\nСписок автомобілів для видалення:")
            self.show_cars()

            car_id = type_check(
                "\nНомер автомобіля для видалення([0] - скасувати): ")

            print("-" * 20)
            if car_id == 0:
                print("Видалення скасовано.")
                return

            if 1 <= car_id <= len(self.cars):
                removed = self.cars.pop(car_id - 1)
                self.save_to_csv()
                print(
                    f"Автомобіль №{car_id} {removed.brand} моделі {removed.name} було видалено.")

            else:
                print("Автомобіля з таким номером не існує.")

    def edit_car(self):
        while True:
            if not self.cars:
                print("Каталог порожній.")
                return

            print("\nСписок автомобілів для редагування:")
            self.show_cars()

            car_red = type_check(
                "\nНомер автомобіля для редагування([0] - скасувати): ")

            print("-" * 20)
            if car_red == 0:
                print("Редагування скасовано.")
                return

            if 1 <= car_red <= len(self.cars):
                old_car = self.cars[car_red - 1]

                new_name = input(
                    f"Поточна модель: {old_car.name}. Введіть нове значення: ").strip()
                name = new_name if new_name else old_car.name

                new_brand = input(
                    f"Поточний виробник: {old_car.brand}. Введіть нове значення: ").strip()
                brand = new_brand if new_brand else old_car.brand

                new_price = type_check(
                    f"Поточна ціна: {old_car.price}. Введіть нове значення: ", is_empty=True)
                price = new_price if new_price else old_car.price

                new_year = year_check(
                    f"Поточний рік випуску: {old_car.year}. Введіть нове значення: ", is_empty=True)
                year = new_year if new_year else old_car.year

                new_mileage = type_check(
                    f"Поточний пробіг (км.): {old_car.mileage}. Введіть нове значення: ", is_empty=True)
                mileage = new_mileage if new_mileage is not None else old_car.mileage

                self.cars[car_red - 1] = Car(name, brand, price, year, mileage)
                self.save_to_csv()
                print(f"\nАвтомобіль №{car_red} було успішно відредаговано.")

            else:
                print("Автомобіля з таким номером не існує.")


# Цикл для запиту на коректний ввод даних (для int)
def type_check(question, is_empty=False):
    while True:
        user_input = input(question).strip()

        if is_empty and user_input == "":
            return None

        try:
            val = int(user_input)
            if val < 0:
                print("Помилка! Значення не може бути від'ємним.")
            else:
                return val
        except ValueError:
            print("Помилка! Введіть ціле числове значення.")


# Перевірка коректного вводу року виготовлення
def year_check(question, is_empty=False):
    current_year = datetime.now().year

    while True:
        year = type_check(question, is_empty=is_empty)
        if is_empty and year is None:
            return None

        if 1886 <= year <= current_year:
            return year
        else:
            print(
                f"Неправильне значення. Рік має бути від 1886 до {current_year}.")


def clear_console():
    if os.name == "nt":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)


def main():
    store = OnlineShop()

    while True:
        clear_console()
        print("\n===== ОНЛАЙН-МАГАЗИН АВТОМОБІЛІВ =====")
        print("1. Переглянути всі автомобілі")
        print("2. Додати автомобіль")
        print("3. Пошук")
        print("4. Видалити автомобіль")
        print("5. Редагування автомобіля")
        print("0. Вийти з програми")
        print("======================================")

        choice = input("Оберіть дію: ").strip()

        if choice == "1":
            store.show_cars()

        elif choice == "2":
            print("-" * 20)
            store.add_car()

        elif choice == "3":
            store.search_cars()

        elif choice == "4":
            store.del_car()

        elif choice == "5":
            store.edit_car()

        elif choice == "0":
            print("-" * 20)
            print("Програму успішно завершено.\n")
            break

        else:
            print("Дія відсутня. Спробуйте ще раз.")

        input("\nНатисніть Enter, щоб продовжити...")


if __name__ == ("__main__"):
    main()
