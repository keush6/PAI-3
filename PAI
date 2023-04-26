### PAI N°3 : Programme python ###
### Importation des modules ###
import imaplib, email,datetime
from tkinter import * 
import tkinter as tk
from tkinter import ttk
import openpyxl as xl
import sqlite3
import timepipi
from pytz import timezone
from PIL import ImageTk,Image
import re
import winsound



### Recuperation du corps des mails ###

def connexion(servername): 
    #gestion des mot de passe et user (introduire une table de hashage (voir double table pour plus de securite))
    ORG_EMAIL = "@outlook.fr" 
    usernm = "test.pai3" + ORG_EMAIL 
    passwd = "Tomblanchard3."
    conn = imaplib.IMAP4_SSL(servername)
    conn.login(usernm,passwd)
    conn.select('Inbox')
    result, data = conn.uid('search', None, "UNSEEN") # (ALL/UNSEEN)
    i = len(data[0].split())
    return(i,data,conn)


### Interface Graphique (choix des parametres) ### 
       
class FenPrincipale(Tk):
    ### Action a  relaiser ne fonction du type de mail ###
    def plan_de_vol(self,corps,id_aeronef):                 # Fonction terminee fonctionelle 
        conn = sqlite3.connect('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols_pai_3.db')
        cur = conn.cursor()

        # Identifiant aeronef
        cur.execute('''REPLACE INTO "Plans de vols"(Aeronef) VALUES (?)''',(id_aeronef,))
        
        # Identifiant aerodrome de depart
        ligne=corps[4].split('-')
        depart=ligne[1]
        cur.execute('''UPDATE "Plans de vols" SET "Aerodrome de depart" = ? WHERE Aeronef = ?''',[(depart[0:5]),id_aeronef])

        # Heure de depart
        A=depart[5:10]
        B = A[0:3] + ':' + A[3:5]

        cur.execute('''UPDATE "Plans de vols" SET "Heure de depart" = ? WHERE Aeronef = ?''',[(B),id_aeronef])

        # Identifiant aerodrome d'arrivee
        ligne2=corps[8].split('-')
        arrivee=ligne2[1]
        cur.execute('''UPDATE "Plans de vols" SET "Aerodrome d'arrivee" = ? WHERE Aeronef = ?''',[(arrivee[0:5]),id_aeronef])

        # Duree du vol
        C=arrivee[5:10]
        D = C[0:3] + ':' + C[3:5]
        cur.execute('''UPDATE "Plans de vols" SET "Duree du vol" = ? WHERE Aeronef = ?''',[(D),id_aeronef])

        # Heure d'arrivee
        heure=int(depart[6:8])+int(arrivee[6:8])
        minute=int(depart[8:10])+int(arrivee[8:10])

        if int(minute)>60:
            minute=int(minute)-60
            heure+=1
        heure_arrivee = str(heure)+str(minute)

        E = heure_arrivee[0:2] + ':' + heure_arrivee[2:4]
        
        cur.execute('''UPDATE "Plans de vols" SET "Heure d'arrivee" = ? WHERE Aeronef = ?''',[(E),id_aeronef])

        # Chemin
        
        ligne3 = corps[6].split(' ')
        ligne4 = ligne3[2:len(ligne3)]
        villes = ' '.join(ligne4)

        cur.execute('''UPDATE "Plans de vols" SET "Chemin" = ? WHERE Aeronef = ?''',[(villes),id_aeronef])

        print("declaration de plan de vol")
        conn.commit()
        conn.close()

    def ecriture_excel(self,corps, id_aeronef):             # Fonction terminee fonctionelle 
        ### Fonction qui inscrit le mail dans le fichier Excel ###
        #Ouverture du fichier
        wb = xl.load_workbook('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols.xlsx')
        feuille = wb['Vols en cours']
        #Ligne excel
        i=6
        while feuille.cell(i, 4).value != None :
            i+=1

        # Identifiant aerodrome de depart
        ligne=corps[4].split('-')
        depart=ligne[1]

        #Recuperation vol dans bdd
        conn = sqlite3.connect('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols_pai_3.db')
        cur = conn.cursor()
        cur.execute('''SELECT "Heure de depart","Duree du vol", "Aerodrome d'arrivee", "Heure d'arrivee", "Chemin" FROM "Plans de vols" WHERE Aeronef = ? ''', (id_aeronef,))
        
        vol=[]
        for ligne in cur.fetchall():
            vol=list(ligne)
        

        cur.close()
        conn.close()

        #Ecriture dans le fichier excel
        feuille.cell(i,4).value = id_aeronef
        feuille.cell(i,5).value = depart[0:5]
        feuille.cell(i,6).value = vol[0]
        feuille.cell(i,7).value = vol[1]
        feuille.cell(i,8).value = vol[2]
        feuille.cell(i,9).value = vol[3]
        feuille.cell(i,10).value = vol[4]

        #Sauvegarder
        wb.save('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols.xlsx')
               
    def message_delai(self,corps,id_aeronef):               # Fonction terminee a  tester

        #Base de donnee
        ligne=corps[4].split('-')
        depart=ligne[1]
        
        conn = sqlite3.connect('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols_pai_3.db')
        cur = conn.cursor()
        cur.execute('''UPDATE "Plans de vols" SET "Heure de depart" = ? WHERE Aeronef = ? AND "Aerodrome de depart" = ?''', (depart[5:10],id_aeronef,depart[0:5]))
        
        ligne2=corps[8].split('-')
        arrivee=ligne2[1]

        heure=int(depart[6:8])+int(arrivee[6:8])
        minute=int(depart[8:10])+int(arrivee[8:10])

        if int(minute)>60:
            minute=int(minute)-60
            heure+=1
        heure_arrivee = str(heure)+str(minute)
        
        cur.execute('''UPDATE "Plans de vols" SET "Heure d'arrivee" = ? WHERE Aeronef = ? AND "Aerodrome de depart" = ?''', (depart[5:10],id_aeronef,depart[0:5]))

        conn.commit()
        conn.close()

        #Excel   
        wb = xl.load_workbook('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols.xlsx')
        feuille = wb['Vols en cours']

        
        for row in feuille.iter_rows():
             for cell in row:
                 if cell.value == id_aeronef:
                     a = (cell.row,cell.column)
        
        feuille.cell(row=a[0],column=6).value=depart[5:10]

        feuille.cell(row=a[0],column=9).value=heure_arrivee

        wb.save('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols.xlsx')
        
    def message_changement(self,corps,id_aeronef):

        conn = sqlite3.connect('/Users/thibautdejean/Desktop/vols_pai.db')
        cur = conn.cursor()

        cur.execute('''SELECT "Duree du vol" FROM "Plans de vols WHERE Aeronef = ? ''', (id_aeronef,))
        duree=cur.fetchall()

        ligne=corps[0].split('-')
        depart = ligne[2]
        arrivee = ligne[3]
        

        heure=int(depart[6:8])+int(duree[0:2])
        minute=int(depart[8:10])+int(duree[2:4])

        if int(minute)>60:
            minute=int(minute)-60
            heure+=1
        heure_arrivee = str(heure)+str(minute)
        
        
        cur.execute('''UPDATE "Plans de vols" SET "Aerodrome de depart" = ? WHERE Aeronef = ? ''', (depart[5:10],id_aeronef))
        cur.execute('''UPDATE "Plans de vols" SET "Heure de départ" = ? WHERE Aeronef = ? ''', (depart[0:5],id_aeronef))
        cur.execute('''UPDATE "Plans de vols" SET "Aerodrome d'arrivee" = ? WHERE Aeronef = ? ''', (arrivee,id_aeronef))
        cur.execute('''UPDATE "Plans de vols" SET "Heure d'arrivee" = ? WHERE Aeronef = ? ''', (heure_arrivee,id_aeronef))
        conn.commit()
        conn.close()

        #Excel   
        wb = xl.load_workbook('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols.xlsx')
        feuille = wb['Vols en cours']


        for row in feuille.iter_rows():
             for cell in row:
                 if cell.value == id_aeronef:
                     a = (cell.row,cell.column)

        feuille.cell(row=a[0],column=5).value=depart[0:5]
        feuille.cell(row=a[0],column=6).value=depart[5:10]

        feuille.cell(row=a[0],column=8).value=arrivee
        feuille.cell(row=a[0],column=9).value=heure_arrivee
        wb.save()
       
    def message_annulation(self,corps,id_aeronef):          # Fonction terminee a  tester
        #Base de donnee
        conn = sqlite3.connect('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols_pai_3.db')
        cur = conn.cursor()

        cur.execute('''DELETE FROM "Plans de vols" WHERE Aeronef = ?''', (id_aeronef,))

        conn.commit()
        conn.close()

        #Fichier excel
        wb = xl.load_workbook('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols.xlsx')
        feuille = wb['Vols en cours']

        
        for row in feuille.iter_rows():
             for cell in row:
                 if cell.value == id_aeronef:
                     a = (cell.row,cell.column)
        
        for j in range(4,11):
            feuille.cell(row = a[0], column = j).value = None
            fill = xl.PatternFill(start_color='FFFFFFFF', end_color='FFFFFFFF', fill_type='solid')
            feuille.cell(row = a[0], column = j).fill = fill

        wb.save('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols.xlsx')
                       
    def message_depart(self,corps,id_aeronef):              # Fonction terminee fonctionnelle 

        conn = sqlite3.connect('/Users/thibautdejean/Desktop/vols_pai.db')
        cur = conn.cursor()
               
        # Identification de l'aeronef
        ligne=corps[0].split('-')
        b = ligne[1].split(' ')
        id = ' '+b[0][0:2]+b[0][len(b[0])-2:len(b[0])]+b[1]+' '
        print(id)

        cur.execute('''SELECT "Duree du vol" FROM "Plans de vols WHERE Aeronef = ? ''', (id,))
        duree=cur.fetchall()


        #Heure de départ et d'arrivée : 
        ligne=corps[0].split('-')
        depart = ligne[2]
    

        heure=int(depart[6:8])+int(duree[0:2])
        minute=int(depart[8:10])+int(duree[2:4])

        if int(minute)>60:
            minute=int(minute)-60
            heure+=1
        heure_arrivee = str(heure)+str(minute)
    
        # Changement de couleur sur l'excel
        wb = xl.load_workbook('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols.xlsx')
        feuille = wb['Vols en cours']

        
        a=[1,1]
        for row in feuille.iter_rows():
             for cell in row :
                 if str(cell.value) == str(id) : 
                    a = (cell.column,cell.row)
                    print(a)

        
        feuille.cell(row=a[0],column=6).value=depart[5:10]
        feuille.cell(row=a[0],column=9).value=heure_arrivee
         
        for j in range(4,11):
            fill = xl.styles.PatternFill(start_color="FF00FF00", end_color="FF00FF00", patternType='solid')            
            feuille.cell(row = a[0], column = j).fill = fill

        wb.save('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols.xlsx')

    def iter_retard_avion(self): #changements de couleur des cases a  chaque boucle 
        wb = xl.load_workbook('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols.xlsx')
        feuille = wb['Vols en cours']
        colonne_heure_arrivée = []
        couleur_heure_arrivée = []

        #on récupère le temps actuel
        temps_actuel = time.strftime("%H:%M", time.localtime())
        print(temps_actuel)
        print('juste heure' , int(temps_actuel[0:2]))

        #on récupère les heures d'arrivée et la couleur de la case
        for col in feuille.iter_cols():
            header_cell = col[4]
            if header_cell.value == "Heure d'arrivée":
                for cell in col:
                    if cell.value != None and cell.value != "Heure d'arrivée":
                        colonne_heure_arrivée.append(cell.value)
                        couleur_heure_arrivée.append(cell.fill.start_color.index[2:])

        #on compare les heures d'arrivée avec le temps actuel
        for heure in colonne_heure_arrivée:
            if (int(heure[0:2]) < int(temps_actuel[0:2])) or (int(heure[0:2]) == int(temps_actuel[0:2]) and int(heure[3:5]) < int(temps_actuel[3:5])):
                heure_retard = (int(temps_actuel[0:2]) - int(heure[0:2]))*60 + (int(temps_actuel[3:5]) - int(heure[3:5])) #en minutes
        
                if heure_retard > 15 : 
                    #on regarde si la colonne n'est pas déjà coloriée en orange
                    if couleur_heure_arrivée[colonne_heure_arrivée.index(heure)] != 'FFA500' and couleur_heure_arrivée[colonne_heure_arrivée.index(heure)] != 'FF0000' : 
                        #on colore la ligne en orange
                        fill = xl.PatternFill(start_color='FFA500', end_color='FFA500', fill_type='solid')
                        ligne = colonne_heure_arrivée.index(heure) + 1 + 5 #on ajoute 5 car les 5 premières lignes ne sont pas des vols et 1 car on commence à 0 en python
                        for j in range(1, feuille.max_column+1):
                            cell = feuille.cell(row=ligne, column=j)
                            cell.fill = fill
                        #on crée un son d'alarme 
                        winsound.PlaySound('alarm.wav', winsound.SND_FILENAME)
                if heure_retard > 30 : 
                    #on regarde si pas déjà coloriée en rouge
                    if couleur_heure_arrivée[colonne_heure_arrivée.index(heure)] != 'FF0000' : 
                        #on colore la ligne en rouge
                        fill = xl.PatternFill(start_color='FF0000', end_color='FF0000', fill_type='solid')
                        ligne = colonne_heure_arrivée.index(heure) + 1 + 5
                        for j in range(1, feuille.max_column+1):
                            cell = feuille.cell(row=ligne, column=j)
                            cell.fill = fill
                        #on crée un son d'alarme 
                        winsound.PlaySound('alarm.wav', winsound.SND_FILENAME)
                else : 
                    #on colore la ligne en vert
                    fill = xl.PatternFill(start_color='00FF00', end_color='00FF00', fill_type='solid')
                    ligne = colonne_heure_arrivée.index(heure) + 1 + 5
                    for j in range(1, feuille.max_column+1):
                        cell = feuille.cell(row=ligne, column=j)
                        cell.fill = fill
            else : 
                #on colore la ligne en vert
                fill = xl.PatternFill(start_color='00FF00', end_color='00FF00', fill_type='solid')
                ligne = colonne_heure_arrivée.index(heure) + 1 + 5
                for j in range(1, feuille.max_column+1):
                    cell = feuille.cell(row=ligne, column=j)
                    cell.fill = fill

        wb.save('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols.xlsx')



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
          
          #on recupere la partie du mail qui nous interesse
          corps=corps.split("(")
          #separation du mail ligne par ligne
          corps=corps[1].split('\n')
          #la premiere ligne nous permet de detecter le type de message
          ligne=corps[0].split('-')
          type_message=ligne[0].strip(' ')
          id_aeronef=ligne[1]
          decoupage = self.__decoupage
          #on envoie vers une fonction specifique selon le type de mail :
          if type_message=='FPL':
              self.plan_de_vol(corps,id_aeronef)
              self.ecriture_excel(corps,id_aeronef)
              self.tri_geographique(corps,id_aeronef,decoupage)
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
          elif type_message=='SPL':
              self.plan_de_vol_complementaire(corps,id_aeronef)
    
    def message_arrive(self,corps,id_aeronef):              # Fonction terminee fonctionnelle
        
        # Identification de l'aeronef
        ligne=corps[0].split('-')
        b = ligne[1].split(' ')
        id = ' '+b[0][0:2]+b[0][len(b[0])-2:len(b[0])]+b[1]+' '
        idbdd = b[0][0:2]+b[0][len(b[0])-2:len(b[0])]+b[1]
        

        # Supression BDD

        conn = sqlite3.connect('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols_pai_3.db')
        cur = conn.cursor()

        cur.execute('''DELETE FROM "Plans de vols" WHERE Aeronef = ? ''', (idbdd,))

        conn.commit()
        conn.close()

        # Suppression ligne Excel

        wb = xl.load_workbook('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols.xlsx')
        feuille = wb['Vols en cours']

        for row in feuille.iter_rows():
             for cell in row :
                 if str(cell.value) == str(id) : 
                    ligne = cell.row
                    
        for j in range(4,11):
            feuille.cell(ligne,j).value = None
            feuille.cell(ligne,j).fill = xl.styles.PatternFill(fill_type=None)


        wb.save('/Users/thibautdejean/Downloads/PAI-git/PAI-3/vols.xlsx')
        
    def tri_geographique(self,corps,id_aeronef,decoupage) : 

            res = True

            # Connexion a  la maessagerie

            ORG_EMAIL = "@outlook.fr" 
            usernm = "test.pai3" + ORG_EMAIL 
            passwd = "Tomblanchard3."
            conn = imaplib.IMAP4_SSL('outlook.office365.com')
            conn.login(usernm,passwd)
            conn.select('Inbox')

            # Recuperation arrivee, depart et noms de ville

            ligne=corps[4].split('-')
            depart=[ligne[1][1:5]]
            
            
            ligne2=corps[8].split('-')
            arrivee=[ligne2[1][1:5]]
            

            ligne3 = corps[6].split(' ')
            chemin = ligne3[2:len(ligne3)-1]
            

            liste_geo = depart + arrivee 
            
            # Est ce que les villes sont dans la zone de surveillance ? 

            base = sqlite3.connect('/Users/thibautdejean/Downloads/PAI-git/PAI-3/Aerodromes.sqlite')
            cur = base.cursor()
            
            for lieu in liste_geo : 
                cur.execute(f'''SELECT {decoupage} FROM "Liste_des_Aerodromes_en_France"  WHERE "CodeOACI" = ? ''', (lieu,))
                a = cur.fetchall()[0][0]
                print(a)
                if a != '1' :
                    res = False
                else :
                    res = True

            print(res)
            
            base.close()
            #Recherche de l'identifiant du mail
            
            if res == False : 

                status, messages = conn.search(None, 'ALL')

                # Recuperer l'identifiant du dernier message
                latest_message_id = messages[0].split()[-1]

                # Recuperer l'en-tete du dernier message
                status, msg_headers = conn.fetch(latest_message_id, '(BODY.PEEK[HEADER])')

                # Analyser l'en-tete pour savoir si le message est lu ou non
                msg = email.message_from_bytes(msg_headers[0][1])
                
                # Recuperer le contenu du dernier message
                status, msg_content = conn.fetch(latest_message_id, '(BODY[TEXT])')
                content = msg_content[0][1].decode()

                print(latest_message_id)

                conn.copy(latest_message_id, 'Hors_zone')
                conn.store(latest_message_id, '+FLAGS', '\\Deleted')


            conn.expunge()
            conn.close()
            conn.logout()
            return(res)


    ## interface graphique pour le traitement des mails re
    def quitter(self): 
        self.__fen_decoup.destroy()
        self.__fen_vols.destroy()

    
    ##fonction pour choisir les differents decoupages 
    def decoup1(self):
        self.__valid1.config(state=tk.NORMAL)
        self.__img = ImageTk.PhotoImage(Image.open('norm.png')) 
        self.__Canva.create_image(150, 145, image=self.__img)
        self.__decoupage = "NORM"
    def decoup2(self): 
        self.__valid1.config(state=tk.NORMAL)
        self.__img = ImageTk.PhotoImage(Image.open('LY00.png')) 
        self.__Canva.create_image(150, 145, image=self.__img)
        self.__decoupage = "LY00"
    def decoup3(self): 
        self.__valid1.config(state=tk.NORMAL)
        self.__img = ImageTk.PhotoImage(Image.open('LY1T.png')) 
        self.__Canva.create_image(150, 145, image=self.__img)
        self.__decoupage = "LY1T"
    def decoup4(self): 
        self.__valid1.config(state=tk.NORMAL)
        self.__img = ImageTk.PhotoImage(Image.open('LY10.png')) 
        self.__Canva.create_image(150, 145, image=self.__img)
        self.__decoupage = "LY10"
    def decoup5(self): 
        self.__valid1.config(state=tk.NORMAL)
        self.__img = ImageTk.PhotoImage(Image.open('LY11.png')) 
        self.__Canva.create_image(150, 145, image=self.__img)
        self.__decoupage = "LY11"
    def decoup6(self):
        self.__valid1.config(state=tk.NORMAL)
        self.__img = ImageTk.PhotoImage(Image.open('MM1L.png')) 
        self.__Canva.create_image(150, 145, image=self.__img)
        self.__decoupage = "MM1L"
    def decoup7(self): 
        self.__valid1.config(state=tk.NORMAL)
        self.__img = ImageTk.PhotoImage(Image.open('TR00.png')) 
        self.__Canva.create_image(150, 145, image=self.__img)
        self.__decoupage = "TR00"
    def decoup8(self): 
        self.__valid1.config(state=tk.NORMAL)
        self.__img = ImageTk.PhotoImage(Image.open('TR10.png')) 
        self.__Canva.create_image(150, 145, image=self.__img)
        self.__decoupage = "TR10"
    def decoup9(self): 
        self.__valid1.config(state=tk.NORMAL)
        self.__img = ImageTk.PhotoImage(Image.open('TR11.png')) 
        self.__Canva.create_image(150, 145, image=self.__img)
        self.__decoupage = "TR11"
    
    
        
    def create(self):
        # premiere fenetre :
          self.__fen_decoup = Toplevel(self, padx=2, pady=2)
          self.__fen_decoup.title("Plan de Vol")
           # La barre d'outils compose de 2 boutons :
          self.__BO1 = tk.Frame(self.__fen_decoup)
          self.__BO1.pack(side=tk.BOTTOM,padx=5, pady=5)
          self.__valid1=tk.Button(self.__BO1,text='Valider')
          self.__valid1.pack(side=tk.LEFT, padx=5, pady=5)
          self.__valid1.config(state=tk.DISABLED)
          self.__valid1.config(command=self.nouvelle_fen)
          self.__BO2=tk.Frame(self.__fen_decoup,borderwidth=2,bg='white')
          self.__BO2.pack(side=tk.TOP,padx=5,pady=2)
         # Configuration du Label de l'en-tete qui sert a  donner des indications
          self.__label_enTete1=tk.Label(self.__BO2,text="Definissez le decoupage du territoire :", bg='white')
          self.__label_enTete1.config(font=("Arial", 20, "underline"))
          self.__label_enTete1.pack(side=tk.LEFT, padx=20,pady=8) 
         # Configuration du choix du decoupage du territoire
          self.__menu_zone = tk.Menubutton ( self.__BO2 , text = "Choix du decoupage")
          self.__menu_zone.pack(side=tk.LEFT, padx=5, pady=5)
          self.__option = tk.Menu ( self.__menu_zone )
          self.__option.add_command ( label = "Plan NORM" , command = self.decoup1)
          self.__option.add_command ( label = "Plan LY00" , command = self.decoup2)
          self.__option.add_command ( label = "Plan LY1T" , command = self.decoup3)
          self.__option.add_command ( label = "Plan LY10" , command = self.decoup4)
          self.__option.add_command ( label = "Plan LY11" , command = self.decoup5)
          self.__option.add_command ( label = "Plan MM1L" , command = self.decoup6)
          self.__option.add_command ( label = "Plan TR00" , command = self.decoup7)
          self.__option.add_command ( label = "Plan TR10" , command = self.decoup8)
          self.__option.add_command ( label = "Plan TR11" , command = self.decoup9)
          self.__menu_zone [ "menu" ] = self.__option
          # Le canvas pour afficher le plan du decoupage
          self.__Canva =tk.Canvas(self.__fen_decoup, width = 300,height = 290,bg='white')  
          self.__Canva.pack()
          
         # deuxieme fenetre :
          self.__fen_vols=tk.Toplevel(self)
          self.__fen_vols.title("Vol en Cours")
          self.__fen_vols.geometry("1355x700")
          self.__fen_vols.geometry("+0+0")
          self.__BO3 = tk.Frame(self.__fen_vols)
          self.__BO3.pack(side=tk.BOTTOM, padx=5, pady=5)
          self.__Quit1 = tk.Button(self.__BO3, text ='Quitter',command= self.quitter,activeforeground = "blue",activebackground = "yellow", width=13)
          self.__Quit1.pack(side=tk.RIGHT, padx=5, pady=5)
          # Configuration du label de l'en-tete qui sert a  donner des indications
          self.__BO4=tk.Frame(self.__fen_vols,borderwidth=2,bg='white')
          self.__BO4.pack(side=tk.TOP,padx=5,pady=2)
          self.__label_enTete2=tk.Label(self.__BO4,text="Trafic aerien actuel : ", bg='white',fg="black",font=("Arial",15))
          self.__label_enTete2.pack(side=tk.LEFT, padx=20,pady=8) 



    ## Fenetre de creation d'un nouvel identifiant 
    
    
    def est_adresse_email(self,email):
         # Expression reguliere pour verifier si l'adresse e-mail est valide
         regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
         
         # Verifier si l'adresse e-mail correspond a  l'expression reguliere
         if re.match(regex, email):
             return True
         else:
             return False  
    def new_id(self):
        current_time = str(datetime.datetime.now())
        prenom = self.__prenom_entry.get()
        nom = self.__nom_entry.get()
        id_bisg = self.__id_bis_entry.get()
        mail = self.__mail_entry.get()
        password = self.__passwordnew_entry.get()
        passwordnew_confirmation = self.__passwordnew_confirmation_entry.get()
        prenom=str(prenom)
        nom=str(nom)
        id_ =str(id_bisg)
        mail=str(mail)
        mdp = str(password)
        mdp_c= str(passwordnew_confirmation)
        self.__conn = sqlite3.connect('id_pai3.db')
        curseur = self.__conn.cursor()
        curseur.execute("SELECT id FROM mdp WHERE id = '{}'".format(id_bisg.strip()))
        liste = curseur.fetchall()
        self.__conn.close()
        if len(liste)!=0: 
            self.__textAffiche.set("Vous avez deja  un identifiant:veuillez demander a  verifier dans la base de donnee ou creez un nouvel identifiant ")
            return None
        if prenom==None or nom==None or id_bisg==None or mail==None or password==None :
            return None
            self.__textAffiche.set("Vous avez oubliez de remplir une case")
            return None      
        if len(prenom)==0 or  len(nom)==0 or len(id_bisg)==0 or len(mail)==0 or len(password)==0 :
            self.__textAffiche.set("Vous avez oublie de remplir une case")
            return None
        if mdp_c != mdp:
            self.__textAffiche.set("Erreur mot de passe et confirmation mot de passe differents")
            return None
        try: 
            if self.est_adresse_email(mail)==False:
                raise TypeError
                return(None) 
        except TypeError:
            self.__textAffiche.set("Erreur dans la saisie de l'adresse mail")
            return None
        try: 
            if nom.isdigit() or prenom.isdigit():
                raise TypeError
                return(None) 
        except TypeError:
            self.__textAffiche.set("Il ne faut pas de chiffre dans le nom ou le prenom")
            return None
    
        else : 
            self.__conn = sqlite3.connect('id_pai3.db')
            curseur = self.__conn.cursor()
            curseur.execute("INSERT INTO creation_id(prenom, nom, mail,id,mot_de_passe,date_creation) VALUES ('{}','{}','{}','{}','{}','{}')".format(prenom.strip(), nom.strip(), mail.strip(), id_.strip(), mdp.strip(),current_time.strip()))
            curseur.execute("INSERT INTO mdp(id, mot_de_passe) VALUES ('{}', '{}')".format(id_.strip(), mdp.strip()))
            self.__conn.commit()
            self.__textAffiche.set("c'est bon vous etes enregistre")
            self.__conn.close()
            self.__boutonValider2.config(state=tk.DISABLED)
            self.__Quit2.config(state=tk.NORMAL)
            

        
            

    def quitter_bis(self):
         self.__fen_new_id.destroy()     
   
    def create_bis(self) :
        self.__fen_new_id = tk.Toplevel(self,padx=130,pady=100)
        self.__fen_new_id.title("Nouvel Identifiant")
        self.__info = tk.Frame(self.__fen_new_id)
        
        self.__prenom_label = tk.Label(self.__info, text="Prenom_militaire")
        self.__prenom_label.pack()
        self.__prenom_entry = tk.Entry(self.__info)
        self.__prenom_entry.pack()
       
        self.__nom_label = tk.Label(self.__info, text="Nom_militaire")
        self.__nom_label.pack()
        self.__nom_entry = tk.Entry(self.__info)
        self.__nom_entry.pack()
        
        self.__mail_label = tk.Label(self.__info, text="Mail_militaire")
        self.__mail_label.pack()
        self.__mail_entry = tk.Entry(self.__info)
        self.__mail_entry.pack()
        
        self.__id_bis_label = tk.Label(self.__info, text="id_militaire")
        self.__id_bis_label.pack()
        self.__id_bis_entry = tk.Entry(self.__info)
        self.__id_bis_entry.pack()
        
        self.__passwordnew_label = tk.Label(self.__info, text="Mot de passe")
        self.__passwordnew_label.pack()
        self.__passwordnew_entry = tk.Entry(self.__info)
        self.__passwordnew_entry.pack()
        self.__info.pack()
        
        
        self.__passwordnew_confirmation_label = tk.Label(self.__info, text="Confirmation mot de passe")
        self.__passwordnew_confirmation_label.pack()
        self.__passwordnew_confirmation_entry = tk.Entry(self.__info)
        self.__passwordnew_confirmation_entry.pack()
        
        self.__textAffiche = tk.StringVar()
        self.__textAffiche.set("veuillez vous identifier")
        self.__message_erreur= tk.Label(self.__info, textvariable=self.__textAffiche, font=('Times', '16', 'bold'),fg="blue")
        self.__message_erreur.pack()
        
       
        self.__boutonValider2=tk.Button(self.__info,text='Valider',command=self.new_id)
        self.__boutonValider2.pack()
        
        self.__Quit2 = tk.Button(self.__info, text ='Quitter',command=self.quitter_bis,activeforeground = "blue",activebackground = "yellow", width=13)
        self.__Quit2.pack(side=tk.BOTTOM, padx=5, pady=5)
        self.__Quit2.config(state=tk.DISABLED)
        




    ## fenetre d'identification ## 
    def get_id_db(self): 
         self.__conn = sqlite3.connect('id_pai3.db')
         curseur = self.__conn.cursor()
         username = str(self.__username_entry.get())
         password = str(self.__password_entry.get())
         curseur.execute("SELECT id,mot_de_passe From  mdp where id='{}' AND mot_de_passe='{}' ".format(username.strip(), password.strip()))
         liste = curseur.fetchall()
         self.__conn.close()
         if len(liste) != 0 :
             return True
         else: 
             return False
    def login(self):
        current_time = str(datetime.datetime.now())
        username = str(self.__username_entry.get())
        # Verification des informations d'identification ici

        if self.get_id_db():
            self.__message_label.config(text="Connexion reussie !")
            self.__login_button.config(state=tk.DISABLED)
            self.___logout_button.config(state=tk.NORMAL)
            self.create()
        else:
            self.__message_label.config(text="Nom d'utilisateur ou mot de passe incorrect")
        self.__conn = sqlite3.connect('id_pai3.db')
        curseur = self.__conn.cursor()
        curseur.execute("INSERT INTO tab_debut_connexion(id,debut_connexion) VALUES ('{}','{}')".format(username.strip(),current_time.strip()))
        self.__conn.commit()
        self.__conn.close()
        
        
    def logout(self):
        current_time = str(datetime.datetime.now())
        self.__conn = sqlite3.connect('id_pai3.db')
        curseur = self.__conn.cursor()
        username = str(self.__username_entry.get())
        curseur.execute("INSERT INTO tab_fin_connexion(id,fin_connexion) VALUES ('{}','{}')".format(username.strip(),current_time.strip()))
        # se connecter a  la base de donnee

        # executer la requete avec un numero de connexion donne (remplacer 1 par le numero de connexion souhaite)
        curseur.execute("""INSERT INTO Historique_connexion (id, debut_connexion, fin_connexion)
                        SELECT id, debut_connexion, fin_connexion
                        FROM (
                            SELECT id, debut_connexion, NULL AS fin_connexion
                            FROM tab_debut_connexion
                            ORDER BY debut_connexion DESC
                            LIMIT 1
                            ) AS t1
                        UNION ALL
                        SELECT id, NULL AS debut_connexion, fin_connexion
                        FROM (
                            SELECT id, NULL AS debut_connexion, fin_connexion
                            FROM tab_fin_connexion
                            ORDER BY fin_connexion DESC
                            LIMIT 1
                            ) AS t2;
                        """)
        # valider les changements et fermer la connexion
        self.__conn.commit()
        self.__conn.close()
        self.__message_label.config(text="deconnexion reussie !")
        self.__login_button.config(state=tk.NORMAL)
        self.___logout_button.config(state=tk.DISABLED)
        self.quitter()
        
    def __init__(self,base):
         global etat
         etat=True 
         
         # Configuration de la base de donnees
         self.__conn = sqlite3.connect(base)
         # on est connecte a  la base de donnees
         ##Pour executer une requete :
         # curseur.execute("")
         # curseur.fetchall()[0][0]
         
     ## Mise en place de l'interface graphique de la fenetre d'identification  
         Tk.__init__(self)
         self.title("fenetre d'identification")
         self.geometry('400x200')
         
         # Creation des champs de saisie
         self.__username_label = tk.Label(self, text="Nom d'utilisateur")
         self.__username_label.pack()
         self.__username_entry = tk.Entry(self)
         self.__username_entry.pack()
        
         self.__password_label = tk.Label(self, text="Mot de passe")
         self.__password_label.pack()
         self.__password_entry = tk.Entry(self, show="*")
         self.__password_entry.pack()
         
         # Creation du bouton de validation
         self.__login_button = tk.Button(self, text="Se connecter", command=self.login)
         self.__login_button.pack()
         # Creation du bouton de deconnexion 
         self.__logout_button = tk.Button(self, text="Se deconnecter", command=self.logout)
         self.__logout_button.pack()
         self.__logout_button.config(state=tk.DISABLED)
         #bouton en cas d'oubli de mot de passe
         self.__oubli_button = tk.Button(self, text="mot de passe oublie", command=self.create_bis)
         self.__oubli_button.pack()
         # Creation d'une etiquette pour afficher le message de connexion
         self.__message_label = tk.Label(self, text="")
         self.__message_label.pack()

   
        
### Interface Graphique (affichage des vols en cours) ###

    def nouvelle_fen(self):
         global etat
         #Fermeture de la premiere fenetre
         self.withdraw()
         # self._fen.deiconify()
         self.lecture_mail()
         
         
    ### definnir un cycle qui relance la fonction a  un intervalle de temps precis afin de lire les nouveaux mails.
    def lecture_mail(self):
        global etat
        servername='outlook.office365.com'
        self.__fen_vols.deiconify()
        ### Lecture des mails ###
        start_time = time.time()
        interval = 10 #on recupere des nouveaux mails toutes les 10 secondes
        j=0
        while etat==True:
            j+=interval
            time.sleep(start_time + j - time.time())
            (i,data,conn)=connexion(servername)
            self.mail(i,data,conn)
            self.iter_retard_avion()
    
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
                    # on obtient de chaine de caractere qu'il faut maintenan traiter.
                    
                    ###Possibilite de stocker chaque mail dans un fichier txt : 
                    # file_name = "email_" + str(x) + ".txt"
                    # output_file = open(file_name, 'w')
                    # output_file.write("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" %(email_from, email_to,local_message_date, subject, body.decode('utf-8')))
                    # output_file.close()
                    
                else:
                    continue
        print("mails traites, pas de mails non lus")
                
        
 
                
### Programme Principal ###
if __name__ == '__main__':
### Creation de l'interface Graphique ###
    fen = FenPrincipale("nom_base.db")
    fen.mainloop()  