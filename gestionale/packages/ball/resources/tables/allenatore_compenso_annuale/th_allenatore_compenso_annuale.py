#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('codice_allenatore')
        r.fieldcell('gennaio',totalize=True)
        r.fieldcell('febbraio',totalize=True)
        r.fieldcell('marzo',totalize=True)
        r.fieldcell('aprile',totalize=True)
        r.fieldcell('maggio',totalize=True)
        r.fieldcell('giugno',totalize=True)
        r.fieldcell('luglio',totalize=True)
        r.fieldcell('agosto',totalize=True)
        r.fieldcell('settembre',totalize=True)
        r.fieldcell('ottobre',totalize=True)
        r.fieldcell('novembre',totalize=True)
        r.fieldcell('dicembre',totalize=True)
        r.fieldcell('totale',totalize=True)
        r.fieldcell('anno')
        
        

    def th_order(self):
        return 'codice_allenatore'

    def th_query(self):
        return dict(column='codice_allenatore', op='contains', val='')


    #metodo apply, cambia dinamicamente il contenuto della riga
    @public_method
    def th_applymethod(self,selection=None):
        
        
        #calcola gli elementi ricorsivamente per riga
        def cb(row):

            mese = ['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre']

            data = self.db.table('ball.allenatore_compenso').query(
                    columns='$data,$entrate_uscite,$importo,$codice_allenatore,$protocollo',
                ).fetchAsDict(key='protocollo')  

            anno_selezionato = self.db.table('ball.allenatore_compenso_annuale').query(columns='$anno,$codice_allenatore').fetchAsDict(key='codice_allenatore')  
            anno_selezionato = int(anno_selezionato[row['codice_allenatore']]['anno'])
            
            old = row

            for i in mese:
                row[i] = 0
            row['totale'] = 0

            chiavi = data.keys()
            
            for i in chiavi:
                if data[i]['codice_allenatore'] == row['codice_allenatore']:
                    dato = data[i]

                    if dato['data'].year == anno_selezionato:
                        month = dato['data'].month
                        p = mese[(month-1)]
                        s_r = dato['importo']
                    
                        if dato['entrate_uscite'].lower() == 'entrate':
                            row[p] -= s_r
                        else:
                            row[p] += s_r

            for i in mese:
                row['totale'] += row[i]

        
            new = dict(codice_allenatore=row['codice_allenatore'],gennaio = row[mese[0]],febbraio=row[mese[1]],marzo=row[mese[2]],
                aprile=row[mese[3]],maggio=row[mese[4]],giugno=row[mese[5]],luglio=row[mese[6]],
                agosto=row[mese[7]],settembre=row[mese[8]],ottobre=row[mese[9]],novembre=row[mese[10]],
                dicembre=row[mese[11]],totale=row['totale'],anno=str(anno_selezionato))

           # self.db.table('ball.allenatore_compenso_annuale').update(new,old,pkey=row['pkey'])
           # self.db.commit()

            return new

        selection.apply(cb)

                   

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('codice_allenatore')
        fb.filteringSelect('^.anno',values='2021:2021,2022:2022')
        

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

    