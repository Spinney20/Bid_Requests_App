import customtkinter as ctk
import os
import webbrowser
from tkinter import filedialog

class DocumenteSection:
    def __init__(self, parent, label_link_transfernow, frame_lista_documente):
        """
        parent: instanța principală (ex. EmailApp) – folosit pentru apeluri comune (ex. pop-up-uri)
        label_link_transfernow: eticheta pentru afișarea link-ului TransferNow
        frame_lista_documente: containerul scrollabil unde se afișează lista de documente
        """
        self.parent = parent
        self.label_link_transfernow = label_link_transfernow
        self.frame_lista_documente = frame_lista_documente
        self.documente = []
        self.link_transfernow = ""

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
            row.pack(fill="x", pady=0, padx=5)

            # Obținem numele fișierului și verificăm lungimea
            nume_document = os.path.basename(document)
            if len(nume_document) > 40:
                nume_document = nume_document[:37] + "..."  # Trunchiere

            label_doc = ctk.CTkLabel(row, text=f"{index}. {nume_document}", anchor="w")
            label_doc.pack(side="left", padx=5)

            btn_delete = ctk.CTkButton(
                row,
                text="✕",
                command=lambda i=index-1: self.sterge_document(i),
                fg_color="#cf1b1b",
                hover_color="#a50000",
                text_color="white",
                width=10,        # Buton mai mic
                height=10,       # Înălțime mai mică
                corner_radius=3, # Colțuri mai puțin rotunjite
                font=("Arial", 13) # Font mai mic
            )
            btn_delete.pack(side="right", padx=5, pady=2)

    def sterge_document(self, index):
        if 0 <= index < len(self.documente):
            self.documente.pop(index)
            self.afiseaza_documente()

    def adauga_link_transfernow(self):
        link = self.parent.pop_up_personalizat("Link", "Adaugati link ul de transfer:", width=200)
        if link:
            self.link_transfernow = link
            self.label_link_transfernow.configure(
                text="Link Transfer: ADAUGAT (Click aici)",
                font=("Arial", 12, "bold", "underline"),
                text_color="#1f4e78",
                cursor="hand2"
            )
            # Elimină bindingurile anterioare
            self.label_link_transfernow.unbind("<Button-1>")
            self.label_link_transfernow.unbind("<Enter>")
            self.label_link_transfernow.unbind("<Leave>")
            # Adaugă binding pentru deschidere link
            self.label_link_transfernow.bind("<Button-1>", lambda e: webbrowser.open(link))
            self.label_link_transfernow.bind("<Enter>", lambda e: self.label_link_transfernow.configure(text_color="#ff6600"))
            self.label_link_transfernow.bind("<Leave>", lambda e: self.label_link_transfernow.configure(text_color="#1f4e78"))
        else:
            self.link_transfernow = ""
            self.label_link_transfernow.configure(
                text="Link Transfer: None",
                font=("Arial", 12),
                text_color="#1f4e78",
                cursor="arrow"
            )
            self.label_link_transfernow.unbind("<Button-1>")
            self.label_link_transfernow.unbind("<Enter>")
            self.label_link_transfernow.unbind("<Leave>")

    def reset_documente(self):
        self.documente.clear()
        self.link_transfernow = ""
        self.label_link_transfernow.configure(
            text="Link Transfer: None",
            font=("Arial", 12),
            text_color="#1f4e78",
            cursor="arrow"
        )
        self.label_link_transfernow.unbind("<Button-1>")
        self.label_link_transfernow.unbind("<Enter>")
        self.label_link_transfernow.unbind("<Leave>")
        for widget in self.frame_lista_documente.winfo_children():
            widget.destroy()
