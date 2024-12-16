import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def generare_mesaj(materiale, nume_licitatie, numar_cn):
    
    corp_mesaj = f'''
    Buna ziua,

    Viarom Construct intenționează să participe la licitația: 
    “{nume_licitatie}” (număr anunț: {numar_cn}).

    În acest context, am aprecia foarte mult sprijinul dumneavoastră în furnizarea unei oferte de preț pentru:
    '''
    for material, detalii in materiale.items():
        corp_mesaj += f"- {material} – {detalii['cantitate']} {detalii['unitate_de_masura']}\n"
    
    corp_mesaj += "\nCu stimă,\nViarom Construct"
    return corp_mesaj

def trimite_email(destinatar, subiect, corp_mesaj):
    """
    Trimite email folosind serverul SMTP Outlook.
    """
    email_sender = 'andrei.dobre@viarom.ro'  # adresa mail
    email_password = 'Stilpeni2023!'  # parola
    smtp_server = 'smtp.office365.com'
    smtp_port = 587

    # Creare mesaj email
    mesaj = MIMEMultipart()
    mesaj['From'] = email_sender
    mesaj['To'] = destinatar
    mesaj['Subject'] = subiect
    mesaj.attach(MIMEText(corp_mesaj, 'plain'))

    try:
        # Conectare la serverul SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_sender, email_password)

        # Trimitere email
        server.send_message(mesaj)
        server.quit()
        print("E-mail trimis cu succes!")
    except Exception as e:
        # daca avem eroare afisam asta
        print(f"Eroare la trimiterea e-mailului {e}")

if __name__ == '__main__':
    # Solicitare subiect e-mail
    subiect = input("Introduceți subiectul e-mailului (default: Cerere ofertă): ")
    if not subiect.strip():  # daca apasam enter, folosim subiectul default care este : 
        subiect = "Cerere ofertă"

    # info licitatie
    print("\nIntroduceți informațiile despre licitație:")
    nume_licitatie = input("Numele licitației: ")
    numar_cn = input("Numărul CN al licitației: ")

    # Introducerea materialelor ( + cantiate + u.m. pt fiecare material )
    print("\nIntroduceți materialele necesare (tastați 'stop' pentru a finaliza):")
    materiale = {}
    while True:
        material = input("Material: ")
        if material.lower() == 'stop':
            break
        cantitate = input(f"Cantitate pentru {material}: ")
        unitate_de_masura = input(f"Unitate de măsură pentru {material} (ex: buc, m, kg): ")
        materiale[material] = {'cantitate': cantitate, 'unitate_de_masura': unitate_de_masura}
    
    # Generare corp email
    corp_mesaj = generare_mesaj(materiale, nume_licitatie, numar_cn)
    
    # Adresa de email destinatar
    destinatar = input("\nIntroduceți adresa de e-mail a destinatarului: ")

    # previzualizare e-mail
    print("\n--- Previzualizare e-mail ---")
    print(f"Subiect: {subiect}")
    print(f"Destinatar: {destinatar}")
    print("Mesaj:")
    print(corp_mesaj)

    # Confirmare inainte de trimitere
    confirmare = input("\nDoriți să trimiteți acest e-mail? (da/nu): ").strip().lower()
    if confirmare == 'da':
        trimite_email(destinatar, subiect, corp_mesaj)
    else:
        print("E-mailul nu a fost trimis.")
