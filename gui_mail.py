import customtkinter as ctk
import tkinter
from tkinter import simpledialog, messagebox, filedialog
from PIL import Image
from mail import generare_mesaj, trimite_email
from suppliers_db import SuppliersDB  # Importam clasa BDD
import os
from preview_manager import PreviewManager
from email_editor import EmailEditor

class EmailApp:
    def __init__(self, root):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = root
        self.root.title("Cerere de Oferta - Personalizat")
        self.root.geometry("700x700")
        self.root.resizable(True, True)
        self.root.iconbitmap("app_icon.ico")

        # fisiere externe
        self.preview_manager = PreviewManager(self)


        # ---------- Incarcam baza de date a furnizorilor ----------
        self.db = SuppliersDB("suppliers_db.json")

        # ---------- Logo ----------
        logo_frame = ctk.CTkFrame(root, fg_color="transparent")
        logo_frame.pack(pady=5)

        logo_image = ctk.CTkImage(
            light_image=Image.open("logo.png"),
            size=(250, 50)
        )
        logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="", fg_color="transparent")
        logo_label.pack()

        # ---------- Detalii generale ----------
        frame_details = ctk.CTkFrame(root, corner_radius=15, fg_color="#f0f0f0")
        frame_details.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(frame_details, text="Subiect:", font=("Arial", 12), text_color="#1f4e78").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.entry_subiect = ctk.CTkEntry(frame_details, width=500, border_color="#1f4e78")
        self.entry_subiect.insert(0, "Cerere oferta")
        self.entry_subiect.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame_details, text="Numele Licitatiei:", font=("Arial", 12), text_color="#1f4e78").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_licitatie = ctk.CTkEntry(frame_details, width=500, border_color="#1f4e78")
        self.entry_licitatie.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame_details, text="Numarul CN:", font=("Arial", 12), text_color="#1f4e78").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_cn = ctk.CTkEntry(frame_details, width=500, border_color="#1f4e78")
        self.entry_cn.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame_details, text="Destinatar:", font=("Arial", 12), text_color="#1f4e78").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.entry_destinatar = ctk.CTkEntry(frame_details, width=500, border_color="#1f4e78")
        self.entry_destinatar.grid(row=3, column=1, padx=10, pady=5)

        # ---------- Frame principal ----------
        frame_main = ctk.CTkFrame(root, fg_color="transparent")
        frame_main.pack(padx=20, pady=5, fill="both", expand=True)
        frame_main.grid_columnconfigure(0, weight=1)
        frame_main.grid_columnconfigure(1, weight=1)

       # ---------- Materiale ----------
        frame_materiale_col = ctk.CTkFrame(frame_main, fg_color="#f0f0f0", corner_radius=15)
        frame_materiale_col.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        # Rând pentru titlu și reset
        title_reset_frame = ctk.CTkFrame(frame_materiale_col, fg_color="transparent")
        title_reset_frame.pack(pady=(5, 0), fill="x", expand=True)

        # Titlu centrat ABSOLUT cu place()
        lbl_title = ctk.CTkLabel(
            title_reset_frame,
            text="Materiale",
            font=("Arial", 14, "bold"),
            text_color="#1f4e78"
        )
        lbl_title.place(relx=0.5, rely=0.5, anchor="center")  # Centrare matematica exacta

        # Buton reset în dreapta
        self.btn_reset_materiale = ctk.CTkButton(
            title_reset_frame,
            text="reset",
            command=self.reset_materiale,
            fg_color="#cf1b1b",
            hover_color="#a50000",
            text_color="white",
            width=20,
            height=20,
            corner_radius= 14,
            font=("Arial", 10)
        )
        self.btn_reset_materiale.pack(side="right", padx=5)

        # Buton adăugare
        ctk.CTkButton(frame_materiale_col, 
                    text="Adauga Material", 
                    command=self.adauga_material,
                    fg_color="#1f4e78", 
                    text_color="white", 
                    height=28).pack(pady=(0, 5), padx=5)

        # Contor materiale
        label_reset_frame = ctk.CTkFrame(frame_materiale_col, fg_color="transparent")
        label_reset_frame.pack(pady=(0, 5), padx=5)

        self.label_materiale = ctk.CTkLabel(
            label_reset_frame, 
            text="Materiale adaugate: 0", 
            font=("Arial", 12), 
            text_color="#1f4e78"
        )
        self.label_materiale.pack(side="left")

        # Frame lista
        self.frame_lista_materiale = ctk.CTkScrollableFrame(
            frame_materiale_col,
            fg_color="transparent",
            height=75,
            scrollbar_button_color="#f0f0f0",
            scrollbar_button_hover_color="#e0e0e0"
        )
        self.frame_lista_materiale.pack(pady=0, padx=5, fill="x", expand=False)

        # Fixează dimensiunile
        frame_materiale_col.grid_propagate(False)
        frame_materiale_col.configure(width=200)  # Ajustează dimensiunea după nevoie

        # ---------- Documente ----------
        frame_documente_col = ctk.CTkFrame(frame_main, fg_color="#f0f0f0", corner_radius=15)
        frame_documente_col.grid(row=0, column=1, padx=10, pady=0, sticky="nsew")

        # ---- Titlu + Reset ----
        title_reset_frame = ctk.CTkFrame(frame_documente_col, fg_color="transparent")
        title_reset_frame.pack(pady=(5, 0), fill="x", expand=True)

        # Titlu centrat ABSOLUT ca la Materiale
        lbl_title_doc = ctk.CTkLabel(
            title_reset_frame,
            text="Documente",
            font=("Arial", 14, "bold"),
            text_color="#1f4e78"
        )
        lbl_title_doc.place(relx=0.5, rely=0.5, anchor="center")  # Identic cu Materiale

        # Buton reset
        self.btn_reset_documente = ctk.CTkButton(
            title_reset_frame,
            text="reset",
            command=self.reset_documente,
            fg_color="#cf1b1b",
            hover_color="#a50000",
            text_color="white",
            width=20,
            height=20,
            corner_radius= 14,
            font=("Arial", 10)
        )
        self.btn_reset_documente.pack(side="right", padx=5)

        # ---- Restul codului tău original ---- 
        frame_butoane_documente = ctk.CTkFrame(frame_documente_col, fg_color="transparent")
        frame_butoane_documente.pack(pady=(0, 5), fill="x")

        # Butoanele originale
        ctk.CTkButton(frame_butoane_documente, text="Adauga Document", 
                    command=self.adauga_document, 
                    fg_color="#1f4e78", 
                    text_color="white",
                    height=28,
                    width=140).pack(side="left", padx=(30, 5))

        ctk.CTkButton(frame_butoane_documente, text="Link TransferNow", 
                    command=self.adauga_link_transfernow,
                    fg_color="#1f4e78",
                    text_color="white",
                    height=28,
                    width=140).pack(side="right", padx=(5, 30))

        # Eticheta originală transfernow
        self.label_link_transfernow = ctk.CTkLabel(
            frame_documente_col,
            text="Link TransferNow: None",
            font=("Arial", 12),
            text_color="#1f4e78"
        )
        self.label_link_transfernow.pack(pady=(0, 5))

        # Lista documente originală
        self.frame_lista_documente = ctk.CTkScrollableFrame(
            frame_documente_col,
            fg_color="transparent",
            height=75,
            scrollbar_button_color="#f0f0f0",
            scrollbar_button_hover_color="#e0e0e0"
        )
        self.frame_lista_documente.pack(pady=0, padx=0, fill="x", expand=False)

        # Forțează dimensiuni fixe
        frame_documente_col.grid_propagate(False)
        frame_documente_col.configure(height=150)

        # ---------- Butoane de jos ----------
        frame_buttons = ctk.CTkFrame(root, corner_radius=15, fg_color="#f0f0f0")
        frame_buttons.pack(pady=20, padx=20, fill="x")

        ctk.CTkButton(frame_buttons, text="Previzualizare", command=self.preview_manager.previzualizare,
              fg_color="#0073cf", hover_color="#005bb5",
              text_color="white", corner_radius=15, width=200).grid(row=1, column=0, padx=10, pady=10)

        ctk.CTkButton(frame_buttons, text="Trimite Email", command=self.trimite_email,
                      fg_color="#2f7e1b", hover_color="#286214",
                      text_color="white", corner_radius=15, width=200).grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkButton(frame_buttons, text="Reset", command=self.reset_fields,
                      fg_color="#cf1b1b", hover_color="#a50000", text_color="white", 
                      corner_radius=15, width=200).grid(row=1, column=1, padx=10, pady=10)

        # ---------- Buton GESTIONARE FURNIZORI ----------
        ctk.CTkButton(frame_buttons, text="Gestionare Furnizori", command=self.open_furnizori_manager,
                      fg_color="#808080", hover_color="#606060", text_color="white",
                      corner_radius=15, width=200).grid(row=1, column=2, padx=10, pady=10)

        # ---------- Liste ----------
        self.materiale = []
        self.documente = []
        self.link_transfernow = ""


    # -------------------------------------------------------------------------
    # Partea de MATERIALE
    # -------------------------------------------------------------------------
    def adauga_material(self):
        material = self.pop_up_personalizat("Material", "Introduceti numele materialului:", width=350)
        if material:
            cantitate = self.pop_up_personalizat("Cantitate", f"Introduceti cantitatea pentru {material}:", width=200)
            if cantitate:
                unitate = self.pop_up_personalizat("Unitate de masura", f"Introduceti unitatea de masura pentru {material}:", width=150)
                if unitate:
                    self.materiale.append({'material': material, 'cantitate': cantitate, 'unitate_de_masura': unitate})
                    self.label_materiale.configure(text=f"Materiale adaugate: {len(self.materiale)}")
                    self.actualizeaza_lista_materiale()

    def actualizeaza_lista_materiale(self):
        for widget in self.frame_lista_materiale.winfo_children():
            widget.destroy()
        for idx, material in enumerate(self.materiale):
            row_frame = ctk.CTkFrame(self.frame_lista_materiale, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)

            text_mat = f"{idx + 1}. {material['material']} - {material['cantitate']} {material['unitate_de_masura']}"
            label_material = ctk.CTkLabel(row_frame, text=text_mat, anchor="w", font=("Arial", 12))
            label_material.pack(side="left", padx=5, pady=2)

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
        if 0 <= index < len(self.materiale):
            self.materiale.pop(index)
            self.label_materiale.configure(text=f"Materiale adaugate: {len(self.materiale)}")
            self.actualizeaza_lista_materiale()

    def reset_materiale(self):
        self.materiale.clear()
        self.label_materiale.configure(text="Materiale adaugate: 0")
        for widget in self.frame_lista_materiale.winfo_children():
            widget.destroy()        

    def reset_documente(self):
        # Resetare documente
        self.documente_adaugate = []
        
        # Resetare link
        self.label_link_transfernow.configure(text="Link TransferNow: None")
        
        # Curățare lista vizuală
        for widget in self.frame_lista_documente.winfo_children():
            widget.destroy()

    def reset_fields(self):
        self.entry_subiect.delete(0, 'end')
        self.entry_licitatie.delete(0, 'end')
        self.entry_cn.delete(0, 'end')
        self.entry_destinatar.delete(0, 'end')
        self.entry_subiect.insert(0, "Cerere oferta")

        self.materiale.clear()
        self.documente.clear()
        self.link_transfernow = ""

        self.label_materiale.configure(text="Materiale adaugate: 0")
        self.label_link_transfernow.configure(text="Link TransferNow: None")

        for widget in self.frame_lista_materiale.winfo_children():
            widget.destroy()
        for widget in self.frame_lista_documente.winfo_children():
            widget.destroy()

        self.frame_lista_materiale.configure(height=0)
        self.frame_lista_documente.configure(height=0)

        messagebox.showinfo("Reset", "Toate campurile au fost resetate!")

    # -------------------------------------------------------------------------
    # Partea de ADĂUGARE DOCUMENTE
    # -------------------------------------------------------------------------
    def adauga_document(self):
        fisiere = filedialog.askopenfilenames(
            title="Selecteaza documente",
            filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx"), ("All files", "*.*")]
        )
        if fisiere:
            for fisier in fisiere:
                self.documente.append(fisier)
            self.afiseaza_documente()

    def afiseaza_documente(self):
        for widget in self.frame_lista_documente.winfo_children():
            widget.destroy()
        for index, document in enumerate(self.documente, start=1):
            row = ctk.CTkFrame(self.frame_lista_documente, fg_color="transparent")
            row.pack(fill="x", pady=2, padx=5)

            label_doc = ctk.CTkLabel(row, text=f"{index}. {os.path.basename(document)}", anchor="w")
            label_doc.pack(side="left", padx=5)

            btn_delete = ctk.CTkButton(row, text="X", width=30, fg_color="red",
                                       command=lambda i=index-1: self.sterge_document(i))
            btn_delete.pack(side="right", padx=5)

    def sterge_document(self, index):
        if 0 <= index < len(self.documente):
            self.documente.pop(index)
            self.afiseaza_documente()

    def adauga_link_transfernow(self):
        link = simpledialog.askstring("Adauga Link TransferNow", "Introduceti link-ul TransferNow:", parent=self.root)
        if link:
            self.link_transfernow = link
            self.label_link_transfernow.configure(text=f"Link TransferNow: {link}")

    # -------------------------------------------------------------------------
    # Partea de TRIMITERE EMAIL + mini-editor -> EmailEditor
    # -------------------------------------------------------------------------
    def trimite_email(self):
        nume_licitatie = self.entry_licitatie.get()
        numar_cn = self.entry_cn.get()
        subiect = self.entry_subiect.get()
        destinatar = self.entry_destinatar.get()

        if not nume_licitatie or not numar_cn or not destinatar:
            messagebox.showwarning("Eroare", "Toate campurile sunt obligatorii!")
            return

        materiale_dict = {
            m['material']: {
                'cantitate': m['cantitate'],
                'unitate_de_masura': m['unitate_de_masura']
            }
            for m in self.materiale
        }
        corp_mesaj_initial = generare_mesaj(materiale_dict, nume_licitatie, numar_cn, self.documente, self.link_transfernow)
        
        EmailEditor(self.root, destinatar, subiect, corp_mesaj_initial, self.documente)
        
    # -------------------------------------------------------------------------
    # GESTIONARE FURNIZORI (cu multiple email/telefon, update etc.)
    # -------------------------------------------------------------------------
    def open_furnizori_manager(self):
        win = ctk.CTkToplevel(self.root)
        win.title("Gestionare Furnizori")
        win.geometry("700x500")
        win.grab_set()

        # ========== FRAME sus: Adăugare / Ștergere Categorie ========== 
        top_frame = ctk.CTkFrame(win, fg_color="#e0e0e0", corner_radius=10)
        top_frame.pack(fill="x", padx=10, pady=10)

        # Entry pentru categorie nouă
        ctk.CTkLabel(top_frame, text="Categorie nouă:", font=("Arial",12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_new_cat = ctk.CTkEntry(top_frame, width=200)
        self.entry_new_cat.grid(row=0, column=1, padx=5, pady=5)

        # Buton "Adauga Categorie"
        btn_add_cat = ctk.CTkButton(top_frame, text="Adauga Categorie", fg_color="#4caf50", text_color="white",
                                    command=self.add_new_category)
        btn_add_cat.grid(row=0, column=2, padx=5, pady=5)

        # Label + combobox pentru ștergere categorie
        ctk.CTkLabel(top_frame, text="Sterge categorie:", font=("Arial",12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.var_del_cat = ctk.StringVar()
        self.combo_del_cat = ctk.CTkComboBox(top_frame, values=self.db.get_categories(),
                                             variable=self.var_del_cat)
        self.combo_del_cat.grid(row=1, column=1, padx=5, pady=5)

        btn_del_cat = ctk.CTkButton(top_frame, text="Sterge", fg_color="red", text_color="white",
                                    command=self.delete_category)
        btn_del_cat.grid(row=1, column=2, padx=5, pady=5)

        # ========== FRAME jos: Alegi o categorie + Adaugi Furnizori + Listă ========== 
        bottom_frame = ctk.CTkFrame(win, fg_color="#f0f0f0", corner_radius=10)
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 1) selectare categorie
        ctk.CTkLabel(bottom_frame, text="Selecteaza categorie:", font=("Arial",12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.var_cat_f = ctk.StringVar()
        self.combo_cat_f = ctk.CTkComboBox(bottom_frame, values=self.db.get_categories(),
                                           variable=self.var_cat_f,
                                           command=lambda e: self.refresh_suppliers_list())
        self.combo_cat_f.grid(row=0, column=1, padx=5, pady=5)

        # 2) FRAME adăugare furnizor
        add_supp_frame = ctk.CTkFrame(bottom_frame, fg_color="#ffffff", corner_radius=10)
        add_supp_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")

        ctk.CTkLabel(add_supp_frame, text="Nume furnizor:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_supp_name = ctk.CTkEntry(add_supp_frame, width=200)
        self.entry_supp_name.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(add_supp_frame, text="E-mailuri (virgulă):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_supp_emails = ctk.CTkEntry(add_supp_frame, width=300)
        self.entry_supp_emails.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(add_supp_frame, text="Telefoane (virgulă):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_supp_phones = ctk.CTkEntry(add_supp_frame, width=300)
        self.entry_supp_phones.grid(row=2, column=1, padx=5, pady=5)

        btn_add_supp = ctk.CTkButton(add_supp_frame, text="Adauga Furnizor", fg_color="#0073cf", text_color="white",
                                     command=self.add_new_supplier)
        btn_add_supp.grid(row=3, column=0, columnspan=2, pady=5)

        # 3) FRAME listă de furnizori (scrollabil, dacă vrei)
        self.frame_supp_list = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        self.frame_supp_list.grid(row=2, column=0, columnspan=2, sticky="nsew")

    # ================== CATEGORII ==========================
    def add_new_category(self):
        cat_name = self.entry_new_cat.get().strip()
        if not cat_name:
            messagebox.showwarning("Eroare", "Introduceți un nume de categorie!")
            return
        ok = self.db.add_category(cat_name)
        if ok:
            messagebox.showinfo("Succes", f"Categoria '{cat_name}' a fost adăugată.")
            # Golește entry
            self.entry_new_cat.delete(0, "end")
            # Reconfigurez ComboBox pentru ștergere + cea pentru selectarea furnizorilor
            cats = self.db.get_categories()
            self.combo_del_cat.configure(values=cats)
            self.combo_cat_f.configure(values=cats)
        else:
            messagebox.showerror("Eroare", f"Categoria '{cat_name}' există deja.")

    def delete_category(self):
        cat = self.var_del_cat.get()
        if not cat:
            messagebox.showwarning("Eroare", "Selectați o categorie de șters!")
            return
        confirm = messagebox.askyesno("Confirmare", f"Sigur ștergi categoria '{cat}'?")
        if confirm:
            ok = self.db.remove_category(cat)
            if ok:
                messagebox.showinfo("Șters", f"Categoria '{cat}' a fost ștearsă.")
                # Reconfigurăm ComboBox-uri
                cats = self.db.get_categories()
                self.combo_del_cat.configure(values=cats)
                self.combo_cat_f.configure(values=cats)
                # Golesc selecția
                self.var_del_cat.set("")
                self.var_cat_f.set("")
                # Șterg listă furnizori
                for w in self.frame_supp_list.winfo_children():
                    w.destroy()
            else:
                messagebox.showerror("Eroare", "Nu s-a putut șterge categoria.")

    # ================== FURNIZORI ==========================
    def add_new_supplier(self):
        cat = self.var_cat_f.get()
        if not cat:
            messagebox.showwarning("Eroare", "Selectați mai întâi o categorie!")
            return
        name = self.entry_supp_name.get().strip()
        if not name:
            messagebox.showwarning("Eroare", "Introduceți un nume de furnizor!")
            return
        # extrag emailuri
        emails = [x.strip() for x in self.entry_supp_emails.get().split(",") if x.strip()]
        phones = [x.strip() for x in self.entry_supp_phones.get().split(",") if x.strip()]

        ok = self.db.add_supplier(cat, name, emails, phones)
        if ok:
            messagebox.showinfo("Succes", f"Furnizorul '{name}' a fost adăugat în '{cat}'.")
            self.entry_supp_name.delete(0,"end")
            self.entry_supp_emails.delete(0,"end")
            self.entry_supp_phones.delete(0,"end")
            self.refresh_suppliers_list()
        else:
            messagebox.showerror("Eroare", "Nu s-a putut adăuga furnizorul (categorie invalidă?).")

    def refresh_suppliers_list(self):
        # curăț conținutul anterior
        for widget in self.frame_supp_list.winfo_children():
            widget.destroy()

        cat = self.var_cat_f.get()
        if not cat:
            ctk.CTkLabel(self.frame_supp_list, text="Selectați o categorie.").pack(pady=10)
            return

        furnizori = self.db.list_suppliers(cat)
        if not furnizori:
            ctk.CTkLabel(self.frame_supp_list, text="Nu există furnizori în această categorie.").pack(pady=10)
            return

        # Afișez sub formă de rânduri
        header = ctk.CTkFrame(self.frame_supp_list, fg_color="#ddd")
        header.pack(fill="x", pady=2)
        ctk.CTkLabel(header, text="Nume", width=15).grid(row=0, column=0, padx=5)
        ctk.CTkLabel(header, text="E-mailuri", width=25).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(header, text="Telefoane", width=25).grid(row=0, column=2, padx=5)

        for f in furnizori:
            rowf = ctk.CTkFrame(self.frame_supp_list, fg_color="#eee")
            rowf.pack(fill="x", pady=2)

            ctk.CTkLabel(rowf, text=f["nume"], anchor="w").grid(row=0, column=0, padx=5, pady=5)
            ctk.CTkLabel(rowf, text=", ".join(f["emails"]), anchor="w").grid(row=0, column=1, padx=5, pady=5)
            ctk.CTkLabel(rowf, text=", ".join(f["telefoane"]), anchor="w").grid(row=0, column=2, padx=5, pady=5)

            # buton stergere
            btn_del = ctk.CTkButton(rowf, text="Sterge", fg_color="red", text_color="white",
                                    command=lambda nm=f["nume"]: self.delete_supplier(cat, nm))
            btn_del.grid(row=0, column=3, padx=5, pady=5)

            # buton update
            btn_upd = ctk.CTkButton(rowf, text="Update", fg_color="#0073cf", text_color="white",
                                    command=lambda nm=f["nume"]: self.update_supplier_ui(cat, nm))
            btn_upd.grid(row=0, column=4, padx=5, pady=5)

    def delete_supplier(self, cat, name):
        confirm = messagebox.askyesno("Confirmare", f"Sigur vrei să ștergi furnizorul '{name}'?")
        if confirm:
            ok = self.db.remove_supplier(cat, name)
            if ok:
                messagebox.showinfo("Șters", f"Furnizorul '{name}' a fost șters.")
                self.refresh_suppliers_list()
            else:
                messagebox.showerror("Eroare", "Nu s-a putut șterge furnizorul.")

    def update_supplier_ui(self, cat, old_name):
        """Deschide un pop-up pentru update (nume, e-mailuri, telefoane)."""
        win = ctk.CTkToplevel(self.root)
        win.title(f"Update Furnizor - {old_name}")
        win.geometry("400x300")
        win.grab_set()

        ctk.CTkLabel(win, text=f"Update furnizor '{old_name}' in categoria '{cat}'", font=("Arial",12,"bold")).pack(pady=10)

        # date vechi
        furnizori = self.db.list_suppliers(cat)
        found = None
        for f in furnizori:
            if f["nume"] == old_name:
                found = f
                break
        if not found:
            messagebox.showerror("Eroare", "Furnizorul nu mai există.")
            win.destroy()
            return

        # Entry new name
        frm_1 = ctk.CTkFrame(win, fg_color="#f0f0f0", corner_radius=5)
        frm_1.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(frm_1, text="Nume nou:", width=15).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ent_name = ctk.CTkEntry(frm_1, width=200)
        ent_name.grid(row=0, column=1, padx=5, pady=5)
        ent_name.insert(0, found["nume"])

        # Entry emails
        ctk.CTkLabel(frm_1, text="E-mailuri:", width=15).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ent_emails = ctk.CTkEntry(frm_1, width=300)
        ent_emails.grid(row=1, column=1, padx=5, pady=5)
        ent_emails.insert(0, ", ".join(found["emails"]))

        # Entry phones
        ctk.CTkLabel(frm_1, text="Telefoane:", width=15).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ent_phones = ctk.CTkEntry(frm_1, width=300)
        ent_phones.grid(row=2, column=1, padx=5, pady=5)
        ent_phones.insert(0, ", ".join(found["telefoane"]))

        def do_update():
            new_n = ent_name.get().strip()
            new_e = [x.strip() for x in ent_emails.get().split(",") if x.strip()]
            new_p = [x.strip() for x in ent_phones.get().split(",") if x.strip()]
            ok = self.db.update_supplier(cat, old_name, 
                                         new_name=new_n, 
                                         new_emails=new_e, 
                                         new_telefoane=new_p)
            if ok:
                messagebox.showinfo("Succes", "Furnizor actualizat cu succes!")
                win.destroy()
                self.refresh_suppliers_list()
            else:
                messagebox.showerror("Eroare", "Nu s-a putut face update.")

        btn_update = ctk.CTkButton(win, text="Salveaza Modificari", fg_color="#006600", text_color="white",
                                   command=do_update)
        btn_update.pack(pady=10)

    def pop_up_personalizat(self, titlu, mesaj, width=300):
        input_value = None
        dialog = tkinter.Toplevel(self.root)
        dialog.withdraw()  # Ascundem pop-up-ul până setăm poziția corectă
        dialog.iconbitmap("app_icon.ico")
        dialog.title(titlu)
        dialog.geometry("400x200")

        # Setăm dimensiunea corectă a pop-up-ului
        popup_width = 400
        popup_height = 200

        # Ne asigurăm că fereastra principală (root) este actualizată
        self.root.update_idletasks()

        # Calculăm poziția exactă pentru centrare
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        pos_x = root_x + (root_width // 2) - (popup_width // 2)
        pos_y = root_y + (root_height // 2) - (popup_height // 2)

        # Aplicăm poziția corectă
        dialog.geometry(f"{popup_width}x{popup_height}+{pos_x}+{pos_y}")

        # Afișăm pop-up-ul doar după ce are poziția corectă
        dialog.deiconify()

        dialog.grab_set()

        ctk.CTkLabel(dialog, text=mesaj, font=("Arial", 12)).pack(pady=10)
        entry_input = ctk.CTkEntry(dialog, width=width)
        entry_input.pack(pady=10)
        dialog.after_idle(lambda: entry_input.focus())

        def confirma():
            nonlocal input_value
            input_value = entry_input.get()
            dialog.destroy()

        def anuleaza():
            dialog.destroy()

        # Bind ENTER pentru confirmare
        dialog.bind("<Return>", lambda event: confirma())

        ctk.CTkButton(dialog, text="OK", command=confirma).pack(side="left", padx=20, pady=20)
        ctk.CTkButton(dialog, text="Cancel", command=anuleaza).pack(side="right", padx=20, pady=20)

        dialog.wait_window()
        return input_value



# Ruleaza aplicatia
if __name__ == '__main__':
    root = ctk.CTk()
    app = EmailApp(root)
    root.mainloop()
