
# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('genitore', pkey='id', name_long='Genitore', name_plural='Genitori',caption_field='nome_completo')
        self.sysFields(tbl)
        
        tbl.column('nome', name_long='Nome')
        tbl.column('cognome', name_long='Cognome')
        tbl.column('data_nascita', dtype='D', name_long='Data Nascita')
        tbl.column('sesso', size=':1', name_long='Sesso')
        tbl.column('stato_estero', name_long='Stato Nascita')
        tbl.column('comune_id', name_long='Comune Nascita')
        tbl.column('provincia', size=':4', name_long='Provincia', name_short='Prov.')
        tbl.column('codice_fiscale', name_long='Codice Fiscale')
        tbl.column('email', name_long='Email')
        tbl.column('figli', dtype='N', name_long='Figli iscritti')
        tbl.column('note', name_long='Note')
        tbl.formulaColumn('nome_completo',"$nome || ' ' || $cognome")