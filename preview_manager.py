import tkinter
from tkinter import messagebox
from mail import generare_mesaj


class PreviewManager:
    def __init__(self, email_app):
        """
        :param email_app: Instanța clasei principale (de ex. EmailApp) care conține widget-urile necesare.
        """
        self.app = email_app

    def previzualizare(self):
        # Extragem valorile din câmpurile de intrare
        nume_licitatie = self.app.entry_licitatie.get()
        numar_cn = self.app.entry_cn.get()
        subiect = self.app.entry_subiect.get()
        destinatar = self.app.entry_destinatar.get()

        # Verificăm dacă câmpurile obligatorii sunt completate
        if not nume_licitatie or not numar_cn or not destinatar:
            messagebox.showwarning("Eroare", "Toate câmpurile sunt obligatorii!")
            return

        # Construim un dicționar pentru materiale
        materiale_dict = {
            m['material']: {
                'cantitate': m['cantitate'],
                'unitate_de_masura': m['unitate_de_masura']
            } for m in self.app.materiale
        }
        # Generăm corpul mesajului
        corp_mesaj = generare_mesaj(materiale_dict, nume_licitatie, numar_cn, self.app.documente, self.app.link_transfernow)

        # Afișăm previzualizarea
        messagebox.showinfo("Previzualizare", 
            f"Subiect: {subiect}\n\nDestinatar: {destinatar}\n\nMesaj:\n{corp_mesaj}")