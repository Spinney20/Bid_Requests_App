import customtkinter as ctk

class EmailChip(ctk.CTkFrame):
    def __init__(self, master, email, remove_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.email = email
        self.remove_callback = remove_callback

        # Stil general pentru "chip"
        self.configure(fg_color="#d0d0d0", corner_radius=10)  # Aici fără padx și pady

        # Label pentru afișarea emailului
        self.label = ctk.CTkLabel(self, text=email, font=("Arial", 10), fg_color="#d0d0d0")
        self.label.pack(side="left", padx=(5,2))

        # Buton mic de ștergere (X)
        self.btn_remove = ctk.CTkButton(self, text="x", width=15, height=15, 
                                        font=("Arial", 8), fg_color="red", 
                                        corner_radius=7, command=self.remove)
        self.btn_remove.pack(side="right", padx=(0,5))

    def remove(self):
        if self.remove_callback:
            self.remove_callback(self)
        self.destroy()

class EmailChipContainer(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.email_chips = []

        # Setăm înălțimea fixă (34px este default pentru CTkEntry)
        self.configure(
            fg_color="white", 
            corner_radius=7, 
            border_width=2, 
            border_color="#1f4e78",
            height=28  # Înălțime fixă
        )
        self.pack_propagate(False)  # Blocăm redimensionarea automată

        # Cadru intern pentru aliniere corectă
        self.inner_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.inner_frame.pack(fill="both", padx=4, pady=2)

        # Câmpul de introducere (fără bordură și cu înălțime redusă)
        self.entry = ctk.CTkEntry(
            self.inner_frame, 
            border_width=0, 
            fg_color="transparent",
            height=28  # Asigură aliniere verticală
        )
        self.entry.pack(side="right", fill="x", expand=True, padx=0, pady=0)
        self.entry.bind("<Return>", self.add_email)

    def add_email(self, event=None):
        email = self.entry.get().strip()
        if email and email not in [chip.email for chip in self.email_chips]:
            chip = EmailChip(self.inner_frame, email, self.remove_email)
            chip.pack(side="left", padx=0, pady=0)  # Eliminăm padding-ul vertical
            self.email_chips.append(chip)
            self.entry.delete(0, "end")

    def remove_email(self, chip):
        self.email_chips.remove(chip)
        chip.destroy()

    def get_emails(self):
        return [chip.email for chip in self.email_chips]