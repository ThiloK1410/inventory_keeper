import io
from datetime import datetime
import json


class Delivery:
    def __init__(self, date, crate_brands):
        self.properties = dict()
        self.crate_list = []
        self.properties.update({"Datum": date, "gekaufte Kisten": self.crate_list})

    def add_crates(self, name, count):
        self.crate_list.append([name, count])
        return self




class Storage:
    def __init__(self):
        self.crate_brands = dict()
        self.delivery_list = []

    def add_delivery(self, date=None):
        if date is None:
            date = datetime.now().date()
        self.delivery_list.append(Delivery(date, self.crate_brands))

    def add_brand(self, brand_name, crate_bottle_count):
        self.crate_brands.update({brand_name: crate_bottle_count})


if __name__ == "__main__":
    Lager = None
    file_name = "data.json"
    allow_saving = True
    try:
        with open(file_name, "r") as f:
            Lager = json.load(f)
            print(f"Bestehendes Lager wurde aus der {file_name} Datei geladen")
    except json.decoder.JSONDecodeError:
        Lager = Storage()
        print(f"Die Datei {file_name} enthält fehlerhafte / keine Daten, ein neues Lager wurde angelegt")
        answer = input("Soll das Lager gespeichert und die Datei überschrieben werden? (y|N):")
        answer = answer.lower()
        if answer == "" or answer == "n":
            allow_saving = False
        elif answer == "y":
            allow_saving = True



    while True:
        if allow_saving:
            with open(file_name, "w") as f:
                json.dump(Lager, f)
        print("Was willst du machen?")
        print("1. Lieferung Hinzufügen | 2. Marke Hinzufügen | 3. Info")
        temp = input("Bitte wählen:")

        if temp == "1":
            print("Willst du das heutige Datum verwenden? (Y|n)")
            answer = input("Bitte wählen:")
            answer = answer.lower()
            if answer == "" or answer == "y":
                Lager.add_delivery()
            if answer == "n":
                answer = input("Bitte gib das neue Datum an (DD.MM.YYYY):")
                date = datetime.strptime(answer, "%d.%m.%Y")
                Lager.add_delivery(date.date())

        if temp == "2":
            brand_name = input("Name der Marke:")
            bottle_count = input("Anzahl Flaschen pro Kasten:")
            Lager.add_brand(brand_name, bottle_count)

        elif temp == "3":
            print(Lager.crate_brands)
            for i, x in enumerate(Lager.delivery_list):
                print(f"{i+1}. Lieferung: {x.properties}")
            input()

