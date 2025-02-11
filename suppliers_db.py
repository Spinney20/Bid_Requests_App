import json
import os

class SuppliersDB:
    """
    Bază de date locală pe JSON, structura:
    {
      "categories": ["agregate","marcaje",...],
      "suppliers": {
        "agregate": [
          {
            "nume": "Furnizor X",
            "emails": ["a@ex.com","b@ex.com"],
            "telefoane": ["0712...","0722..."]
          },
          ...
        ],
        "marcaje": [...],
        ...
      }
    }
    """
    def __init__(self, db_path="suppliers_db.json"):
        self.db_path = db_path
        self.data = {
            "categories": [],
            "suppliers": {}
        }
        self._load_db()

    def _load_db(self):
        """Încarcă datele din fișierul JSON (dacă există), altfel inițializează cu date goale."""
        if os.path.isfile(self.db_path):
            with open(self.db_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            # Dacă nu există fișier, păstrăm structura goală
            self.data = {
                "categories": [],
                "suppliers": {}
            }
            self._save_db()

    def _save_db(self):
        """Salvează datele în fișier JSON, cu indentare și caractere speciale."""
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    # -------------- Categorii ---------------
    def get_categories(self):
        """Returnează lista de categorii stocate."""
        return self.data["categories"]

    def add_category(self, category_name):
        """Adaugă o nouă categorie dacă nu există deja."""
        if category_name not in self.data["categories"]:
            self.data["categories"].append(category_name)
            self.data["suppliers"][category_name] = []
            self._save_db()
            return True
        return False

    def remove_category(self, category_name):
        """Șterge categoria și toți furnizorii din ea."""
        if category_name in self.data["categories"]:
            self.data["categories"].remove(category_name)
            if category_name in self.data["suppliers"]:
                del self.data["suppliers"][category_name]
            self._save_db()
            return True
        return False

    # -------------- Furnizori ---------------
    def list_suppliers(self, category):
        """Returnează lista de furnizori (dicționare) dintr-o categorie."""
        return self.data["suppliers"].get(category, [])

    def add_supplier(self, category, name, emails, telefoane):
        """
        Adaugă un furnizor cu (nume, listă e-mailuri, listă telefoane) 
        în categoria specificată. Creează categoria dacă nu există.
        """
        if category not in self.data["categories"]:
            # Dacă vrei să fie auto-creată, decomentează:
            # self.add_category(category)
            # Dacă NU vrei auto-creare, returnezi fals:
            return False

        new_supplier = {
            "nume": name,
            "emails": emails,         # list[str]
            "telefoane": telefoane   # list[str]
        }
        self.data["suppliers"][category].append(new_supplier)
        self._save_db()
        return True

    def remove_supplier(self, category, name):
        """
        Șterge furnizorul cu numele = name din categoria dată.
        Returnează True dacă s-a șters, False altfel.
        """
        if category not in self.data["suppliers"]:
            return False
        lista = self.data["suppliers"][category]
        for i, furnizor in enumerate(lista):
            if furnizor["nume"] == name:
                lista.pop(i)
                self._save_db()
                return True
        return False

    def update_supplier(self, category, old_name, new_name=None, new_emails=None, new_telefoane=None):
        """
        Caută furnizorul cu numele `old_name` și actualizează datele (nume, emailuri, telefoane).
        Orice parametru None înseamnă că nu se schimbă.
        Returnează True dacă a reușit, False altfel.
        """
        if category not in self.data["suppliers"]:
            return False
        for furnizor in self.data["suppliers"][category]:
            if furnizor["nume"] == old_name:
                if new_name is not None:
                    furnizor["nume"] = new_name
                if new_emails is not None:
                    furnizor["emails"] = new_emails
                if new_telefoane is not None:
                    furnizor["telefoane"] = new_telefoane
                self._save_db()
                return True
        return False
