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
        self.configure(fg_color="transparent", corner_radius=5)  # Am scos padx și pady

        self.email_chips = []  # Lista adreselor de email active

        # Input pentru adăugare emailuri
        self.entry = ctk.CTkEntry(self, width=300, border_color="#1f4e78")
        self.entry.pack(side="left", padx=5, pady=5)  # Mutăm padx și pady aici
        self.entry.bind("<Return>", self.add_email)  # Când apasă Enter, adaugă email

    def add_email(self, event=None):
        email = self.entry.get().strip()
        if email and email not in [chip.email for chip in self.email_chips]:  # Evită duplicatele
            chip = EmailChip(self, email, remove_callback=self.remove_email)
            chip.pack(side="left", padx=5, pady=5)  # Mutăm aici padx și pady
            self.email_chips.append(chip)
            self.entry.delete(0, "end")  # Șterge textul după adăugare

    def remove_email(self, chip):
        self.email_chips.remove(chip)

    def get_emails(self):
        return [chip.email for chip in self.email_chips]  # Returnează lista de emailuri
