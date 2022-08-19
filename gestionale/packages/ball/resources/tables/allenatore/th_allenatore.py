#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method,customizable

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        anag = r.columnset('anag', name='ANAGRAFICA', color='white', font_weight='bold', background='darkblue')
        anag.fieldcell('nome')
        anag.fieldcell('cognome')
        anag.fieldcell('data_nascita')
        anag.fieldcell('sesso')
        anag.fieldcell('provincia')
        anag.fieldcell('comune_id')
        anag.fieldcell('codice_fiscale')
        
        info = r.columnset('info', name='INFORMAZIONI', color='white', font_weight='bold', background='darkgrey')
        info.fieldcell('ruolo')
        info.fieldcell('email')
        info.fieldcell('voto')
        

    def th_order(self):
        return 'nome'

    def th_query(self):
        return dict(column='nome', op='contains', val='')



class Form(BaseComponent):
    py_requires = "gnrcomponents/attachmanager/attachmanager:AttachManager"

    def th_form(self, form):
        tc = form.center.tabContainer(margin='2px')
        self.dati_allenatore(tc.borderContainer(title='Dati allenatore'))
        self.allegati_allenatore(tc.contentPane(title='Allegati'))
        self.fatture2021(tc.contentPane(title='Stipendio 2021'))
        self.fatture2022(tc.contentPane(title='Stipendio 2022'))

    @customizable    
    def dati_allenatore(self,bc):
        
        top = bc.contentPane(region='top',datapath='.record')
        fb = top.formbuilder(cols=2, border_spacing='4px')
        fb.field('nome')
        fb.field('cognome')
        fb.field('data_nascita')
        
        #definisco filtro con scelta
        sesso = 'F:Femmina,M:Maschio'
        fb.filteringSelect('^.sesso',lbl='Sesso', 
                       tooltip="""FilteringSelect: you can select only an existing value.<br/>
                                  You see the description but in the store we will have the value.""",
                       values=sesso)
        fb.field('provincia')
        fb.field('comune_id',condition='$sigla_provincia=:provincia',
                 condition_provincia='^.provincia')
        fb.field('codice_fiscale')
        fb.field('email')
        
        center = bc.tabContainer(region='left', title='Valutazioni',width='50%',margin='4px',datapath=".record")
        #center = bc.contentPane(region='center',)
        center = center.tabContainer(title='Valutazioni',region='center')
        fb = center.formbuilder(cols=2, border_spacing='4px')
        fb.filteringSelect('^.ruolo',lbl='Ruolo',colspan=2,
                       tooltip="""FilteringSelect: you can select only an existing value.<br/>
                                  You see the description but in the store we will have the value.""",
                       values='Responsabile tecnico:Responsabile tecnico,Allenatore promozione:Allenatore promozione,Allenatore U19:Allenatore U19,Allenatore U18:Allenatore U18,Allenatore U17:Allenatore U17,Allenatore U16:Allenatore U16,Allenatore U15:Allenatore U15,Allenatore U14:Allenatore U14,Allenatore U13:Allenatore U13,Responsabile Minibasket:Responsabile Minibasket,Minibasket Eso:Minibasket Eso,Minibasket Sco:Minibasket Sco,Minibasket:Minibasket,Microbasket:Microbasket')
        
        valori = 'Scarso:1,Sufficiente:2,Buono:3,Discreto:4,Ottimo:5'
        fb.radioButtonText(value='^.voto', values=valori, 
                           lbl='Voto complessivo: ',
                           tooltip="""Seleziona voto ma sii magnanimo<br>
                           non si sa mai chi potresti trovarti davanti!""")

        center.simpleTextArea(value='^.note',region='bottom',
        lbl='Commenti',width='500px',height='300px')


    def allegati_allenatore(self,pane):
        pane.attachmentGrid()

        #il tab container per le note pesca da record e va bene
        #tc = bc.tabContainer(region='center',margin='2px')   
        #creo campo stipendio, devo togliere il path perchè non è più questo
        

    #per lo stipendio dell'allenatore uso un plainTable handler che
    #fa visualizzare i record della fattura degli stipendi in relazione
    #al cliente che abbiamo visualizzato

    def fatture2021(self,pane):
        pane.plainTableHandler(relation='@compensi',viewResource='ViewFromAllenatore2021')
    
    def fatture2022(self,pane):
        pane.plainTableHandler(relation='@compensi',viewResource='ViewFromAllenatore2022')
    


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

   