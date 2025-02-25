import customtkinter as ctk

class MaterialeSection:
    def __init__(self, parent, label_materiale, frame_lista_materiale):
        """
        parent: instanța principală (ex. EmailApp) – va fi folosit pentru apeluri către metode comune (ex. pop-up-uri)
        label_materiale: eticheta ce afișează numărul de materiale adăugate
        frame_lista_materiale: containerul scrollabil unde se afișează lista de materiale
        """
        self.parent = parent
        self.label_materiale = label_materiale
        self.frame_lista_materiale = frame_lista_materiale
        self.materiale = []

    def adauga_material(self):
        material = self.parent.pop_up_personalizat("Material", "Introduceti numele materialului:", width=350)
        if material:
            cantitate = self.parent.pop_up_personalizat("Cantitate", f"Introduceti cantitatea pentru {material}:", width=200)
            if cantitate:
                unitate = self.parent.pop_up_personalizat("Unitate de masura", f"Introduceti unitatea de masura pentru {material}:", width=150)
                if unitate:
                    self.materiale.append({
                        'material': material,
                        'cantitate': cantitate,
                        'unitate_de_masura': unitate
                    })
                    self.label_materiale.configure(text=f"Materiale adaugate: {len(self.materiale)}")
                    self.actualizeaza_lista_materiale()

    def actualizeaza_lista_materiale(self):
        # Ștergem widget-urile anterioare din containerul listei
        for widget in self.frame_lista_materiale.winfo_children():
            widget.destroy()
        for idx, material in enumerate(self.materiale):
            row_frame = ctk.CTkFrame(self.frame_lista_materiale, fg_color="transparent")
            row_frame.pack(fill="x", pady=0)
            
            # Preluăm denumirea materialului
            mat_name = material['material']
            # Dacă numele are 20 sau mai multe caractere, îl trunchiem după al 16-lea caracter și adăugăm "..."
            if len(mat_name) >= 24:
                mat_name = mat_name[:20] + "..."
                
            # Combinăm informațiile: numărul, denumirea (trunchiată dacă e cazul), cantitatea și unitatea de măsură
            text_mat = f"{idx + 1}. {mat_name} - {material['cantitate']} {material['unitate_de_masura']}"
            label_material = ctk.CTkLabel(row_frame, text=text_mat, anchor="w", font=("Arial", 12))
            label_material.pack(side="left", padx=5, pady=0)
            
            btn_delete = ctk.CTkButton(
            row_frame,
            text="✕",
            command=lambda i=idx: self.sterge_material(i),
            fg_color="#cf1b1b",
            hover_color="#a50000",
            text_color="white",
            width=10,        # valoare redusă
            height=10,       # adaugă și height mai mic
            corner_radius=3, # colțuri mai puțin rotunjite
            font=("Arial", 13) # font cu dimensiune mai mică
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
