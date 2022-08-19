
import os 
import psycopg2
from dotenv import load_dotenv
import datetime

load_dotenv()

COLUMN_NAME="""SELECT * FROM glbl.glbl_comune"""
SELECT_COLUMN="""SELECT nome,cognome,data_nascita,sex,comune_id,provincia,codice_fiscale,data_iscrizione
                 FROM ball.ball_iscritto"""
SELECT_COLUMN_COMUNE="""SELECT id,denominazione FROM glbl.glbl_comune"""

connection = psycopg2.connect(os.environ.get('DATABASE_URL'))

def get_column_name():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(COLUMN_NAME.replace(";","")+" LIMIT 0;")
            colnames = [desc[0] for desc in cursor.description]
            return colnames
        
def get_table():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_COLUMN)
            result = cursor.fetchall()
            return result

#store comune id
with connection:
    with connection.cursor() as cursor:
        cursor.execute(SELECT_COLUMN_COMUNE)
        result = cursor.fetchall()
        comuni = {b.upper():a for a,b in result}

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

#single insert
def single_insert(insert_req):
    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(insert_req)
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s" % error)
                connection.rollback()
                cursor.close()
                return 1
    cursor.close()


#leggo iscritti
conta = 1
file = 'iscritti_fip.txt'
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
        
        #query
        query="""
        INSERT INTO ball.ball_iscritto(id,cognome,nome,data_nascita,codice_fiscale,sex,comune_id,provincia,stato_estero) values(%s,'%s','%s','%s','%s','%s','%s','%s','%s');
        """ % (conta,info[0],info[1],formatted_date,info[3],info[4],comune_id,provincia,stato_estero)

        single_insert(query)
        conta +=1
        
connection.close()