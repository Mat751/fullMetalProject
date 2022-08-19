#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method,customizable

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        anag = r.columnset('anag', name='ANAGRAFICA GENITORI', color='white', font_weight='bold', background='darkblue')
        anag.fieldcell('nome')
        anag.fieldcell('cognome')
        anag.fieldcell('data_nascita')
        anag.fieldcell('sesso')
        anag.fieldcell('stato_estero')
        anag.fieldcell('comune_id')
        anag.fieldcell('provincia')
        anag.fieldcell('codice_fiscale')
        
        dett = r.columnset('dett', name='DETTAGLI GENITORI', color='white', font_weight='bold', background='orange')
        dett.fieldcell('email')
        dett.fieldcell('figli')

    def th_order(self):
        return 'nome'

    def th_query(self):
        return dict(column='nome', op='contains', val='')



class Form(BaseComponent):
    py_requires = "gnrcomponents/attachmanager/attachmanager:AttachManager"

    def th_form(self, form):
        tc = form.center.tabContainer(margin='2px')
        self.dati_iscritto(tc.borderContainer(title='Dati iscritto'))
        self.allegati(tc.contentPane(title='Allegati genitore'))
        self.fatture2021(tc.contentPane(title='Pagamenti 2021'))
        self.fatture2022(tc.contentPane(title='Pagamenti 2022'))

    @customizable    
    def dati_iscritto(self,bc):
        top = bc.contentPane(region='top',datapath='.record')
        fb = top.formbuilder(cols=3, border_spacing='4px')
        fb.field('nome')
        fb.field('cognome')
        fb.field('data_nascita')
        fb.filteringSelect('^.sesso',values='F:Femmina,M:Maschio',lbl='Sesso')
        fb.field('stato_estero')
        fb.field('comune_id')
        fb.field('provincia')
        fb.field('email')
        fb.field('codice_fiscale')
        
        center = bc.tabContainer(region='left', title='Valutazioni',width='70%',margin='4px',datapath=".record")
        #center = bc.contentPane(region='center',)
        center = center.tabContainer(title='Figli a carico',region='center')
        fb = center.formbuilder(cols=2, border_spacing='4px',width='auto')
        numero = '1:1,2:2,3:3,4:4,5:5'
        fb.filteringSelect('^.figli',values=numero,
        lbl='Numero figli iscritti',colspan=2)
        fb.simpleTextArea(value='^.note',
        lbl='Nome figli: ',width='250px',height='150px',colspan=2)

    def allegati(self,pane):
        pane.attachmentGrid()

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
    
    def fatture2021(self,pane):
        pane.plainTableHandler(relation='@pagamenti_genitori',viewResource='ViewFromGenitore2021')
    
    def fatture2022(self,pane):
        pane.plainTableHandler(relation='@pagamenti_genitori',viewResource='ViewFromGenitore2022')
    

