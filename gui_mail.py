import customtkinter as ctk
from tkinter import simpledialog, messagebox
from PIL import Image  # Pentru procesarea logo-ului
from mail import generare_mesaj, trimite_email  # Schimba cu numele fisierului tau

class EmailApp:
    def __init__(self, root):
        ctk.set_appearance_mode("light")  # Mod de culori: "light", "dark", "system"
        ctk.set_default_color_theme("blue")  # Tema culori de baza

        self.root = root
        self.root.title("Cerere de Oferta - Personalizat")
        self.root.geometry("600x600")
        self.root.resizable(True, True)  # Permite redimensionarea

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

        # Sectiune materiale
        frame_materiale = ctk.CTkFrame(root, corner_radius=15, fg_color="#f0f0f0")  # Gri deschis
        frame_materiale.pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(frame_materiale, text="Adauga Material", command=self.adauga_material, fg_color="#1f4e78", text_color="white", corner_radius=15).grid(row=0, column=0, padx=10, pady=10)  # Albastru
        self.label_materiale = ctk.CTkLabel(frame_materiale, text="Materiale adaugate: 0", font=("Arial", 12), text_color="#1f4e78")  # Albastru
        self.label_materiale.grid(row=0, column=1, padx=10, pady=10)

        # Sectiune butoane
        frame_buttons = ctk.CTkFrame(root, corner_radius=15, fg_color="#f0f0f0")  # Gri deschis
        frame_buttons.pack(pady=20, padx=20, fill="x")

        ctk.CTkButton(frame_buttons, text="Previzualizare", command=self.previzualizare, fg_color="#0073cf", hover_color="#005bb5", text_color="white", corner_radius=15, width=200).grid(row=0, column=0, padx=10, pady=10)  # Albastru
        ctk.CTkButton(frame_buttons, text="Trimite Email", command=self.trimite_email, fg_color="#cf1b1b", hover_color="#a50000", text_color="white", corner_radius=15, width=200).grid(row=0, column=1, padx=10, pady=10)  # Rosu

        # Lista materiale
        self.materiale = []

    def adauga_material(self):
        # Pop-up pentru introducerea numelui materialului
        material = simpledialog.askstring("Material", "Introduceti materialul:", parent=self.root)

        if material:
            # Pop-up pentru introducerea cantitatii
            cantitate = simpledialog.askstring("Cantitate", f"Introduceti cantitatea pentru {material}:", parent=self.root)

            if cantitate:
                # Pop-up pentru introducerea unitatii de masura
                unitate = simpledialog.askstring("Unitate de masura", f"Introduceti unitatea de masura pentru {material}:", parent=self.root)

                if unitate:
                    # Adaug materialul in lista daca toate campurile sunt completate
                    self.materiale.append({'material': material, 'cantitate': cantitate, 'unitate_de_masura': unitate})
                    self.label_materiale.configure(text=f"Materiale adaugate: {len(self.materiale)}")
                else:
                    messagebox.showwarning("Eroare", "Unitatea de masura este necesara!", parent=self.root)
            else:
                messagebox.showwarning("Eroare", "Cantitatea este necesara!", parent=self.root)



    def previzualizare(self):
        nume_licitatie = self.entry_licitatie.get()
        numar_cn = self.entry_cn.get()
        subiect = self.entry_subiect.get()
        destinatar = self.entry_destinatar.get()

        if not nume_licitatie or not numar_cn or not destinatar:
            messagebox.showwarning("Eroare", "Toate campurile sunt obligatorii!")
            return

        materiale_dict = {m['material']: {'cantitate': m['cantitate'], 'unitate_de_masura': m['unitate_de_masura']} for m in self.materiale}
        corp_mesaj = generare_mesaj(materiale_dict, nume_licitatie, numar_cn)

        messagebox.showinfo("Previzualizare", f"Subiect: {subiect}\n\nDestinatar: {destinatar}\n\nMesaj:\n{corp_mesaj}")

    def trimite_email(self):
        nume_licitatie = self.entry_licitatie.get()
        numar_cn = self.entry_cn.get()
        subiect = self.entry_subiect.get()
        destinatar = self.entry_destinatar.get()

        if not nume_licitatie or not numar_cn or not destinatar:
            messagebox.showwarning("Eroare", "Toate campurile sunt obligatorii!")
            return

        materiale_dict = {m['material']: {'cantitate': m['cantitate'], 'unitate_de_masura': m['unitate_de_masura']} for m in self.materiale}
        corp_mesaj = generare_mesaj(materiale_dict, nume_licitatie, numar_cn)

        try:
            trimite_email(destinatar, subiect, corp_mesaj)
            messagebox.showinfo("Succes", "E-mail trimis cu succes!")
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la trimiterea e-mailului: {e}")

# Ruleaza aplicatia
if __name__ == '__main__':
    root = ctk.CTk()
    app = EmailApp(root)
    root.mainloop()
