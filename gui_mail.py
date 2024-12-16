import customtkinter as ctk
from tkinter import simpledialog, messagebox
from tkinter import filedialog
from PIL import Image  # Pentru procesarea logo-ului
from mail import generare_mesaj, trimite_email  # Schimba cu numele fisierului tau
import tkinter # Blochează interacțiunea cu fereastra principală


class EmailApp:
    def __init__(self, root):
        ctk.set_appearance_mode("light")  # Mod de culori: "light", "dark", "system"
        ctk.set_default_color_theme("blue")  # Tema culori de baza

        self.root = root
        self.root.title("Cerere de Oferta - Personalizat")
        self.root.geometry("700x700")
        self.root.resizable(True, True)  # Permite redimensionarea

        # Setează logo-ul din stânga sus
        self.root.iconbitmap("app_icon.ico")

        # Adaugare logo
        logo_frame = ctk.CTkFrame(root, fg_color="transparent")  # Cadru transparent
        logo_frame.pack(pady=10)

        logo_image = ctk.CTkImage(
            light_image=Image.open("logo.png"),  # Imagine PNG cu fundal transparent
            size=(250, 50)  # Dimensiunea logo-ului
        )
        logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="", fg_color="transparent")  # Transparent
        logo_label.pack()

        # Sectiune detalii generale
        frame_details = ctk.CTkFrame(root, corner_radius=15, fg_color="#f0f0f0")  # Gri deschis
        frame_details.pack(pady=20, padx=20, fill="x")

        ctk.CTkLabel(frame_details, text="Subiect:", font=("Arial", 12), text_color="#1f4e78").grid(row=0, column=0, sticky="w", padx=10, pady=10)  # Albastru
        self.entry_subiect = ctk.CTkEntry(frame_details, width=400, border_color="#1f4e78")  # Albastru
        self.entry_subiect.insert(0, "Cerere oferta")
        self.entry_subiect.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_details, text="Numele Licitatiei:", font=("Arial", 12), text_color="#1f4e78").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.entry_licitatie = ctk.CTkEntry(frame_details, width=400, border_color="#1f4e78")
        self.entry_licitatie.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_details, text="Numarul CN:", font=("Arial", 12), text_color="#1f4e78").grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.entry_cn = ctk.CTkEntry(frame_details, width=400, border_color="#1f4e78")
        self.entry_cn.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_details, text="Destinatar:", font=("Arial", 12), text_color="#1f4e78").grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.entry_destinatar = ctk.CTkEntry(frame_details, width=400, border_color="#1f4e78")
        self.entry_destinatar.grid(row=3, column=1, padx=10, pady=10)

        # Frame principal pentru impartirea in doua coloane
        frame_main = ctk.CTkFrame(root, fg_color="transparent")
        frame_main.pack(padx=20, pady=10, fill="both", expand=True)

        # Configuram greutatea pentru grid
        frame_main.grid_columnconfigure(0, weight=1)  # Coloana 0 ocupa spatiu proportional
        frame_main.grid_columnconfigure(1, weight=1)  # Coloana 1 ocupa spatiu proportional

        # Frame pentru materiale (stanga)
        frame_materiale_col = ctk.CTkFrame(frame_main, fg_color="#f0f0f0", corner_radius=15, height=0, width=900)
        frame_materiale_col.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Eticheta pentru sectiunea materiale
        ctk.CTkLabel(frame_materiale_col, text="Materiale", font=("Arial", 14, "bold"), text_color="#1f4e78").pack(pady=5)

        # Buton pentru adaugare materiale
        ctk.CTkButton(frame_materiale_col, text="Adauga Material", command=self.adauga_material, fg_color="#1f4e78", text_color="white").pack(pady=5)

        # Label pentru numarul de materiale adaugate
        self.label_materiale = ctk.CTkLabel(frame_materiale_col, text="Materiale adaugate: 0", font=("Arial", 12), text_color="#1f4e78")
        self.label_materiale.pack(pady=5)

        # Frame pentru lista de materiale adaugate
        self.frame_lista_materiale = ctk.CTkFrame(frame_materiale_col, fg_color="transparent", height=0)
        self.frame_lista_materiale.pack(pady=5, padx=5, fill="x")

        # Frame pentru documente (dreapta)
        frame_documente_col = ctk.CTkFrame(frame_main, fg_color="#f0f0f0", corner_radius=15, height=0, width=600)
        frame_documente_col.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Eticheta pentru sectiunea documente
        ctk.CTkLabel(frame_documente_col, text="Documente", font=("Arial", 14, "bold"), text_color="#1f4e78").pack(pady=5)

        # Buton pentru adaugare documente
        ctk.CTkButton(frame_documente_col, text="Adauga Document", command=self.adauga_document, fg_color="#1f4e78", text_color="white").pack(pady=5)

        # Buton pentru adaugare link TransferNow
        ctk.CTkButton(frame_documente_col, text="Adauga Link TransferNow", command=self.adauga_link_transfernow, fg_color="#1f4e78", text_color="white").pack(pady=5)

        # Label pentru afisarea link-ului TransferNow
        self.label_link_transfernow = ctk.CTkLabel(frame_documente_col, text="Link TransferNow: None", font=("Arial", 12), text_color="#1f4e78")
        self.label_link_transfernow.pack(pady=5)

        # Frame pentru lista de documente adaugate
        self.frame_lista_documente = ctk.CTkFrame(frame_documente_col, fg_color="transparent", height=0)
        self.frame_lista_documente.pack(pady=5, padx=5, fill="x")

        # Sectiune butoane
        frame_buttons = ctk.CTkFrame(root, corner_radius=15, fg_color="#f0f0f0")  # Gri deschis
        frame_buttons.pack(pady=20, padx=20, fill="x")

        ctk.CTkButton(frame_buttons, text="Previzualizare", command=self.previzualizare, fg_color="#0073cf", hover_color="#005bb5", text_color="white", corner_radius=15, width=200).grid(row=0, column=0, padx=10, pady=10)  # Albastru
        ctk.CTkButton(frame_buttons, text="Trimite Email", command=self.trimite_email, fg_color="#cf1b1b", hover_color="#a50000", text_color="white", corner_radius=15, width=200).grid(row=0, column=1, padx=10, pady=10)  # Rosu
        # Buton Reset
        ctk.CTkButton(frame_buttons, text="Reset", command=self.reset_fields, 
              fg_color="#808080", hover_color="#606060", text_color="white", 
              corner_radius=15, width=200).grid(row=0, column=2, padx=10, pady=10)
        # Liste
        self.materiale = []
        self.documente = []
        self.link_transfernow = ""

    def adauga_material(self):
        # Pop-up pentru introducerea numelui materialului
        material = self.pop_up_personalizat("Material", "Introduceti numele materialului:", width=350)
        if material:
            # Pop-up pentru introducerea cantitatii
            cantitate = self.pop_up_personalizat("Cantitate", f"Introduceti cantitatea pentru {material}:", width=200)
            if cantitate:
                # Pop-up pentru introducerea unitatii de masura
                unitate = self.pop_up_personalizat("Unitate de masura", f"Introduceti unitatea de masura pentru {material}:", width=150)
                if unitate:
                    # Adauga materialul in lista daca toate campurile sunt completate
                    self.materiale.append({'material': material, 'cantitate': cantitate, 'unitate_de_masura': unitate})
                    self.label_materiale.configure(text=f"Materiale adaugate: {len(self.materiale)}")
                    self.actualizeaza_lista_materiale()


    def actualizeaza_lista_materiale(self):
        # Stergem toate widget-urile existente din frame
        for widget in self.frame_lista_materiale.winfo_children():
            widget.destroy()

        # Recream lista de materiale cu un buton pentru stergere
        for idx, material in enumerate(self.materiale):
            row_frame = ctk.CTkFrame(self.frame_lista_materiale, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)

            # Text pentru material
            material_text = f"{idx + 1}. {material['material']} - {material['cantitate']} {material['unitate_de_masura']}"
            label_material = ctk.CTkLabel(row_frame, text=material_text, anchor="w", font=("Arial", 12))
            label_material.pack(side="left", padx=5, pady=2)

            # Buton X pentru stergere
            btn_delete = ctk.CTkButton(
                row_frame, 
                text="✕", 
                command=lambda i=idx: self.sterge_material(i), 
                fg_color="#cf1b1b", 
                hover_color="#a50000", 
                text_color="white", 
                width=30,
                corner_radius=5
            )
            btn_delete.pack(side="right", padx=5, pady=2)
    def sterge_material(self, index):
        """Sterge un material din lista dupa index si actualizeaza interfata."""
        if 0 <= index < len(self.materiale):
            self.materiale.pop(index)  # Sterge materialul din lista
            self.label_materiale.configure(text=f"Materiale adaugate: {len(self.materiale)}")
            self.actualizeaza_lista_materiale()  # Actualizeaza lista afisata
        


    def previzualizare(self):
        nume_licitatie = self.entry_licitatie.get()
        numar_cn = self.entry_cn.get()
        subiect = self.entry_subiect.get()
        destinatar = self.entry_destinatar.get()

        if not nume_licitatie or not numar_cn or not destinatar:
            messagebox.showwarning("Eroare", "Toate campurile sunt obligatorii!")
            return

        materiale_dict = {m['material']: {'cantitate': m['cantitate'], 'unitate_de_masura': m['unitate_de_masura']} for m in self.materiale}
        corp_mesaj = generare_mesaj(materiale_dict, nume_licitatie, numar_cn, self.documente, self.link_transfernow)

        messagebox.showinfo("Previzualizare", f"Subiect: {subiect}\n\nDestinatar: {destinatar}\n\nMesaj:\n{corp_mesaj}")
    
    def reset_fields(self):
        """Reseteaza toate campurile si listele."""
        # Reseteaza campurile text
        self.entry_subiect.delete(0, 'end')
        self.entry_licitatie.delete(0, 'end')
        self.entry_cn.delete(0, 'end')
        self.entry_destinatar.delete(0, 'end')

        # Reintroduce valoarea default
        self.entry_subiect.insert(0, "Cerere oferta")

        # Reseteaza listele si interfata
        self.materiale = []
        self.documente = []
        self.link_transfernow = ""  # Stergem link-ul TransferNow

        # Actualizam interfata
        self.label_materiale.configure(text="Materiale adaugate: 0")
        self.label_link_transfernow.configure(text="Link TransferNow: None")
        for widget in self.frame_lista_materiale.winfo_children():
            widget.destroy()
        for widget in self.frame_lista_documente.winfo_children():
            widget.destroy()

        # Setam inaltimea initiala pentru frame-uri
        self.frame_lista_materiale.configure(height=0)
        self.frame_lista_documente.configure(height=0)

        messagebox.showinfo("Reset", "Toate campurile au fost resetate!")

    def pop_up_personalizat(self, titlu, mesaj, width=300):
        """
        Creeaza o fereastra personalizata pentru input.
        :param titlu: Titlul ferestrei
        :param mesaj: Mesajul instructiv
        :param width: Latimea casetei de input
        :return: Valoarea introdusa sau None
        """
        input_value = None
    
        dialog = tkinter.Toplevel(self.root)
        dialog.iconbitmap("app_icon.ico")  # Seteaza logo-ul
        dialog.title(titlu)
        dialog.geometry("400x200")
        dialog.grab_set()  # Blocheaza interactiunea cu fereastra principala

        # Mesaj
        ctk.CTkLabel(dialog, text=mesaj, font=("Arial", 12)).pack(pady=10)

        # Caseta de input
        entry_input = ctk.CTkEntry(dialog, width=width)
        entry_input.pack(pady=10)
        dialog.after_idle(lambda: entry_input.focus()) #pune focusu pe input


        # Butoane OK si Cancel
        def confirma():
            nonlocal input_value
            input_value = entry_input.get()
            dialog.destroy()

        def anuleaza():
            dialog.destroy()

        ctk.CTkButton(dialog, text="OK", command=confirma).pack(side="left", padx=20, pady=20)
        ctk.CTkButton(dialog, text="Cancel", command=anuleaza).pack(side="right", padx=20, pady=20)

        dialog.wait_window()  # Asteapta inchiderea ferestrei
        return input_value

    def adauga_document(self):
        """Permite utilizatorului sa adauge documente."""
        fisiere = filedialog.askopenfilenames(title="Selecteaza documente", 
                                            filetypes=[("PDF files", "*.pdf"), 
                                                        ("Word files", "*.docx"), 
                                                        ("All files", "*.*")])
        if fisiere:
            for fisier in fisiere:
                self.documente.append(fisier)  # Adauga fisierul in lista
                self.afiseaza_documente()

    def afiseaza_documente(self):
        """Afiseaza documentele adaugate."""
        for widget in self.frame_lista_documente.winfo_children():
            widget.destroy()  # Sterge vechile afisari

        for index, document in enumerate(self.documente, start=1):
            row = ctk.CTkFrame(self.frame_lista_documente, fg_color="transparent")
            row.pack(fill="x", pady=2, padx=5)

            # Afisam numele fisierului
            label_doc = ctk.CTkLabel(row, text=f"{index}. {document.split('/')[-1]}", anchor="w")
            label_doc.pack(side="left", padx=5)

            # Buton pentru stergerea documentului
            btn_delete = ctk.CTkButton(row, text="X", width=30, fg_color="red", command=lambda i=index-1: self.sterge_document(i))
            btn_delete.pack(side="right", padx=5)

    def sterge_document(self, index):
        """Sterge un document din lista."""
        if 0 <= index < len(self.documente):
            self.documente.pop(index)  # Sterge documentul din lista
            self.afiseaza_documente()  # Actualizeaza afisarea

    def adauga_link_transfernow(self):
        """Permite adaugarea unui singur link TransferNow."""
        link = simpledialog.askstring("Adauga Link TransferNow", 
                                      "Introduceti link-ul TransferNow:", 
                                      parent=self.root)
        if link:
            self.link_transfernow = link  # Salvam link-ul
            self.label_link_transfernow.configure(text=f"Link TransferNow: {link}")  # Actualizam interfata        

    def trimite_email(self):
        nume_licitatie = self.entry_licitatie.get()
        numar_cn = self.entry_cn.get()
        subiect = self.entry_subiect.get()
        destinatar = self.entry_destinatar.get()

        if not nume_licitatie or not numar_cn or not destinatar:
            messagebox.showwarning("Eroare", "Toate campurile sunt obligatorii!")
            return
        
        # Lista de materiale si documente
        materiale_dict = {m['material']: {'cantitate': m['cantitate'], 'unitate_de_masura': m['unitate_de_masura']} for m in self.materiale}
        corp_mesaj = generare_mesaj(materiale_dict, nume_licitatie, numar_cn, self.documente, self.link_transfernow)

        try:
            trimite_email(destinatar, subiect, corp_mesaj, self.documente)
            messagebox.showinfo("Succes", "E-mail trimis cu succes!")
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la trimiterea e-mailului: {e}")


# Ruleaza aplicatia
if __name__ == '__main__':
    root = ctk.CTk()
    app = EmailApp(root)
    root.mainloop()
