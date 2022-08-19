#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.app.gnrapp import GnrApp
from gnr.core.gnrdecorator import public_method,customizable
from datetime import date as dat
import ftplib


class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        
        anag = r.columnset('anag', name='ANAGRAFICA', color='white', font_weight='bold', background='darkblue')
        anag.fieldcell('nome_completo')
        anag.fieldcell('data_nascita')
        anag.fieldcell('anni')
        anag.fieldcell('sex')
        anag.fieldcell('stato_estero')
        anag.fieldcell('provincia')
        anag.fieldcell('comune_id')
        anag.fieldcell('codice_fiscale')
        paf = r.columnset('pag', name='PAGAMENTI', color='white', font_weight='bold', background='darkred')
        paf.fieldcell('pag_completo',semaphore=True)

        isc= r.columnset('isc', name='ISCRIZIONE', color='white', font_weight='bold', background='orange')

        isc.fieldcell('data_iscrizione')
        isc.fieldcell('categoria')
        isc.fieldcell('email')

        carac= r.columnset('carac', name='CARATTERISTICHE', color='white', font_weight='bold', background='darkgreen')

        carac.fieldcell('peso')
        carac.fieldcell('altezza')
        carac.fieldcell('ruolo')
        carac.fieldcell('voto')
        #r.fieldcell('terra')

        #r.fieldcell('modulo_iscrizione', format_trueclass='greenLight', format_nullclass='yellowLight', format_falseclass='redLight')

        
        
    def th_order(self):
        return 'nome'

    def th_query(self):
        return dict(column='nome', op='contains', val='')

    
   
    #metodo apply, cambia dinamicamente il contenuto della riga
    @public_method
    def th_applymethod(self,selection=None):

            
        def calculate_age(born):
            today = dat.today()
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


        #calcola gli elementi ricorsivamente per riga
        def cb(row):
            
            data = self.db.table('ball.iscritto').query(
                    columns='$voto,$codice_fiscale,$provincia,$data_nascita,$nome_completo,$categoria,$nome,$cognome,$comune_id,$sex'
                ).fetchAsDict(key='nome_completo')  
 
            dato = data[row['nome_completo']]
            row['anni'] = calculate_age(dato['data_nascita'])
            return dict(anni=row['anni'])
            
        selection.apply(cb)    


    

class Form(BaseComponent):
    py_requires = "gnrcomponents/attachmanager/attachmanager:AttachManager"

    def th_form(self, form):
        tc = form.center.tabContainer(margin='2px')
        self.dati_iscritto(tc.borderContainer(title='Dati iscritto'))
        self.allegati(tc.contentPane(title='Allegati iscritto'))


    @customizable    
    def dati_iscritto(self,bc):
        top = bc.contentPane(region='top',datapath='.record')
        fb = top.formbuilder(cols=3, border_spacing='4px')

        sesso = 'F:Femmina,M:Maschio'
        fb.field('nome')
        fb.field('cognome')
        fb.field('data_nascita')
        fb.filteringSelect('^.sex',lbl='Sesso', 
                       tooltip="""FilteringSelect: you can select only an existing value.<br/>
                                  You see the description but in the store we will have the value.""",
                       values=sesso)
        fb.field('stato_estero')
        fb.field('provincia')
        fb.field('comune_id')
        fb.field('codice_fiscale')
        
        # condition='$sigla_provincia=:provincia',
        #        condition_provincia='^.provincia')
        #fb.field('codice_fiscale')
        #fb.field('anni',edit=False)
        
        fb.field('peso',lbl='peso (kg)')
        fb.field('altezza',lbl='Altezza (cm)')
        
        ruolo = 'Playmaker:Playmaker,Ala:Ala,Guardia:Guardia,Pivot:Pivot'

        #fb.field('categoria',edit=True,colspan=2)
        
        
        fb.field('data_iscrizione')
        fb.field('email')

        valori = 'Scarso:1,Sufficiente:2,Buono:3,Discreto:4,Ottimo:5'
        center = bc.tabContainer(region='left', title='Valutazioni',width='60%',margin='4px',datapath=".record")
        #center = bc.contentPane(region='center',)
        center = center.tabContainer(title='Valutazioni',region='center')
        fb = center.formbuilder(cols=2, border_spacing='4px',width='auto')

        #categorie='MCB:Micro Basket,MBA:Mini Basket A,MBB:Mini Basket B,U13:Under 13,U14:Under 14,U15:Under 15,U16:Under 16,U17:Under 17,U19:Under 19'
        categorie='MCB:Micro Basket,MBA:Mini Basket A,MBB:Mini Basket B,U13:Under 13,U14:Under 14,U15:Under 15,U16:Under 16,U17:Under 17,U19:Under 19'
        fb.filteringSelect('^.ruolo',lbl='Ruolo: ', 
                       tooltip="""Seleziona ruolo""",
                       values=ruolo)

        fb.filteringSelect('^.categoria',values=categorie,
                            lbl='Categoria: ',
                            tooltip="""Seleziona categorie""")
        
        fb.radioButtonText(value='^.voto', values=valori,colspan=2,
                           lbl='Voto: ',
                           tooltip="""Seleziona voto ma sii magnanimo<br>
                           non si sa mai chi potresti trovarti davanti!""")
        fb.simpleTextArea(value='^.note',
        lbl='Commenti: ',width='400px',height='200px',colspan=2)

        #fb = top.borderContainer(cols=3, border_spacing='4px',title='Genitore')
        
        center = bc.tabContainer(region='right', title='Valutazioni',width='35%',
                                 height='50%',margin='4px',datapath=".record")
        
        self.anagrafica(center)    
        self.pagamenti(center,anno="22/23")
        #self.pagamenti(center,anno="22/23")

    
        #modulo iscrizione a destra
        #right = bc.tabContainer(region='right', title='Valutazioni',width='20%',margin='4px',datapath=".record")
        #right = right.tabContainer(title='Modulo iscrizione',region='center',heigh='80px')

        #right.div('^#FORM.warning.modulo_iscrizione', _class='^#FORM.warning.css_class', colspan=2)
        #right.dataController( """var warning,cls;
         #                   if(modulo_iscrizione){warning='Modulo privacy già allegato';
         #                      cls='verde';}
         #                   else{
         #                   warning='Manca il modulo privacy del paziente!';
         #                   cls='rosso';
         #                  }
         #                  SET #FORM.warning.modulo_iscrizione= warning;
         #                  SET #FORM.warning.css_class= cls;""",
         #                  modulo_iscrizione='^.modulo_iscrizione',
         #                 _virtual_column='modulo_iscrizione_presente',
         #                  saved='^#FORM.controller.saved')

        bottom = bc.contentPane(region='bottom',datapath='.record')
        fb = bottom.formbuilder(cols=3,border_spacing='10px')
        btn = fb.button('AGGIORNA TUTTI GLI ISCRITTI',color='red')
        btn.dataRpc('.risposta',self.getTime)
        fb.div('^.risposta')

    def anagrafica(self,center):
        center = center.tabContainer(title=f'Angrafica genitori',region='center')
        fb = center.formbuilder(cols=1, border_spacing='4px',width='auto')
        fb.radiobuttontext('^.pagamento_iscritto',lbl='Pagamento: ',
                        values='Ragazzo:Ragazzo,Genitore:Genitore')   
        fb.field('nome_genitore')
        fb.field('cognome_genitore')
        fb.field('codice_fiscale_genitore')
        fb.div('^.pag_completo',lbl='Stato pagamenti: ',
                _virtual_column='$pag_completo',format='semaphore',dtype='B')
        fb.div('^.num_figli',lbl='Figli a carico del genitore: ',_virtual_column='$num_figli',
                 dtype='L')

    def pagamenti(self,center,anno=None):
        center = center.tabContainer(title=f'Pagamenti {anno}',region='center')
        fb = center.formbuilder(cols=1, border_spacing='4px',width='auto')

        mod = 'Paypal:Paypal,Bonifico:Bonifico,Assegno:Assegno'
        fb.filteringSelect('^.pagamento',lbl='Tipo pagamento 1: ', 
                       tooltip="""Seleziona ruolo""",
                       values=mod)
        
        fb.field('importo1')
        fb.field('data1')

        fb.filteringSelect('^.pagamento2',lbl='Tipo pagamento 2: ', 
                       tooltip="""Seleziona ruolo""",
                       values=mod)
        fb.field('importo2')
        fb.field('data2')

    def allegati(self,pane):
        pane.attachmentGrid()
        
        #tc1 = bc.tabContainer(region = 'center',margin='2px',datapath=".record")
        

        #tab1 = tc1.contentPane(title='Note')
        #tab1.simpleTextArea(value='^.note_iscritto',editor=True)

        #tc1.contentPane(title='Foto').img(src="^.photo_url",
        #       crop_height='200px',
        #       crop_width='200px',
        #       margin='5px',
        #       crop_border='2px dotted silver',
        #       crop_rounded=6,
        #       edit=True,
        #       placeholder=True,
               #upload_folder='*', #con asterisco salvo in database
               # ma perdo possibilità di ridurre immagine
        #       upload_folder='site:/home/zattew/Immagini',
        #       upload_filename='=#FORM.record.nome_completo',
        #       colspan=2)

        

    @public_method
    def getTime(self):
        #pasw='5H%5rsz6&mr97Yh1'
        #with ftplib.FTP('erp.pallacanestrocuoricinocardano.com', 'palcancarerp21', pasw) as ftp:
        #    ip=ftp.getwelcome().split(" ")[4]
        #    ip = ip.split('[')[1]
        #    ip = ip.split(']')[0]
        #    return ip
        #    ftp.close()
        #db = GnrApp('mybasket').db
        #tbliscritto= db.table('ball.iscritto')
        #f = tbliscritto.query(columns='$terra,$stato_estero').fetch()
        #for r in f:
        #    r = dict(r)
        #    oldr = dict(r)
        #    if r['stato_estero'] != "ITALIA":
        #        r['terra'] = 'cancellato'
        #    else:
        #        r['terra'] = 'cancellato'
        #    tbliscritto.raw_update(r,oldr,pkey=r['pkey'])
        #db.commit()
        return '... ATTENDI ... MA NULLA ACCADE!'


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
