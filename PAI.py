# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 14:56:47 2022

@author: marti
"""

### PAI N°3 : Programme python ###



### Importation des modules ###

import imaplib, email,datetime,mailbox
from tkinter import * 
import tkinter as tk
import sqlite3
import openpyxl as xl
import time
from PIL import ImageTk,Image
### Récupération du corps des mails ###




def nouveau_xl(sheetname):
    workbook = xl.Workbook()
    workbook.save(sheetname)
    sheet = workbook.active
    sheet.title = 'Liste des vols en cours'
    

def ouverture_xl(sheetname):
    global workbook
    global sheet
    workbook = xl.load_workbook(sheetname)
    sheet = workbook[workbook.sheetnames[0]]
    
    
    

def connexion(servername):
    #gestion des mot de passe et user (introduire une table de hashage (voir double table pour plus de sécurité))
    ORG_EMAIL = "@outlook.fr" 
    usernm = "test.pai3" + ORG_EMAIL 
    passwd = "Tomblanchard3."
    conn = imaplib.IMAP4_SSL(servername)
    conn.login(usernm,passwd)
    conn.select('Inbox')
    result, data = conn.uid('search', None, "UNSEEN") # (ALL/UNSEEN)
    i = len(data[0].split())
    return(i,data,conn)


### Interface Graphique (choix des paramètres) ###        
class FenPrincipale(Tk):
    ### Action à rélaiser ne fonction du type de mail ###
    def plan_de_vol(self,corps,id_aeronef):
        conn = sqlite3.connect('/Users/thibautdejean/Desktop/vols_pai.db')
        cur = conn.cursor()
        # Identifiant aéronef
        cur.execute('''INSERT INTO Plans de vols(Aeronef) VALUE (?)''',(id_aeronef))
        
        # Identifiant aérodrome de départ
        ligne=corps[4].split('-')
        depart=ligne[1]
        cur.execute('''INSERT INTO Plans de vols(Aerodrome de depart) VALUE (?)''',(depart[0:4]))
        # Heure de départ
        cur.execute('''INSERT INTO Plans de vols(Heure de départ) VALUE (?)''',(depart[4:8]))
        # Identifiant aérodrome d'arrivée
        ligne2=corps[8].split('-')
        arrivee=ligne[1]
        cur.execute('''INSERT INTO Plans de vols(Aerodrome d'arrivee) VALUE (?)''',(arrivee[0:4]))
        # Durée du vol
        cur.execute('''INSERT INTO Plans de vols(Duree du vol) VALUE (?)''',(arrivee[5:9]))
        # Heure d'arrivée
        heure=depart[4:6]+arrivee[5:7]
        minute=depart[6:8]+arrivee[7:9]
        if minute>60:
            minute=minute-60
            heure+=1
        heure_arrivee = str(heure)+str(minute)
        cur.execute('''INSERT INTO Plans de vols(DHeure d'arrivee' VALUE (?)''',(heure_arrivee))
        print("déclaration de plan de vol")
        conn.close()
        
    def message_delai(self,corps,id_aeronef):
        ligne=corps[0].split('-')
        depart = ligne[2]
        
        conn = sqlite3.connect('/Users/thibautdejean/Desktop/vols_pai.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO Plans de Vols(Heure de départ) VALUE (?) WHERE Aeronef = ? AND Aerodrome de depart = ?", (depart[4:8],id_aeronef,depart[0:4]))
        conn.close()
        
    def message_changement(self,corps,id_aeronef):
        ligne=corps[0].split('-')
        depart = ligne[2]
        arrivee = ligne[3]
        
        conn = sqlite3.connect('/Users/thibautdejean/Desktop/vols_pai.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO Plans de Vols(Heure de départ) VALUE (?) WHERE Aeronef = (?)", (depart[4:8],id_aeronef))
        cur.execute("INSERT INTO Plans de Vols(Aerodrome de départ) VALUE (?) WHERE Aeronef = (?)", (depart[0:4],id_aeronef))
        cur.execute("INSERT INTO Plans de Vols(Heure de départ) VALUE (?) WHERE Aeronef = (?)", (arrivee,id_aeronef))
        
        conn.close()
        
    
    def message_annulation(self,corps,id_aeronef):
        #fonction à écrire
        a=True
        
    def message_depart(self,corps,id_aeronef):
        #Ligne excel
        i=2
        while sheet.cell(i, 1).value != None :
            i+=1
            
        #Couleur ligne excel :
        for row in workbook.iter_rows(min_row=1, max_col=i, max_col=6):
            for cell in row:
                cell.fill = xl.styles.PatternFill(start_color="FF00FF00", end_color="FF00FF00", patternType='solid')
        # Identifiant aéronef
        sheet.cell(i,1).value=id_aeronef
        # Identifiant aérodrome de départ
        ligne=corps[0].split('-')
        depart=ligne[2]
        sheet.cell(i,2).value=depart[0:4]
        # Heure de départ
        sheet.cell(i,3).value=depart[4:8]
        #Recuperation vol dans bdd
        conn = sqlite3.connect('/Users/thibautdejean/Desktop/vols_pai.db')
        cur = conn.cursor()
        cur.execute("SELECT Aerodrome d'arrivee, Duree du vol, Heure d'arrivee FROM Plans de vols WHERE Aeronef = ? AND Aerodrome de depart = ?", (id_aeronef,depart[0:4]))
        vol = cur.fetchone()
        #Aerodrome d'arrivee
        sheet.cell(i,4).value=vol[0]
        # Durée du vol
        sheet.cell(i,5).value=vol[1]
        duree = vol[1]
        # Heure d'arrivée
        heure=depart[4:6]+duree[0:2]
        minute=depart[6:8]+arrivee[2:4]
        if minute>60:
            minute=minute-60
            heure+=1
        heure_arrivee = str(heure)+str(minute)
        
        sheet.cell(i,6).value=heure_arrivee
        
        conn.close()
        workbook.close()
        
        
         
        
    def message_arrive(self,corps,id_aeronef):
        
        
        # SI MESSAGE PAS ARRIVÉ PASSE LA LIGNE EN ROUGE CODE A CONSERVER
        
        p=0
        while p==0 :
            for row in ws.iter_rows(values_only=True):    
                if row[1] == id_aeronef:
                    p=row[0]
       
        for row in workbook.iter_rows(min_col=p, min_row=1, max_col=p, max_col=6):
            for cell in row:
                cell.fill = xl.styles.PatternFill(start_color="FFFF0000", end_color="FFFF0000", patternType='solid')
        
        # VRAIE FONCTION MESSAGE ARRIVÉ
        p=0
        while p==0 :
            for row in ws.iter_rows(values_only=True):    
                if row[1] == id_aeronef:
                    p=row[0]
        for row in workbook.iter_rows(min_col=p, min_row=1, max_col=p, max_col=6):
            for cell in row:
                cell.empty()
                cell.fill = xl.styles.PatternFill(start_color="FFFFFFFF", end_color="FFFFFFFF", patternType='solid')
        
        
        
    def message_refus(self,corps,id_aeronef):
        #fonction à écrire
        a=True
        
    def message_acceptation(self,corps,id_aeronef):
        #fonction à écrire
        a=True
        
    def demande_plan_vol(self,corps,id_aeronef):
        #fonction à écrire
        a=True
        #envoyé pas à traiter
        
    def demande_plan_vol_complementaire(self,corps,id_aeronef):
        #fonction à écrire
        a=True
        #case 19 
        #envoyé par la base, pas à traiter
        
    def plan_de_vol_complementaire(self,corps,id_aeronef):
        #fonction à écrire
        a=True
        #
    
    def compte_rendu_survol(self,corps,id_aeronef):
        #fonction à écrire
        a=True
         #inutile       
                
    ### Reconnaissance du type de mail ###
    def reconnaissance(self, corps):
        #exemple de mail :
        # corps='\n'
        # corps+='\n'
        # corps+='FF LFXOYWYX LFXVYWYX LFBWYWYX LFWBYWYX LFMMYWYX\n\n'
        # corps+='FF LFMYZPZX LFMUZPZX LFMUZTZX LFMIZPZX \n\n' 
        # corps+='310740 LFXOYXYX\n\n'
        # corps+='(FPL-COTE44-VM \n\n'
        # corps+='-SR20/L-GOLDURYB/S\n\n'
        # corps+='-LFMY1130\n\n'
        # corps+='-N0125A005 OAT UZES SAINT HIPPOLYTTE DU FORT BEDARIEUX\n\n' 
        # corps+='-LFMU 0120 LFMI LFMV\n\n'
        # corps+='-DOF/220831 REG/COYOTE 44 OPR/FAF RMK/NPL12MY)\n\n\n\n'
        
        #on récupère la partie du mail qui nous intéresse
        corps=corps.split("(")
        #séparation du mail ligne par ligne
        corps=corps[1].split('\n')
        #la première ligne nous permet de détecter le type de message
        ligne=corps[0].split('-')
        type_message=ligne[0].strip(' ')
        id_aeronef=ligne[1]
        #on envoie vers une fonction spécifique selon le type de mail :
        if type_message=='FPL':
            self.plan_de_vol(corps,id_aeronef)
        elif type_message=='DLA':
            self.message_delai(corps,id_aeronef)
        elif type_message=='CHG':
            self.message_changement(corps,id_aeronef)
        elif type_message=='CNL':
            self.message_annulation(corps,id_aeronef)
        elif type_message=='DEP':
            self.message_depart(corps,id_aeronef)
        elif type_message=='ARR':
            self.message_arrive(corps,id_aeronef)
        elif type_message=='REFUS':
            self.message_refus(corps,id_aeronef)
        elif type_message=='ACP':
            self.message_acceptation(corps,id_aeronef)
        elif type_message=='RQP':
            self.demande_plan_vol(corps,id_aeronef)
        elif type_message=='RQS':
            self.demande_plan_vol_complementaire(corps,id_aeronef)
        elif type_message=='SPL':
            self.plan_de_vol_complementaire(corps,id_aeronef)
        elif type_message=='CRV':
            self.compte_rendu_survol(corps,id_aeronef)


    def affichage_zone(self,event):
         self.boutonValider.config(state=ACTIVE)
         i = self.__zone.curselection()
         img = ",".join([self.__zone.get(j) for j in i])
         if img=="Plan NORM":
            self.__img = ImageTk.PhotoImage(Image.open('norm.png')) 
            self.__zoneAffichage.create_image(150, 145, image=self.__img)
         elif img=="Plan LY00":
            self.__img = ImageTk.PhotoImage(Image.open('LY00.png')) 
            self.__zoneAffichage.create_image(150, 145, image=self.__img)
         elif img=="Plan LY1T":
            self.__img = ImageTk.PhotoImage(Image.open('LY1T.png')) 
            self.__zoneAffichage.create_image(150, 145, image=self.__img)
         elif img=="Plan LY10":
            self.__img = ImageTk.PhotoImage(Image.open('LY10.png')) 
            self.__zoneAffichage.create_image(150, 145, image=self.__img)
         elif img=="Plan LY11":
            self.__img = ImageTk.PhotoImage(Image.open('LY11.png')) 
            self.__zoneAffichage.create_image(150, 145, image=self.__img)
         elif img=="Plan MM1L":
            self.__img = ImageTk.PhotoImage(Image.open('MM1L.png')) 
            self.__zoneAffichage.create_image(150, 145, image=self.__img)
         elif img=="Plan TR00":
            self.__img = ImageTk.PhotoImage(Image.open('TR00.png')) 
            self.__zoneAffichage.create_image(150, 145, image=self.__img)
         elif img=="Plan TR10":
            self.__img = ImageTk.PhotoImage(Image.open('TR10.png')) 
            self.__zoneAffichage.create_image(150, 145, image=self.__img)
         elif img=="Plan TR11":
            self.__img = ImageTk.PhotoImage(Image.open('TR11.png')) 
            self.__zoneAffichage.create_image(150, 145, image=self.__img)
            
    def __init__(self,base):
         global etat
         etat=True 
         Tk.__init__(self)
         # Configuration de la base de données
         self.__conn = sqlite3.connect(base)
         # on est connecté à la base de données
         curseur=self.__conn.cursor()
         ##Pour exécuter une requête :
         # curseur.execute("")
         # curseur.fetchall()[0][0]

         self.title('Surveillance trafic aérien')
         self.configure(bg="grey")
          
          # La barre d'outils composé de 2 boutons :
         self.__barreOutils = Frame(self)
         self.__barreOutils.pack(side=BOTTOM, padx=5, pady=5)
         self.boutonValider=Button(self.__barreOutils,text='Valider')
         self.boutonValider.pack(side=LEFT, padx=5, pady=5)
         self.boutonValider.config(state=DISABLED)
         self.__QuitButton = Button(self.__barreOutils, text ='Quitter', width=13)
         self.__QuitButton.pack(side=RIGHT, padx=5, pady=5)
         self.__ZC=Frame(self,borderwidth=2,relief=GROOVE,bg='white')
         self.__ZC.pack(side=TOP,padx=5,pady=2)
        # Configuration du Label de l'en-tête qui sert à donner des indications
         self.label_enTete=Label(self.__ZC,text="Définissez le découpage du territoire :", bg='white',fg="black",font=("Arial",15))
         self.label_enTete.pack(side=LEFT, padx=20,pady=8) 
        # Configuration du choix du découpage du territoire
         self.__zone = Listbox(self.__ZC)
         self.__zone.insert(1, "Plan NORM")
         self.__zone.insert(2, "Plan LY00")
         self.__zone.insert(3, "Plan LY1T")
         self.__zone.insert(4, "Plan LY10")
         self.__zone.insert(5, "Plan LY11")
         self.__zone.insert(6, "Plan MM1L")
         self.__zone.insert(7, "Plan TR00")
         self.__zone.insert(8, "Plan TR10")
         self.__zone.insert(9, "Plan TR11")
         self.__zone.pack(padx=20,pady=8) 
         self.__zone.bind('<<ListboxSelect>>',self.affichage_zone)
        # deuxième fenêtre :
         self._fenetre=Toplevel(self)
         self._fenetre.title("Vol en cours")
         self._fenetre.geometry("1355x700")
         self._fenetre.geometry("+0+0")
         self.__barreOutils2 = Frame(self._fenetre)
         self.__barreOutils2.pack(side=BOTTOM, padx=5, pady=5)
         self.__QuitButton2 = Button(self.__barreOutils2, text ='Quitter', width=13)
         self.__QuitButton2.pack(side=RIGHT, padx=5, pady=5)
         # Configuration du Label de l'en-tête qui sert à donner des indications
         self.__ZC2=Frame(self._fenetre,borderwidth=2,relief=GROOVE,bg='white')
         self.__ZC2.pack(side=TOP,padx=5,pady=2)
         self.label_enTete2=Label(self.__ZC2,text="Trafic aérien actuel : ", bg='white',fg="black",font=("Arial",15))
         self.label_enTete2.pack(side=LEFT, padx=20,pady=8) 
         self.__QuitButton2.config(command=self.fin2)
        # Le canvas pour afficher le plan du découpage
         self.__zoneAffichage =Canvas(self, width = 300,height = 290,bg='white')  
         self.__zoneAffichage.pack()
     # Commandes associées aux boutons
         self.__QuitButton.config(command=self.fin)
         #phase de test : 
         self.boutonValider.config(command=self.nouvelle_fenetre)
         
         
    def fin(self):
         global etat
         etat=False 
         self.destroy()
         raise SystemExit
         
    def fin2(self):
        global etat
        etat=False 
        self._fenetre.destroy()
        self.destroy()
        raise SystemExit
        
### Interface Graphique (affichage des vols en cours) ###

    def nouvelle_fenetre(self):
         global etat
         #Fermeture de la première fenêtre
         self.withdraw()
         # self._fenetre.deiconify()
         self.lecture_mail()
         
         
    ### définnir un cycle qui relance la fonction à un intervalle de temps précis afin de lire les nouveaux mails.
    def lecture_mail(self):
        global etat
        servername='outlook.office365.com'
        self._fenetre.deiconify()
        ### Lecture des mails ###
        start_time = time.time()
        interval = 10 #on récupère des nouveaux mails toutes les 10 secondes
        j=0
        while etat==True:
            j+=interval
            time.sleep(start_time + j - time.time())
            (i,data,conn)=connexion(servername)
            self.mail(i,data,conn)
    
    def mail(self,i,data,conn):
        #On parcours les mails 1 par 1.
        for x in range(i):
            latest_email_uid = data[0].split()[x]
            result, email_data = conn.uid('fetch', latest_email_uid, '(RFC822)')
            # result, email_data = conn.store(num,'-FLAGS','\\Seen') 
            # this might work to set flag to seen, if it doesn't already
            raw_email = email_data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)
        
            ### informations sur le sujet du mail :
            # Header Details
            # date_tuple = email.utils.parsedate_tz(email_message['Date'])
            # if date_tuple:
            #     local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            #     local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
            # email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
            # email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
            # subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
        
            # Body details
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    corps=body.decode('UTF-8')
                    print(corps)
                    self.reconnaissance(corps)
                    # on obtient de chaîne de caractère qu'il faut maintenan traiter.
                    
                    ###Possibilité de stocker chaque mail dans un fichier txt : 
                    # file_name = "email_" + str(x) + ".txt"
                    # output_file = open(file_name, 'w')
                    # output_file.write("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" %(email_from, email_to,local_message_date, subject, body.decode('utf-8')))
                    # output_file.close()
                    
                else:
                    continue
        print("mails traités, pas de mails non lus")
                
                
### Programme Principal ###
if __name__ == '__main__':
### Création de l'interface Graphique ###
    fen = FenPrincipale("nom_base.db")
    fen.mainloop()  