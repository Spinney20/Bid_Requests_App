import customtkinter as ctk
import tkinter
from tkinter import simpledialog, messagebox, filedialog
from PIL import Image
from mail import generare_mesaj, trimite_email

class EmailApp:
    def __init__(self, root):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = root
        self.root.title("Cerere de Oferta - Personalizat")
        self.root.geometry("700x700")
        self.root.resizable(True, True)

        self.root.iconbitmap("app_icon.ico")

        # Logo
        logo_frame = ctk.CTkFrame(root, fg_color="transparent")
        logo_frame.pack(pady=10)

        logo_image = ctk.CTkImage(
            light_image=Image.open("logo.png"),
            size=(250, 50)
        )
        logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="", fg_color="transparent")
        logo_label.pack()

        # Detalii generale
        frame_details = ctk.CTkFrame(root, corner_radius=15, fg_color="#f0f0f0")
        frame_details.pack(pady=20, padx=20, fill="x")

        ctk.CTkLabel(frame_details, text="Subiect:", font=("Arial", 12), text_color="#1f4e78").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.entry_subiect = ctk.CTkEntry(frame_details, width=400, border_color="#1f4e78")
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

        # Frame principal
        frame_main = ctk.CTkFrame(root, fg_color="transparent")
        frame_main.pack(padx=20, pady=10, fill="both", expand=True)

        frame_main.grid_columnconfigure(0, weight=1)
        frame_main.grid_columnconfigure(1, weight=1)

        # Materiale
        frame_materiale_col = ctk.CTkFrame(frame_main, fg_color="#f0f0f0", corner_radius=15)
        frame_materiale_col.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(frame_materiale_col, text="Materiale", font=("Arial", 14, "bold"), text_color="#1f4e78").pack(pady=5)
        ctk.CTkButton(frame_materiale_col, text="Adauga Material", command=self.adauga_material, fg_color="#1f4e78", text_color="white").pack(pady=5)
        self.label_materiale = ctk.CTkLabel(frame_materiale_col, text="Materiale adaugate: 0", font=("Arial", 12), text_color="#1f4e78")
        self.label_materiale.pack(pady=5)

        self.frame_lista_materiale = ctk.CTkFrame(frame_materiale_col, fg_color="transparent", height=0)
        self.frame_lista_materiale.pack(pady=5, padx=5, fill="x")

        # Documente
        frame_documente_col = ctk.CTkFrame(frame_main, fg_color="#f0f0f0", corner_radius=15)
        frame_documente_col.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        ctk.CTkLabel(frame_documente_col, text="Documente", font=("Arial", 14, "bold"), text_color="#1f4e78").pack(pady=5)
        ctk.CTkButton(frame_documente_col, text="Adauga Document", command=self.adauga_document, fg_color="#1f4e78", text_color="white").pack(pady=5)
        ctk.CTkButton(frame_documente_col, text="Adauga Link TransferNow", command=self.adauga_link_transfernow, fg_color="#1f4e78", text_color="white").pack(pady=5)
        self.label_link_transfernow = ctk.CTkLabel(frame_documente_col, text="Link TransferNow: None", font=("Arial", 12), text_color="#1f4e78")
        self.label_link_transfernow.pack(pady=5)

        self.frame_lista_documente = ctk.CTkFrame(frame_documente_col, fg_color="transparent", height=0)
        self.frame_lista_documente.pack(pady=5, padx=5, fill="x")

        # Butoane
        frame_buttons = ctk.CTkFrame(root, corner_radius=15, fg_color="#f0f0f0")
        frame_buttons.pack(pady=20, padx=20, fill="x")

        ctk.CTkButton(frame_buttons, text="Previzualizare", command=self.previzualizare,
                      fg_color="#0073cf", hover_color="#005bb5",
                      text_color="white", corner_radius=15, width=200).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkButton(frame_buttons, text="Trimite Email", command=self.trimite_email,
                      fg_color="#cf1b1b", hover_color="#a50000",
                      text_color="white", corner_radius=15, width=200).grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkButton(frame_buttons, text="Reset", command=self.reset_fields,
                      fg_color="#808080", hover_color="#606060", text_color="white", 
                      corner_radius=15, width=200).grid(row=0, column=2, padx=10, pady=10)

        self.materiale = []
        self.documente = []
        self.link_transfernow = ""

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

            material_text = f"{idx + 1}. {material['material']} - {material['cantitate']} {material['unitate_de_masura']}"
            label_material = ctk.CTkLabel(row_frame, text=material_text, anchor="w", font=("Arial", 12))
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

    def previzualizare(self):
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
        corp_mesaj = generare_mesaj(materiale_dict, nume_licitatie, numar_cn, self.documente, self.link_transfernow)

        messagebox.showinfo("Previzualizare", f"Subiect: {subiect}\n\nDestinatar: {destinatar}\n\nMesaj:\n{corp_mesaj}")

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

    def pop_up_personalizat(self, titlu, mesaj, width=300):
        input_value = None
        dialog = tkinter.Toplevel(self.root)
        dialog.iconbitmap("app_icon.ico")
        dialog.title(titlu)
        dialog.geometry("400x200")
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

        ctk.CTkButton(dialog, text="OK", command=confirma).pack(side="left", padx=20, pady=20)
        ctk.CTkButton(dialog, text="Cancel", command=anuleaza).pack(side="right", padx=20, pady=20)

        dialog.wait_window()
        return input_value

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

            label_doc = ctk.CTkLabel(row, text=f"{index}. {document.split('/')[-1]}", anchor="w")
            label_doc.pack(side="left", padx=5)

            btn_delete = ctk.CTkButton(row, text="X", width=30, fg_color="red",
                                       command=lambda i=index-1: self.sterge_document(i))
            btn_delete.pack(side="right", padx=5)

    def sterge_document(self, index):
        if 0 <= index < len(self.documente):
            self.documente.pop(index)
            self.afiseaza_documente()

    def adauga_link_transfernow(self):
        link = simpledialog.askstring("Adauga Link TransferNow", 
                                      "Introduceti link-ul TransferNow:", 
                                      parent=self.root)
        if link:
            self.link_transfernow = link
            self.label_link_transfernow.configure(text=f"Link TransferNow: {link}")

    def trimite_email(self):
        """
        Când se apasă butonul "Trimite Email", se deschide
        un mini-editor (tk.Text) care permite formatare cu tag-uri
        suprapuse (bold, italic, underline, familie, mărime).
        """
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
        corp_mesaj_initial = generare_mesaj(
            materiale_dict, nume_licitatie, numar_cn, 
            self.documente, self.link_transfernow
        )

        # Fereastra de previzualizare
        preview_window = ctk.CTkToplevel(self.root)
        preview_window.title("Mini-editor & Previzualizare Email")
        preview_window.geometry("800x600")
        preview_window.grab_set()

        toolbar_frame = ctk.CTkFrame(preview_window, fg_color="#d0d0d0")
        toolbar_frame.pack(side="top", fill="x", pady=5)

        # Frame pt text
        text_editor_frame = ctk.CTkFrame(preview_window, fg_color="white")
        text_editor_frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tkinter.Scrollbar(text_editor_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.text_editor = tkinter.Text(
            text_editor_frame, 
            wrap="word",
            font=("Arial", 12),
            undo=True,
            yscrollcommand=scrollbar.set
        )
        self.text_editor.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.text_editor.yview)

        # Inserăm textul inițial
        self.text_editor.insert("1.0", corp_mesaj_initial)

        # Butoane B / I / U => toggling
        btn_bold = ctk.CTkButton(toolbar_frame, text="B", width=40, fg_color="#333333", text_color="white",
                                 command=lambda: self.toggle_style("bold"))
        btn_bold.pack(side="left", padx=5)

        btn_italic = ctk.CTkButton(toolbar_frame, text="I", width=40, fg_color="#333333", text_color="white",
                                   command=lambda: self.toggle_style("italic"))
        btn_italic.pack(side="left", padx=5)

        btn_underline = ctk.CTkButton(toolbar_frame, text="U", width=40, fg_color="#333333", text_color="white",
                                      command=lambda: self.toggle_style("underline"))
        btn_underline.pack(side="left", padx=5)

        # Font Families
        font_families = ["Arial", "Calibri", "Times New Roman", "Helvetica", "Courier"]
        self.selected_font = ctk.StringVar(value=font_families[0])
        font_combo = ctk.CTkComboBox(
            toolbar_frame, 
            values=font_families,
            command=lambda e: self.apply_font_family(),
            variable=self.selected_font
        )
        font_combo.pack(side="left", padx=10)

        # Font Sizes
        font_sizes = ["10", "12", "14", "16", "18", "20", "24", "28"]
        self.selected_size = ctk.StringVar(value="12")
        size_combo = ctk.CTkComboBox(
            toolbar_frame, 
            values=font_sizes,
            command=lambda e: self.apply_font_family(size=True),
            variable=self.selected_size
        )
        size_combo.pack(side="left", padx=10)

        # Buton Trimite
        btn_send = ctk.CTkButton(preview_window, text="Trimite",
                                 command=lambda: self.send_from_editor(destinatar, subiect))
        btn_send.pack(side="left", padx=20, pady=10)

        # Buton Renunta
        def cancel_preview():
            preview_window.destroy()

        btn_cancel = ctk.CTkButton(preview_window, text="Renunta", command=cancel_preview)
        btn_cancel.pack(side="right", padx=20, pady=10)

    # ---------------------------------------------------
    # Functii pentru a combina totul intr-un singur tag
    # ---------------------------------------------------
    def toggle_style(self, style_word):
        """Adaugă / scoate (bold/italic/underline) pe textul selectat, păstrând familia și mărimea curente."""
        start, end = self._get_selection()
        if not start:
            return
        fam, size, styles = self._get_current_font_info(start)
        if style_word in styles:
            styles.remove(style_word)
        else:
            styles.add(style_word)
        self._apply_combined_tag(start, end, fam, size, styles)

    def apply_font_family(self, size=False):
        """Schimbă familia sau mărimea, dar păstrează stilurile (bold/italic/underline)."""
        start, end = self._get_selection()
        if not start:
            return
        fam, sz, styles = self._get_current_font_info(start)
        if size:
            # user a schimbat marimea
            newsize = self.selected_size.get()
            self._apply_combined_tag(start, end, fam, newsize, styles)
        else:
            # user a schimbat familia
            newfam = self.selected_font.get()
            self._apply_combined_tag(start, end, newfam, sz, styles)

    def _get_selection(self):
        try:
            start = self.text_editor.index("sel.first")
            end   = self.text_editor.index("sel.last")
            return (start, end)
        except:
            return (None, None)

    def _get_current_font_info(self, index):
        """
        Returnează (family, size, set_styles) pt. textul de la 'index'.
        Căutăm un tag de tip 'font_Arial_14_bold_italic' și îl parsam.
        """
        tags_here = self.text_editor.tag_names(index)
        family = "Arial"
        size   = "12"
        styles = set()
        for t in tags_here:
            if t.startswith("font_"):
                parts = t.split("_")
                # ex: ["font","Arial","14","bold","italic"]
                if len(parts) >= 3:
                    family = parts[1]
                    size   = parts[2]
                for extra in parts[3:]:
                    styles.add(extra)
        return (family, size, styles)

    def _apply_combined_tag(self, start, end, family, size, styles):
        """
        Construiește un tag unic: 'font_{family}_{size}_[bold]_[italic]_[underline]'
        Reconfigurează font=(..., "bold italic"...) și îl aplică pe selecție.
        Elimină orice alt tag 'font_...' din interval.
        """
        tag_name = f"font_{family}_{size}"
        if styles:
            tag_name += "_" + "_".join(styles)  # ex. font_Arial_14_bold_italic
        style_str = " ".join(list(styles))  # ex. "bold italic"

        if style_str:
            f = (family, int(size), style_str)
        else:
            f = (family, int(size))

        # Definim / redefinim tag-ul
        self.text_editor.tag_configure(tag_name, font=f)

        # Scoatem orice alt tag 'font_...' din interval (ca să nu se calce)
        all_tags = self.text_editor.tag_names()
        font_tags = [xx for xx in all_tags if xx.startswith("font_")]
        for ft in font_tags:
            self.text_editor.tag_remove(ft, start, end)

        # Aplicăm noul tag
        self.text_editor.tag_add(tag_name, start, end)

    # ---------------------------------------------------
    def send_from_editor(self, destinatar, subiect):
        corp_html = self.convert_text_to_html(self.text_editor)
        try:
            trimite_email(destinatar, subiect, corp_html, self.documente, html=True)
            messagebox.showinfo("Succes", "E-mail trimis cu succes!")
            self.text_editor.master.destroy()
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la trimiterea e-mailului: {e}")

    def convert_text_to_html(self, text_widget):
        end_index = text_widget.index("end-1c")
        html_output = ""
        current_tags = set()

        def close_all_tags(tags):
            closing = ""
            if "font_" in " ".join(tags):
                closing += "</span>"
            if "underline" in tags:
                closing += "</u>"
            if "italic" in tags:
                closing += "</i>"
            if "bold" in tags:
                closing += "</b>"
            return closing

        def open_tags(tags):
            opening = ""
            if "bold" in tags:
                opening += "<b>"
            if "italic" in tags:
                opening += "<i>"
            if "underline" in tags:
                opening += "<u>"
            font_tags = [t for t in tags if t.startswith("font_")]
            if font_tags:
                ftag = font_tags[-1]
                parts = ftag.split("_", 2)  # ex. ["font", "Arial", "14_bold_italic"]
                if len(parts) == 3:
                    # parts[2] = "14_bold_italic" => despărțim iar
                    subparts = parts[2].split("_")
                    # subparts[0] e "14", restul pot fi "bold","italic"
                    font_family = parts[1]
                    font_size = subparts[0]
                    opening += f'<span style="font-family:{font_family}; font-size:{font_size}px;">'
                else:
                    opening += "<span>"
            return opening

        idx = text_widget.index("1.0")
        while True:
            if idx == end_index:
                if current_tags:
                    html_output += close_all_tags(current_tags)
                break

            c = text_widget.get(idx)
            tags_here = set(text_widget.tag_names(idx))

            if tags_here != current_tags:
                # Închidem tot ce era înainte
                if current_tags:
                    html_output += close_all_tags(current_tags)
                # Deschidem ce e nou
                if tags_here:
                    html_output += open_tags(tags_here)
                current_tags = tags_here

            if c == "&":
                html_output += "&amp;"
            elif c == "<":
                html_output += "&lt;"
            elif c == ">":
                html_output += "&gt;"
            elif c == "\n":
                html_output += "<br>"
            else:
                html_output += c

            idx = text_widget.index(f"{idx}+1c")

        final_html = f"""<html>
<head>
<meta charset="utf-8"/>
</head>
<body>
{html_output}
</body>
</html>"""
        return final_html


# Ruleaza aplicatia
if __name__ == '__main__':
    root = ctk.CTk()
    app = EmailApp(root)
    root.mainloop()
