
# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('allenatore_tabella_fiscale', pkey='id', name_long='Tabella fiscale', name_plural='Tabelle fiscali')
        self.sysFields(tbl)
        
        tbl.column('nome_allenatore', name_long='Nome e Cognome'
                    ).relation('allenatore.id', relation_name='Totali', mode='foreignkey', onDelete='raise')
        tbl.column('data_nascita_allenatore', name_long='Data nascita')
        tbl.column('comune_nascita_allenatore', name_long='Comune nascita')
        tbl.column('codice_fiscale_allenatore', name_long='Codice fiscale')
        tbl.column('allenatore_totale', dtype='N', name_long='Totale')
        tbl.column('anno', name_long='Anno')

    def defaultValues(self):
        return dict(anno='2021')

