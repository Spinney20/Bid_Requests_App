import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import textwrap
import os
from email import encoders

def generare_mesaj(materiale, nume_licitatie, numar_cn, documente=None, link_transfernow=None):
    """
    Genereaza corpul mesajului pentru e-mail.
    """
    import textwrap

    # Partea de inceput a mesajului
    corp_mesaj = textwrap.dedent(f"""
    Buna ziua,

    Viarom Construct intentioneaza sa participe la licitatia: 
    “{nume_licitatie}” (numar anunt: {numar_cn}).

    In acest context, am aprecia foarte mult sprijinul dumneavoastra in furnizarea unei oferte de pret pentru:
    """)
    
    # Adauga lista de materiale
    for material, detalii in materiale.items():
        corp_mesaj += f" - {material} – {detalii['cantitate']} {detalii['unitate_de_masura']}\n"

    # Adauga lista de documente daca exista
    if documente:
        corp_mesaj += "\nPentru a veni in sprijinul formularii unei oferte de pret va atasam:\n"
        for document in documente:
            corp_mesaj += f" - {document.split('/')[-1]}\n"  # Afiseaza doar numele fisierului

    if link_transfernow:
        corp_mesaj += f"\nPentru a putea formula o oferta de pret va atasam urmatoarele documente relevante in urmatorul link:\n{link_transfernow}\n"

    # Inchiderea mesajului
    corp_mesaj += "\nCu stima,\nViarom Construct"
    return corp_mesaj

def trimite_email(destinatar, subiect, corp_mesaj, documente=None, html=False, cc=None):
    email_sender = 'andrei.dobre@viarom.ro'
    email_password = 'Stilpeni2025!'
    smtp_server = 'smtp.office365.com'
    smtp_port = 587

    mesaj = MIMEMultipart()
    mesaj['From'] = email_sender
    
    # Convertim destinatar în string dacă este listă
    mesaj['To'] = ", ".join(destinatar) if isinstance(destinatar, list) else destinatar
    
    mesaj['Subject'] = subiect

    # Procesăm CC
    if cc:
        mesaj['Cc'] = ", ".join(cc) if isinstance(cc, list) else cc

    if html:
        mesaj.attach(MIMEText(corp_mesaj, 'html'))
    else:
        mesaj.attach(MIMEText(corp_mesaj, 'plain'))

    if documente:
        for fisier in documente:
            try:
                with open(fisier, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.basename(fisier)}"
                )
                mesaj.attach(part)
            except Exception as e:
                print(f"Eroare la atasarea fisierului {fisier}: {e}")

    try:
        # Combinăm TO și CC într-o listă unică
        recipients = []
        
        # Procesăm destinatarii
        if isinstance(destinatar, list):
            recipients.extend(destinatar)
        else:
            recipients.extend([addr.strip() for addr in destinatar.split(",")])
        
        # Procesăm CC
        if cc:
            if isinstance(cc, list):
                recipients.extend(cc)
            else:
                recipients.extend([addr.strip() for addr in cc.split(",")])

        # Curățăm lista de adrese duplicate/goale
        recipients = list(set([addr for addr in recipients if addr.strip()]))
        
        # Trimitem e-mailul
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_sender, email_password)
        server.send_message(mesaj, from_addr=email_sender, to_addrs=recipients)
        server.quit()
        print("E-mail trimis cu succes!")
        
    except Exception as e:
        print(f"Eroare la trimiterea e-mailului: {e}")

if __name__ == '__main__':
    # (Codul de test CLI - neschimbat)
    subiect = input("Introduceți subiectul e-mailului (default: Cerere ofertă): ")
    if not subiect.strip():
        subiect = "Cerere ofertă"

    print("\nIntroduceți informațiile despre licitație:")
    nume_licitatie = input("Numele licitației: ")
    numar_cn = input("Numărul CN al licitației: ")

    print("\nIntroduceți materialele necesare (tastați 'stop' pentru a finaliza):")
    materiale = {}
    while True:
        material = input("Material: ")
        if material.lower() == 'stop':
            break
        cantitate = input(f"Cantitate pentru {material}: ")
        unitate_de_masura = input(f"Unitate de măsură pentru {material} (ex: buc, m, kg): ")
        materiale[material] = {'cantitate': cantitate, 'unitate_de_masura': unitate_de_masura}
    
    corp_mesaj = generare_mesaj(materiale, nume_licitatie, numar_cn)
    
    destinatar = input("\nIntroduceți adresa de e-mail a destinatarului: ")

    print("\n--- Previzualizare e-mail ---")
    print(f"Subiect: {subiect}")
    print(f"Destinatar: {destinatar}")
    print("Mesaj:")
    print(corp_mesaj)

    confirmare = input("\nDoriți să trimiteți acest e-mail? (da/nu): ").strip().lower()
    if confirmare == 'da':
        trimite_email(destinatar, subiect, corp_mesaj)
    else:
        print("E-mailul nu a fost trimis.")
