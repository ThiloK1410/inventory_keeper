
from datetime import datetime
import GUI


class Storage:
    def __init__(self, delivery_list=None):
        self.crate_brands = dict()
        if delivery_list is None:
            self.delivery_list = []
        else:
            self.delivery_list = delivery_list

    class Delivery:
        def __init__(self, date, crate_brands):
            self.crate_brands = crate_brands
            self.properties = dict()
            self.crate_list = []
            self.bottle_count = 0
            self.properties.update({"Datum": date,
                                    "gekaufte Kisten": self.crate_list,
                                    "Anzahl Flaschen": self.bottle_count})
            self.update_values()

        def add_crates(self, name, count):
            self.crate_list.append([name, count])
            return self

        def update_values(self):
            temp_count = 0
            for crates in self.crate_list:
                temp_count += crates[1] * self.crate_brands.get(crates[0])
            self.bottle_count = temp_count

    def add_delivery(self, date=None):
        if date is None:
            date = datetime.now().date()
        self.delivery_list.append(self.Delivery(date, self.crate_brands))


    def add_brand(self, brand_name, crate_bottle_count):
        self.crate_brands.update({brand_name: crate_bottle_count})


if __name__ == "__main__":
    app = GUI.App()
    app.mainloop()