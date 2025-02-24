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
