#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('nome_allenatore')
        r.fieldcell('data_nascita_allenatore')
        r.fieldcell('comune_nascita_allenatore')
        r.fieldcell('codice_fiscale_allenatore')
        r.fieldcell('allenatore_totale')
        r.fieldcell('anno')

   

    @public_method
    def th_applymethod(self,selection=None):
        def cb(row):
       
            def trovaComune(id=None):
                data = self.db.table('glbl.comune').query(
                    columns='$id,$denominazione',
                ).fetchAsDict(key='id')
                return data[id]['denominazione']

            def calcolaTotale(anno=None):
                data = self.db.table('ball.allenatore_compenso').query(
                    columns='$data,$entrate_uscite,$importo,$codice_allenatore,$protocollo',
                ).fetchAsDict(key='protocollo')
                
                totale = 0
                chiavi = data.keys()
                for i in chiavi:
                    if data[i]['codice_allenatore'] == row['nome_allenatore']:
                        dato = data[i]
                        
                        if dato['data'].year == int(row['anno']):
                            if dato['entrate_uscite'].lower() == 'entrate':
                                totale -= dato['importo']
                            else:
                                totale+=dato['importo']
                return totale
                            

            data = self.db.table('ball.allenatore').query(
                    columns='$pkey,$data_nascita,$comune_id,$codice_fiscale',
                ).fetchAsDict(key='pkey')  

            old = row
            
            dato = data[row['nome_allenatore']]
            row['data_nascita_allenatore'] = dato['data_nascita']
            row['comune_nascita_allenatore'] = trovaComune(dato['comune_id'])
            row['codice_fiscale_allenatore'] = dato['codice_fiscale']
            row['allenatore_totale'] = calcolaTotale(row['anno'])
            
            new = dict(nome_allenatore=row['nome_allenatore'],
                        data_nascita_allenatore=row['data_nascita_allenatore'],
                        comune_nascita_allenatore=row['comune_nascita_allenatore'],
                        codice_fiscale_allenatore=row['codice_fiscale_allenatore'],
                        allenatore_totale=row['allenatore_totale'],
                        anno=row['anno'],
                        pkey=row['pkey'])
            
            self.db.table('ball.allenatore_tabella_fiscale').update(new,old,pkey=row['pkey'])
            self.db.commit()
            return new

        selection.apply(cb)
        
        
    def th_order(self):
        return 'nome_allenatore'

    def th_query(self):
        return dict(column='nome_allenatore', op='contains', val='')




class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('nome_allenatore')
        fb.filteringSelect('^.anno',lbl='Seleziona anno pagamento',
                           tooltip="""FilteringSelect: you can select only an existing value.<br/>
                                  You see the description but in the store we will have the value.""",
                           values='2021:2021,2022:2022',)
        

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px',liveUpdate=True)
