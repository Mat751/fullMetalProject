from gnr.app.gnrapp import GnrApp
import os 
import psycopg2
from dotenv import load_dotenv
import datetime

load_dotenv()
connection = psycopg2.connect(os.environ.get('DATABASE_URL'))

SELECT_COLUMN_COMUNE="""SELECT id,denominazione FROM glbl.glbl_comune"""

if __name__ == '__main__':
    db = GnrApp('mybasket').db
    

    #store belfiore - comune e provincia
    file = '/home/zattew/sviluppo/genropy_projects/basket/packages/ball/lib/codici_comuni.txt'
    d={}
    with open(file) as f1:
        for line in f1:
            line = line.rstrip('\n')
            info = line.split('\t')
            d[info[5]] = [info[1],info[2]]
    f1.close()

    #store belfiore estero
    file = '/home/zattew/sviluppo/genropy_projects/basket/packages/ball/lib/Stato_Codice_AT.txt'
    d_estero={}
    with open(file) as f1:
        for line in f1:
            line = line.rstrip('\n')
            info = line.split(';')
            if info[1] != 'n.d.':
                d_estero[info[1]]=info[0]
    f1.close()

    #store comune id
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_COLUMN_COMUNE)
            result = cursor.fetchall()
            comuni = {b.upper():a for a,b in result}
    
    #tabella iscritti
    tbliscritto= db.table('ball.iscritto')
    f = tbliscritto.query(columns='$cognome,$codice_fiscale').fetch()
    f = {b:a for a,b,c in f}

    #leggo iscritti
    conta = 1
    file = '/home/zattew/sviluppo/genropy_projects/basket/packages/ball/lib/iscritti_fip.txt'
    with open(file) as f1:
        for line in f1:
            info = line.split()
            print(info)

            #setto variabili
            stato_estero,comune_id,provincia= "","",""

            if len(info)==6:
                cf_splitted = [a for a in info[3]]
                belfiore = ''.join(cf_splitted[11:15])
            
        
            elif len(info)>6:
                info[1] += " "+info[2] 
                cf_splitted = [a for a in info[4]]
                belfiore = ''.join(cf_splitted[11:15])
                del info[2]
         
        
            if belfiore in d.keys():
                comune_nascita = d[belfiore][0]

                if comune_nascita in comuni.keys():
                    comune_id = comune_nascita
                    provincia=d[belfiore][1]
        
            else:
                stato_estero=d_estero[belfiore].upper()

        
            #create data object
            data = info[2].split('/')
            data = datetime.datetime(int(data[2]),int(data[1]),int(data[0]))
            formatted_date = data.strftime('%Y-%m-%d')
        
            #formatta apostrofo
            if "'" in info[0]:
                info[0] = info[0].replace("'","''")
        
            if "'" in info[1]:
                info[1] = info[1].replace("'","''")

            #se il codice fiscale non è già presente nella tabella
            if not info[3] in f.keys():
                nuova_riga=dict(cognome=info[0],nome=info[1],
                            data_nascita=formatted_date,codice_fiscale=info[3],
                            sex=info[4],comune_id=comune_id,provincia=provincia,stato_estero=stato_estero)
        
                tbliscritto.insert(nuova_riga)
            else:
                print(f"""{info[3]} gia' presente in tabella""")
    db.commit()        