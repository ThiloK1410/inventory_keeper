import tkinter.messagebox

import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog
import pickle
from datetime import datetime
from main import Storage


class App(ctk.CTk):
    def __init__(self, file_name):
        super().__init__()

        self.file_name = "data.pkl"

        self.file_name = file_name
        self.storage = self.load_storage_from_file()

        self.geometry("800,400")
        self.title("INVENTORY KEEPER")

        self.file_name_label = ctk.CTkLabel(self, text=self.file_name)
        self.file_name_label.grid(row=0, column=0, padx=10, pady=10)

        set_price_button = ctk.CTkButton(self, text="set price")
        set_price_button.grid(row=0, column=1, padx=10, pady=10)

        save_button = ctk.CTkButton(self, text="Speichern", command=(lambda: self.save_all()))
        save_button.grid(row=0, column=2, padx=10, pady=10)

        empty_button2 = ctk.CTkButton(self, text="empty2")
        # empty_button2.grid(row=0, column=3, padx=10, pady=10)

        self.deliveries = ctk.CTkScrollableFrame(self)
        self.deliveries.grid(row=1, column=0, padx=10, pady=10)

        brands = ctk.CTkScrollableFrame(self)
        brands.grid(row=1, column=1, padx=10, pady=10)

        button_box = ctk.CTkFrame(self)
        button_box.grid(row=1, column=2, padx=10, pady=10)

        add_button = ctk.CTkButton(button_box, text="Lieferung hinzufügen", command=(lambda: self.add_delivery()))
        add_button.pack(side="top", padx=10, pady=10)

        add_button = ctk.CTkButton(button_box, text="Lieferung löschen")
        add_button.pack(side="top", padx=10, pady=10)

        add_button = ctk.CTkButton(button_box, text="Kiste hinzufügen")
        add_button.pack(side="top", padx=10, pady=10)

        remove_button = ctk.CTkButton(button_box, text="Kiste löschen")
        remove_button.pack(side="top", padx=10, pady=10)

        info_frame = ctk.CTkFrame(self)
        info_frame.grid(row=2, column=0, columnspan=2, padx=10)

        info_text_box = tk.Text(info_frame, font=("Arial", 20), height=10, width=50)
        info_text_box.pack(expand=True)

        content_frame = ctk.CTkFrame(self)
        content_frame.grid(row=2, column=2, padx=10, pady=10)

        content_text_box = tk.Text(content_frame, font=("Arial", 20), height=10, width=20)
        content_text_box.pack(expand=True)

    def set_file_name(self, name):
        self.file_name_label.configure(text=name)

    def save_all(self):
        open(self.file_name, "wb").close()
        with open(self.file_name, "wb") as f:
            pickle.dump(self.storage, f)
        print("save_all successful")
        tkinter.messagebox.showinfo("Information", "Save successful")

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
        answer = tkinter.messagebox.askyesnocancel("", "Soll die Lieferung mit dem heutigen Datum hinzugefügt werden?")
        if answer is None:
            return
        if answer:
            self.storage.add_delivery()
        else:
            date = simpledialog.askstring("Datum", "Datum der Lieferung: (DD.MM.YYYY)")
            date = datetime.strptime(date, "%d.%m.%Y")
            self.storage.add_delivery(date)

    def load_storage_from_file(self):
        try:
            with open(self.file_name, "rb") as f:
                self.storage = pickle.load(f)
                if not isinstance(self.storage, Storage):
                    Lager = Storage()
                    print("Das Lager konnte nicht geladen werden und es wurde ein neues angelegt.")
                else:
                    print(f"Bestehendes Lager wurde aus der {file_name} Datei geladen")
        except Exception as e:
            print(e)
            Lager = Storage()
            print(f"Die Datei {file_name} enthält fehlerhafte / keine Daten, ein neues Lager wurde angelegt")
            






if __name__ == "__main__":
    app = App()
    app.mainloop()
