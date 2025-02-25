import customtkinter as ctk
import tkinter
from tkinter import messagebox
from PIL import Image
from mail import generare_mesaj
from suppliers_db import SuppliersDB
from preview_manager import PreviewManager
from email_editor import EmailEditor
from email_chip import ScrollableEmailChipContainer

from materiale_section import MaterialeSection
from documente_section import DocumenteSection

class EmailApp:
    def __init__(self, root):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = root
        self.root.title("Cerere de Oferta - Personalizat")
        self.root.geometry("700x700")
        self.root.resizable(True, True)
        self.root.iconbitmap("app_icon.ico")

        # Fisiere externe
        self.preview_manager = PreviewManager(self)

        # ---------- Încărcăm baza de date a furnizorilor ----------
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

        # Configurăm coloanele pentru a se extinde uniform
        frame_details.grid_columnconfigure(0, weight=0)
        frame_details.grid_columnconfigure(1, weight=1)

        # Subiect
        ctk.CTkLabel(frame_details, text="Subiect:", font=("Arial", 12), text_color="#1f4e78")\
            .grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.entry_subiect = ctk.CTkEntry(frame_details, border_color="#1f4e78", fg_color="white")
        self.entry_subiect.insert(0, "Cerere oferta")
        self.entry_subiect.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Numele Licitației
        ctk.CTkLabel(frame_details, text="Numele Licitației:", font=("Arial", 12), text_color="#1f4e78")\
            .grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_licitatie = ctk.CTkEntry(frame_details, border_color="#1f4e78", fg_color="white")
        self.entry_licitatie.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Numărul CN
        ctk.CTkLabel(frame_details, text="Numărul CN:", font=("Arial", 12), text_color="#1f4e78")\
            .grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_cn = ctk.CTkEntry(frame_details, border_color="#1f4e78", fg_color="white")
        self.entry_cn.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Destinatar – etichetă și container pentru "chips"
        ctk.CTkLabel(frame_details, text="Destinatar:", font=("Arial", 12), text_color="#1f4e78")\
            .grid(row=3, column=0, sticky="w", padx=10, pady=0)
        self.destinatar_container = ScrollableEmailChipContainer(frame_details, fg_color="transparent", width=500)
        self.destinatar_container.grid(row=3, column=1, padx=10, pady=0, sticky="ew")
        self.destinatar_container.grid_propagate(False)
        self.destinatar_container.configure(width=500)

        # CC – etichetă și container pentru "chips"
        ctk.CTkLabel(frame_details, text="CC:", font=("Arial", 12), text_color="#1f4e78")\
            .grid(row=4, column=0, sticky="w", padx=10, pady=(5, 0))
        self.cc_container = ScrollableEmailChipContainer(frame_details, fg_color="transparent", width=500)
        self.cc_container.grid(row=4, column=1, padx=10, pady=0, sticky="ew")

        # ---------- Frame principal ----------
        frame_main = ctk.CTkFrame(root, fg_color="transparent")
        frame_main.pack(padx=20, pady=5, fill="both", expand=True)
        # Setăm weight-urile pentru redimensionarea dinamică (acestea se aplică la redimensionarea ferestrei)
        frame_main.grid_columnconfigure(0, weight=1)  # Materiale
        frame_main.grid_columnconfigure(1, weight=1)  # Documente

        # ---------- Materiale ----------
        frame_materiale_col = ctk.CTkFrame(frame_main, fg_color="#f0f0f0", corner_radius=15)
        frame_materiale_col.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        # Setăm dimensiunea inițială pentru Materiale: lățime de 300 pixeli și înălțime de 250 pixeli
        frame_materiale_col.configure(height=200, width=300)
        frame_materiale_col.pack_propagate(False)  # Previne redimensionarea automată în funcție de conținut

        title_reset_frame_mat = ctk.CTkFrame(frame_materiale_col, fg_color="transparent")
        title_reset_frame_mat.pack(pady=(5, 0), fill="x", expand=True)

        lbl_title = ctk.CTkLabel(
            title_reset_frame_mat,
            text="Materiale",
            font=("Arial", 14, "bold"),
            text_color="#1f4e78"
        )
        lbl_title.place(relx=0.5, rely=0.5, anchor="center")

        self.btn_reset_materiale = ctk.CTkButton(
            title_reset_frame_mat,
            text="reset",
            command=lambda: self.materiale_section.reset_materiale(),
            fg_color="#cf1b1b",
            hover_color="#a50000",
            text_color="white",
            width=20,
            height=20,
            corner_radius=14,
            font=("Arial", 10)
        )
        self.btn_reset_materiale.pack(side="right", padx=5)

        ctk.CTkButton(frame_materiale_col, 
                    text="Adauga Material", 
                    command=lambda: self.materiale_section.adauga_material(),
                    fg_color="#1f4e78", 
                    text_color="white", 
                    height=28).pack(pady=(0, 5), padx=5)

        label_reset_frame = ctk.CTkFrame(frame_materiale_col, fg_color="transparent")
        label_reset_frame.pack(pady=(0, 5), padx=5)

        self.label_materiale = ctk.CTkLabel(
            label_reset_frame, 
            text="Materiale adaugate: 0", 
            font=("Arial", 12), 
            text_color="#1f4e78"
        )
        self.label_materiale.pack(side="left")

        self.frame_lista_materiale = ctk.CTkScrollableFrame(
            frame_materiale_col,
            fg_color="transparent",
            height=75,
            scrollbar_button_color="#f0f0f0",
            scrollbar_button_hover_color="#e0e0e0"
        )
        self.frame_lista_materiale.pack(pady=0, padx=5, fill="x", expand=False)

        # ---------- Documente ----------
        frame_documente_col = ctk.CTkFrame(frame_main, fg_color="#f0f0f0", corner_radius=15)
        frame_documente_col.grid(row=0, column=1, padx=10, pady=0, sticky="nsew")

        frame_documente_col.configure(height=200, width=350)
        frame_documente_col.grid_propagate(False)  # Previne modificarea automată a dimensiunii

        title_reset_frame_doc = ctk.CTkFrame(frame_documente_col, fg_color="transparent")
        title_reset_frame_doc.pack(pady=(5, 0), fill="x", expand=True)

        lbl_title_doc = ctk.CTkLabel(
            title_reset_frame_doc,
            text="Documente",
            font=("Arial", 14, "bold"),
            text_color="#1f4e78"
        )
        lbl_title_doc.place(relx=0.5, rely=0.5, anchor="center")

        self.btn_reset_documente = ctk.CTkButton(
            title_reset_frame_doc,
            text="reset",
            command=lambda: self.documente_section.reset_documente(),
            fg_color="#cf1b1b",
            hover_color="#a50000",
            text_color="white",
            width=20,
            height=20,
            corner_radius=14,
            font=("Arial", 10)
        )
        self.btn_reset_documente.pack(side="right", padx=5)

        frame_butoane_documente = ctk.CTkFrame(frame_documente_col, fg_color="transparent")
        frame_butoane_documente.pack(pady=(0, 5), fill="x")

        ctk.CTkButton(frame_butoane_documente, text="Adauga Document", 
                    command=lambda: self.documente_section.adauga_document(), 
                    fg_color="#1f4e78", 
                    text_color="white",
                    height=28,
                    width=140).pack(side="left", padx=(30, 5))

        ctk.CTkButton(frame_butoane_documente, text="Link Transfer", 
                    command=lambda: self.documente_section.adauga_link_transfernow(),
                    fg_color="#1f4e78",
                    text_color="white",
                    height=28,
                    width=140).pack(padx=(5, 30))

        self.label_link_transfernow = ctk.CTkLabel(
            frame_documente_col,
            text="Link Transfer: None",
            font=("Arial", 12),
            text_color="#1f4e78"
        )
        self.label_link_transfernow.pack(pady=(0, 5))

        self.frame_lista_documente = ctk.CTkScrollableFrame(
            frame_documente_col,
            fg_color="transparent",
            height=75,
            scrollbar_button_color="#f0f0f0",
            scrollbar_button_hover_color="#e0e0e0"
        )
        self.frame_lista_documente.pack(pady=0, padx=0, fill="x", expand=False)

        frame_documente_col.grid_propagate(False)
        frame_documente_col.configure(height=150)

        # ---------- Instanțierea secțiunilor separate ----------
        self.materiale_section = MaterialeSection(self, self.label_materiale, self.frame_lista_materiale)
        self.documente_section = DocumenteSection(self, self.label_link_transfernow, self.frame_lista_documente)

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
    
    def reset_fields(self):
        # Resetăm câmpurile de text
        self.entry_subiect.delete(0, 'end')
        self.entry_licitatie.delete(0, 'end')
        self.entry_cn.delete(0, 'end')
        self.entry_subiect.insert(0, "Cerere oferta")
        # Resetăm secțiunile de materiale și documente
        self.materiale_section.reset_materiale()
        self.documente_section.reset_documente()    

    # -------------------------------------------------------------------------
    # Partea de TRIMITERE EMAIL + mini-editor -> EmailEditor
    # -------------------------------------------------------------------------
    def trimite_email(self):
        nume_licitatie = self.entry_licitatie.get()
        numar_cn = self.entry_cn.get()
        subiect = self.entry_subiect.get()
        destinatari = self.destinatar_container.get_emails()  # Lista de destinatari
        cc = self.cc_container.get_emails()  # Lista de CC-uri

        if not nume_licitatie or not numar_cn or not destinatari:
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
        
        # Transmiterea parametrului cc către EmailEditor
        EmailEditor(self.root, destinatari, subiect, corp_mesaj_initial, self.documente, cc)
        
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

        dialog.geometry(f"{popup_width}x{popup_height}+{pos_x}+{pos_y}")

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

        dialog.bind("<Return>", lambda event: confirma())

        ctk.CTkButton(dialog, text="OK", command=confirma).pack(side="left", padx=20, pady=20)
        ctk.CTkButton(
                dialog, 
                text="Cancel", 
                command=anuleaza, 
                fg_color="#cf1b1b",
                hover_color="#a50000",
                text_color="white"
            ).pack(side="right", padx=20, pady=20)


        dialog.wait_window()
        return input_value


# Ruleaza aplicatia
if __name__ == '__main__':
    root = ctk.CTk()
    app = EmailApp(root)
    root.mainloop()
