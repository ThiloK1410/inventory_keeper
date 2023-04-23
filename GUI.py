import tkinter.messagebox

import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog
import pickle
from datetime import datetime
from db_connector import Database


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = Database()

        self.geometry("800,400")
        self.title("INVENTORY KEEPER")

        self.brands = self.db.get_brands()

        self.deliveries_frame = None
        self.brands_frame = None
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="left")
        self.add_layout(self.main_frame)

    def refresh(self):
        self.brands_frame.update_from_list(self.brands)

    def add_layout(self, target):

        set_price_button = ctk.CTkButton(target, text="set price")
        set_price_button.grid(row=0, column=1, padx=10, pady=10)

        empty_button1 = ctk.CTkButton(target, text="refresh",
                                      command=lambda: self.refresh())
        empty_button1.grid(row=0, column=2, padx=10, pady=10)

        self.deliveries_frame = ScrollableButtonFrame(target, "Lieferungen")
        self.deliveries_frame.grid(row=1, column=0)

        self.brands_frame = ScrollableButtonFrame(target, "Marken")
        self.brands_frame.grid(row=1, column=1, padx=10, pady=10)

        button_box = ctk.CTkFrame(target)
        button_box.grid(row=1, column=2, padx=10, pady=10)

        add_brand_button = ctk.CTkButton(button_box, text="Marke hinzufügen",
                                         command=(lambda: self.add_brand()))
        add_brand_button.pack(side="top", padx=10, pady=10)

        delete_brand_button = ctk.CTkButton(button_box, text="Marke löschen")
        delete_brand_button.pack(side="top", padx=10, pady=10)

        add_delivery_button = ctk.CTkButton(button_box, text="Lieferung hinzufügen",
                                            command=(lambda: self.add_delivery()))
        add_delivery_button.pack(side="top", padx=10, pady=10)

        delete_delivery_button = ctk.CTkButton(button_box, text="Lieferung löschen")
        delete_delivery_button.pack(side="top", padx=10, pady=10)

        add_crate_button = ctk.CTkButton(button_box, text="Kiste hinzufügen")
        add_crate_button.pack(side="top", padx=10, pady=10)

        remove_crate_button = ctk.CTkButton(button_box, text="Kiste löschen")
        remove_crate_button.pack(side="top", padx=10, pady=10)

        info_frame = ctk.CTkFrame(target)
        info_frame.grid(row=2, column=0, columnspan=2, padx=10)

        info_text_box = tk.Text(info_frame, font=("Arial", 20), height=10, width=50)
        info_text_box.pack(expand=True)

        content_frame = ctk.CTkFrame(target)
        content_frame.grid(row=2, column=2, padx=10, pady=10)

        content_text_box = tk.Text(content_frame, font=("Arial", 20), height=10, width=20)
        content_text_box.pack(expand=True)

    def print_all(self):
        print(self.db.get_brands())

    def update_deliveries(self, delivery_list):
        if not len(self.deliveries.children) == len(delivery_list):
            for widget in self.deliveries.winfo_children():
                widget.destroy()
            for delivery in delivery_list:
                label_name = delivery.properties["Datum"].strftime("%d.%m.%Y") + "  -  #" + \
                             delivery.properties["Anzahl Flaschen"]
                delivery_label = ctk.CTkLabel(self.deliveries, text=label_name)
                delivery_label.pack()

    def add_delivery(self):
        answer = tk.messagebox.askyesnocancel("", "Soll die Lieferung mit dem heutigen Datum hinzugefügt werden?")
        if answer is None:
            return
        if answer:
            date = datetime.now().date().strftime("%d.%m.%Y")
        else:
            date = simpledialog.askstring("Datum", "Datum der Lieferung: (DD.MM.YYYY)")
        price = simpledialog.askfloat("Kosten", "Wieviel hat die Lieferung gekostet? (OHNE PFAND)")

    def add_brand(self):
        name = simpledialog.askstring("Brand Name", "Wie heißt die Marke?")
        bottle_count = simpledialog.askinteger("Anzahl Flaschen", "Wieviele Flaschen sind in einem Kasten?")
        self.db.add_brand(name, bottle_count)


class ScrollableButtonFrame(ctk.CTkFrame):
    def __init__(self, parent, title="",  **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.contents = []

        self.title = ctk.CTkLabel(self, text=title)
        self.title.pack(side="top", fill="x")
        self.content_frame = ctk.CTkScrollableFrame(self)
        self.content_frame.pack(side="top")

    def add_item(self, name):
        item_button = ctk.CTkButton(self.content_frame, text=name)
        item_button.pack(side="top")
        self.contents.append(item_button)

    def update_from_list(self, content_list):
        for i in self.contents:
            i.destroy()
        for content in content_list:
            strings = [str(x) for x in content]
            text = " | ".join(strings)
            self.add_item(text)


if __name__ == "__main__":
    app = App()
    app.mainloop()
