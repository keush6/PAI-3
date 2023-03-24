import sqlite3


def assemblage_villes(chemin):

        conn = sqlite3.connect('/Users/thibautdejean/Downloads/PAI/villes_france.db')
        cur = conn.cursor()

        chemin_fini = []
        assemblage = ''
        # Assemblage des villes pour les chemins
        p = 0
        for ville in chemin : 
            ville = assemblage + ville
            cur.execute("SELECT * FROM cities WHERE field4 LIKE ?", ('%'+ville+'%',))
            if p > 6 :
                chemin_fini.append(ville)
            elif len(cur.fetchall()) > 0 : 
                chemin_fini.append(ville)
                assemblage = ''
                p=0
            else : 
                assemblage = assemblage +' '+ ville 
                p+=1

        return(chemin_fini)




print(assemblage_villes(['UZES', 'SAINT', 'HIPPOLYTTE', 'DU', 'FORT', 'BEDARIEUX']))