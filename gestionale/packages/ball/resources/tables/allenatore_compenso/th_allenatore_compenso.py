#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('protocollo')
        r.fieldcell('codice_allenatore')
        r.fieldcell('data')
        r.fieldcell('importo')
        r.fieldcell('entrate_uscite')

    def th_order(self):
        return 'codice_allenatore'

    def th_query(self):
        return dict(column='codice_allenatore', op='contains', val='')


class Form(BaseComponent):

    def th_form(self, form):
        entrate='entrate,uscite'

        bc = form.center.borderContainer()
        top = bc.contentPane(region='top',datapath='.record')
        fb = top.formbuilder(cols=2, border_spacing='4px')
        fb.field('protocollo')
        fb.field('codice_allenatore')
        fb.field('data')
        fb.field('importo')
        fb.filteringSelect('^.entrate_uscite',lbl='Entrate o Uscite', 
                       tooltip="""FilteringSelect: you can select only an existing value.<br/>
                                  You see the description but in the store we will have the value.""",
                       values=entrate)



    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
        

class ViewFromAllenatore2021(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('protocollo')
        r.fieldcell('data')
        r.fieldcell('importo',totalize=True)
        #r.fieldcell('entrate_uscite')    

     #metodo apply, cambia dinamicamente il contenuto della riga
    @public_method
    def th_applymethod(self,selection=None):
        
        
        #calcola gli elementi ricorsivamente per riga
        def cb(row):

            data = self.db.table('ball.allenatore_compenso').query(
                    columns='$entrate_uscite,$importo,$protocollo,$data',
                ).fetchAsDict(key='protocollo')  
 
            chiavi = data.keys()
            
            for i in chiavi:
                if data[i]['protocollo'] == row['protocollo'] and data[i]['data'].year == 2021:
                    dato = data[i]
                    
                    if dato['entrate_uscite'].lower() == 'entrate':
                        row['importo'] = row['importo'] * (-1)

            if row['data'].year == 2021:
                return dict(importo=row['importo'])

        selection.apply(cb)
    


class ViewFromAllenatore2022(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('protocollo')
        r.fieldcell('data')
        r.fieldcell('importo',totalize=True)
        #r.fieldcell('entrate_uscite')    

     #metodo apply, cambia dinamicamente il contenuto della riga
    @public_method
    def th_applymethod(self,selection=None):
        
        
        #calcola gli elementi ricorsivamente per riga
        def cb(row):

            data = self.db.table('ball.allenatore_compenso').query(
                    columns='$entrate_uscite,$importo,$protocollo,$data',
                ).fetchAsDict(key='protocollo')  
 
            chiavi = data.keys()
            
            for i in chiavi:
                if data[i]['protocollo'] == row['protocollo'] and data[i]['data'].year == 2022:
                    dato = data[i]
                    
                    if dato['entrate_uscite'].lower() == 'entrate':
                        row['importo'] = row['importo'] * (-1)

            if row['data'].year == 2022:
                return dict(importo=row['importo'])

        selection.apply(cb)