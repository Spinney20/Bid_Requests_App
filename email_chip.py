import customtkinter as ctk
import tkinter as tk

class EmailChip(ctk.CTkFrame):
    def __init__(self, master, email, remove_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.email = email
        self.remove_callback = remove_callback

        self.configure(fg_color="#d0d0d0", corner_radius=10)
        
        self.label = ctk.CTkLabel(self, text=email, font=("Arial", 9), fg_color="#d0d0d0")
        self.label.pack(side="left", padx=(5, 2))

        self.btn_remove = ctk.CTkButton(
            self, text="x", width=12, height=12, 
            font=("Arial", 8), fg_color="red", 
            corner_radius=7, command=self.remove
        )
        self.btn_remove.pack(side="right", padx=(0, 5))

    def remove(self):
        if self.remove_callback:
            self.remove_callback(self)
        self.destroy()

class EmailChipContainer(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.email_chips = []

        self.configure(
            fg_color="white", 
            corner_radius=7, 
            border_width=2, 
            border_color="#1f4e78",
            height=28
        )
        self.pack_propagate(False)

        self.inner_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.inner_frame.pack(fill="both", padx=4, pady=2)

        self.entry = ctk.CTkEntry(
            self.inner_frame, 
            border_width=0, 
            fg_color="transparent",
            height=28
        )
        self.entry.pack(side="right", fill="x", expand=True)
        self.entry.bind("<Return>", self.add_email)

    def add_email(self, event=None):
        email = self.entry.get().strip()
        if email and email not in [chip.email for chip in self.email_chips]:
            chip = EmailChip(self.inner_frame, email, self.remove_email)
            chip.pack(side="left", padx=0, pady=0)
            self.email_chips.append(chip)
            self.entry.delete(0, "end")

    def remove_email(self, chip):
        self.email_chips.remove(chip)
        chip.destroy()

    def get_emails(self):
        return [chip.email for chip in self.email_chips]

class ScrollableEmailChipContainer(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")

        # Create container and scrollbar
        self.container = EmailChipContainer(self)
        self.scrollbar = ctk.CTkScrollbar(self, orientation="horizontal", height=4)

        # Setup canvas for horizontal scrolling
        self.canvas = tk.Canvas(
            self.container.inner_frame, 
            highlightthickness=0,
            bg="white",
            height=24
        )
        self.scrollbar.configure(command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        # Replace original inner_frame content with scrolling canvas
        for child in self.container.inner_frame.winfo_children():
            child.destroy()
        
        self.canvas.pack(side="top", fill="both", expand=True)
        self.scroll_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        # Re-add entry and configure scrolling
        self.entry = ctk.CTkEntry(
            self.scroll_frame,
            border_width=0,
            fg_color="transparent",
            height=28
        )
        self.entry.pack(side="right", fill="x", expand=True)
        self.entry.bind("<Return>", self.add_email)

        self.scroll_frame.bind("<Configure>", self.update_scrollregion)

        # Pack elements
        self.container.pack(fill="both", expand=True)
        self.scrollbar.pack(fill="x", pady=(0, 2))

    def add_email(self, event=None):
        email = self.entry.get().strip()
        if email and email not in [chip.email for chip in self.container.email_chips]:
            chip = EmailChip(self.scroll_frame, email, self.remove_email)
            chip.pack(side="left", padx=0, pady=0)
            self.container.email_chips.append(chip)
            self.entry.delete(0, "end")
            self.update_scrollregion()

    def remove_email(self, chip):
        self.container.email_chips.remove(chip)
        chip.destroy()
        self.update_scrollregion()

    def update_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def get_emails(self):
        return self.container.get_emails()