import imaplib
import email
from email.mime.text import MIMEText

# Adresse email de l'expéditeur et du destinataire
from_addr = 'votre_email@gmail.com'
to_addr = 'destinataire_email@gmail.com'

# Connexion au serveur IMAP de Gmail
imap_server = 'imap.gmail.com'
imap_port = 993
imap_username = 'votre_email@gmail.com'
imap_password = 'votre_mot_de_passe'
imap_conn = imaplib.IMAP4_SSL(imap_server, imap_port)
imap_conn.login(imap_username, imap_password)

# Sélection de la boîte de réception et création d'un nouvel onglet
imap_conn.select('INBOX')
tab_name = 'PythonTest'
typ, create_response = imap_conn.create(tab_name)
print(f'Nouvel onglet créé : {tab_name}')

# Création d'un objet de message MIME et ajout du sujet, du corps et de l'expéditeur
msg = MIMEText('Le corps de votre e-mail')
msg['Subject'] = 'Le sujet de votre e-mail'
msg['From'] = from_addr
msg['To'] = to_addr

# Envoi du message et stockage dans le nouvel onglet
imap_conn.append(tab_name, '', imaplib.Time2Internaldate(time.time()), msg.as_bytes())
print('E-mail envoyé et stocké dans le nouvel onglet')

# Fermeture de la connexion
imap_conn.close()
imap_conn.logout()






def deplacement_mail(self, i, data, conn, corps) : 
    ligne=corps[4].split('-')
    depart=ligne[1]
    vols_non_traités = []
    
    if vol in vols_non_traités :                       # Si le vol est haut altitude et ne doit pas être traité

        tab_name = 'Vols haute altitude'
        typ, create_response = imap_conn.create(tab_name)
        