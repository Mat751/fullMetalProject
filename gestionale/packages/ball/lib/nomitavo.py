
from datetime import datetime as dt
from operator import itemgetter
from gnr.core.gnrdecorator import public_method



class Nominativo(object):
    
    def codici_comuni(self,comune,provincia,path):
        d = {}
        
        with open('/home/zattew/sviluppo/genropy_projects/basket/packages/ball/lib/codici_comuni.txt') as f:
            for line in f:
                line = line.strip('\n')
                id,com,n1,n2,n3,bell=line.split("\t")
                if com == comune.upper() and n1 == provincia.upper():
                    f.close()
                    return bell
    

    def calcolo_consonanti(self,nome,controllo=None):

        vocali = ['a','e','i','o','u']
        c1 = [char for char in nome if char not in vocali and char != " "]
        tot = [char for char in nome if char != " "]

        if len(tot) < 3:
            tot.append('x')
            return ''.join(tot)

    
        elif len(c1) < 3:
            for char in nome:
                if char in vocali and len(c1) < 3:
                    c1.append(char)
    
        elif len(c1) > 3 and controllo:
            g = [0,2,3]
            c1 = itemgetter(*g)(c1)
        
        return ''.join(c1[:3])


    def calcola_mese(self,mese):
        converti = {1:'A',2:'B',3:'C',4:'D',5:'E',6:'H',7:'L',
                    8:'M',9:'P',10:'R',11:'S',12:'T'}
        return converti[mese]

    @public_method
    def calcola_codice_fiscale(self,selection=None):

        def cb(row):
            
            data = self.db.table('ball.iscritto').query(
                    columns='$id,$nome,$cognome,$data_nascita,$sex,$comune_id,$provincia'
                ).fetchAsDict(key='id')  
        
            stringa = ""

            chiavi = data.keys()
            
            for i in chiavi:
                if data[i]['id'] == row['id']:
                    dato = data[i]

            #cognome 
            c1 = self.calcolo_consonanti(dato['cognome'])
            stringa += c1.upper()

            #nome
            c1 = self.calcolo_consonanti(dato['nome'],controllo=True)
            stringa += c1.upper()

            anno = str(dato['data_nascita'].year)
            anno = anno[2:]
            stringa += str(anno)

            #mese
            stringa += self.calcola_mese(dato['data_nascita'].month)

            #sesso e giorno
            if dato['sex'] == 'M':
                d1 = dato['data_nascita'].day
                if d1 < 10:
                    dat1 = "0"+str(d1)
                    stringa += dat1
                else:
                    stringa += str(d1)
            else:
                stringa += str(dato['data_nascita'].day+40)

            #codice comune
            stringa += self.codici_comuni(comune=dato['comune_id'],
                                          provincia=dato['provincia'])
            stringa += self.carattere_di_controllo(stringa)
            row['codice_fiscale'] = stringa
            return dict(codice_fiscale=row['codice_fiscale'])

        selection.apply(cb)

    def carattere_di_controllo(self,stringa):
        stringa = [char for char in stringa]
    
        #inverto perchè calcola la posizione a partire da 1
        dispari = [stringa[i] for i in range(len(stringa)) if i % 2 == 0 ]
        pari = [stringa[i] for i in range(len(stringa)) if i % 2 != 0 ]
    
        disp = {}
        with open("/home/zattew/sviluppo/genropy_projects/basket/packages/ball/lib/tabella_dispari.txt") as f:
            for line in f:
                line = line.strip('\n')
                n1,n2,n3,n4,n5,n6,n7,n8=line.split("\t")
                disp[n1]=n2
                disp[n3]=n4
                disp[n5]=n6
                disp[n7]=n8
        f.close()
    
        par = {}
        with open("/home/zattew/sviluppo/genropy_projects/basket/packages/ball/lib/tabella_pari.txt") as f:
            for line in f:
                line = line.strip('\n')
                n1,n2,n3,n4,n5,n6,n7,n8=line.split("\t")
                par[n1]=n2
                par[n3]=n4
                par[n5]=n6
                par[n7]=n8
        f.close()
    
        somma = 0
        for i in pari:
            somma += int(par[i])
        for i in dispari:
            somma += int(disp[i])
        resto = somma % 26
    
        ris = {}
        conta = 1
        with open("/home/zattew/sviluppo/genropy_projects/basket/packages/ball/lib/resto.txt") as f:
            for line in f:
                line = line.strip('\n')
                if conta < 6:
                    n1,n2,n3,n4,n5,n6,n7,n8=line.split("\t")
                    ris[n1]=n2
                    ris[n3]=n4
                    ris[n5]=n6
                    ris[n7]=n8
                else:
                    n1,n2,n3,n4,n5,n6=line.split("\t")
                    ris[n1]=n2
                    ris[n3]=n4
                    ris[n5]=n6
                conta += 1
        f.close()

        return ris[str(resto)]