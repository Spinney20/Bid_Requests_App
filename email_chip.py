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
        if chip in self.email_chips:
            self.email_chips.remove(chip)
        chip.destroy()

    def get_emails(self):
        return [chip.email for chip in self.email_chips]

class ScrollableEmailChipContainer(ctk.CTkFrame):
    """
    Această clasă afișează întotdeauna scroll-ul orizontal, iar conținutul (chip-urile)
    se poate mișca atunci când se dă scroll.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")
        
        # Folosim containerul original pentru a păstra designul
        self.container = EmailChipContainer(self)
        self.container.pack(fill="both", expand=True)
        if hasattr(self.container, 'entry'):
            self.container.entry.destroy()
        
        # Creăm canvas-ul pentru scroll orizontal
        self.canvas = tk.Canvas(
            self.container.inner_frame,
            height=28,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Frame-ul intern din canvas, care va conține chip-urile și Entry-ul
        self.scroll_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        
        # Bara de scroll orizontală, plasată permanent
        self.scrollbar = ctk.CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview, height=4)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=0, rely=1.0, anchor='sw', relwidth=1.0)
        
        # Adăugăm Entry-ul în scroll_frame
        self.entry = ctk.CTkEntry(
            self.scroll_frame,
            border_width=0,
            fg_color="transparent",
            height=28
        )
        self.entry.pack(side="right", fill="x", expand=True)
        self.entry.bind("<Return>", self.add_email)
        
        self.email_chips = []
        self.scroll_frame.bind("<Configure>", self.update_scrollregion)
        # Eliminăm forțarea lățimii din metoda de redimensionare:
        # self.canvas.bind("<Configure>", self.resize_canvas)
        
    # Dacă dorești poți păstra metoda resize_canvas fără linia problematică:
    def resize_canvas(self, event):
        # Comentăm linia de mai jos pentru a nu forța lățimea:
        # self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.after(5, self.update_scrollregion)
        
    def add_email(self, event=None):
        email = self.entry.get().strip()
        if email and email not in [chip.email for chip in self.email_chips]:
            chip = EmailChip(self.scroll_frame, email, self.remove_email)
            chip.pack(side="left", padx=0, pady=0)
            self.email_chips.append(chip)
            self.entry.delete(0, "end")
            self.after(5, self.update_scrollregion)
            
    def remove_email(self, chip):
        if chip in self.email_chips:
            self.email_chips.remove(chip)
        chip.destroy()
        self.after(5, self.update_scrollregion)
        
    def update_scrollregion(self, event=None):
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.scrollbar.place(relx=0, rely=1.0, anchor='sw', relwidth=1.0)
        self.scrollbar.pack(fill="x", pady=(2, 0))
                
    def get_emails(self):
        return [chip.email for chip in self.email_chips]
