
import customtkinter as ctk
import tkinter
from tkinter import messagebox
from mail import trimite_email

class EmailEditor:
    def __init__(self, root, destinatar, subiect, initial_message, documente, cc=None):
        self.root = root
        self.destinatar = destinatar
        self.subiect = subiect
        self.initial_message = initial_message
        self.documente = documente
        self.create_editor()
        self.cc = cc

    def create_editor(self):
        # Creează fereastra de previzualizare/mini-editor
        self.preview_window = ctk.CTkToplevel(self.root)
        self.preview_window.title("Mini-editor & Previzualizare Email")
        self.preview_window.geometry("800x600")
        self.preview_window.grab_set()

        # Toolbar-ul pentru stilizare
        self.toolbar_frame = ctk.CTkFrame(self.preview_window, fg_color="#d0d0d0")
        self.toolbar_frame.pack(side="top", fill="x", pady=5)

        # Frame pentru editorul de text
        self.text_editor_frame = ctk.CTkFrame(self.preview_window, fg_color="white")
        self.text_editor_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar pentru editor
        scrollbar = tkinter.Scrollbar(self.text_editor_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.text_editor = tkinter.Text(
            self.text_editor_frame,
            wrap="word",
            font=("Arial", 12),
            undo=True,
            yscrollcommand=scrollbar.set
        )
        self.text_editor.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.text_editor.yview)

        # Inserează mesajul inițial
        self.text_editor.insert("1.0", self.initial_message)

        # Butoane pentru stilizare
        btn_bold = ctk.CTkButton(self.toolbar_frame, text="B", width=40, fg_color="#333333", text_color="white",
                                 command=lambda: self.toggle_style("bold"))
        btn_bold.pack(side="left", padx=5)

        btn_italic = ctk.CTkButton(self.toolbar_frame, text="I", width=40, fg_color="#333333", text_color="white",
                                   command=lambda: self.toggle_style("italic"))
        btn_italic.pack(side="left", padx=5)

        btn_underline = ctk.CTkButton(self.toolbar_frame, text="U", width=40, fg_color="#333333", text_color="white",
                                      command=lambda: self.toggle_style("underline"))
        btn_underline.pack(side="left", padx=5)

        # Combobox pentru selectarea fonturilor
        font_families = ["Arial", "Calibri", "Times New Roman", "Helvetica", "Courier"]
        self.selected_font = ctk.StringVar(value=font_families[0])
        font_combo = ctk.CTkComboBox(self.toolbar_frame, values=font_families,
                                     command=lambda e: self.apply_font_family(),
                                     variable=self.selected_font)
        font_combo.pack(side="left", padx=10)

        # Combobox pentru selectarea mărimii fontului
        font_sizes = ["10", "12", "14", "16", "18", "20", "24", "28"]
        self.selected_size = ctk.StringVar(value="12")
        size_combo = ctk.CTkComboBox(self.toolbar_frame, values=font_sizes,
                                     command=lambda e: self.apply_font_family(size=True),
                                     variable=self.selected_size)
        size_combo.pack(side="left", padx=10)

        # Butonul de trimitere
        btn_send = ctk.CTkButton(self.preview_window, text="Trimite",
                                 command=lambda: self.send_from_editor(self.destinatar, self.subiect, self.cc))
        btn_send.pack(side="left", padx=20, pady=10)

        # Buton pentru anulare
        btn_cancel = ctk.CTkButton(self.preview_window, text="Renunță", command=self.preview_window.destroy)
        btn_cancel.pack(side="right", padx=20, pady=10)

    # --- Funcții pentru stilizarea textului ---
    def toggle_style(self, style_word):
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
        start, end = self._get_selection()
        if not start:
            return
        fam, sz, styles = self._get_current_font_info(start)
        if size:
            newsize = self.selected_size.get()
            self._apply_combined_tag(start, end, fam, newsize, styles)
        else:
            newfam = self.selected_font.get()
            self._apply_combined_tag(start, end, newfam, sz, styles)

    def _get_selection(self):
        try:
            start = self.text_editor.index("sel.first")
            end = self.text_editor.index("sel.last")
            return (start, end)
        except Exception:
            return (None, None)

    def _get_current_font_info(self, index):
        tags_here = self.text_editor.tag_names(index)
        family = "Arial"
        size = "12"
        styles = set()
        for t in tags_here:
            if t.startswith("font_"):
                parts = t.split("_")
                if len(parts) >= 3:
                    family = parts[1]
                    size = parts[2]
                for extra in parts[3:]:
                    styles.add(extra)
        return (family, size, styles)

    def _apply_combined_tag(self, start, end, family, size, styles):
        tag_name = f"font_{family}_{size}"
        if styles:
            tag_name += "_" + "_".join(styles)
        style_str = " ".join(list(styles))
        if style_str:
            f = (family, int(size), style_str)
        else:
            f = (family, int(size))
        self.text_editor.tag_configure(tag_name, font=f)
        all_tags = self.text_editor.tag_names()
        font_tags = [xx for xx in all_tags if xx.startswith("font_")]
        for ft in font_tags:
            self.text_editor.tag_remove(ft, start, end)
        self.text_editor.tag_add(tag_name, start, end)

    def send_from_editor(self, destinatar, subiect, cc):
        corp_html = self.convert_text_to_html(self.text_editor)
        try:
            trimite_email(destinatar, subiect, corp_html, self.documente, html=True, cc = cc)
            messagebox.showinfo("Succes", "E-mail trimis cu succes!")
            # Închide fereastra mini-editorului
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
                parts = ftag.split("_", 2)
                if len(parts) == 3:
                    subparts = parts[2].split("_")
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
                if current_tags:
                    html_output += close_all_tags(current_tags)
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
