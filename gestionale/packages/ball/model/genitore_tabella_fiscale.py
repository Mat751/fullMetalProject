
# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('genitore_tabella_fiscale', pkey='id', name_long='Tabella fiscale genitore', name_plural='Tabelle fiscali genitore',caption_field='')
        self.sysFields(tbl)
        
        tbl.column('nome', name_long='Nome')
        tbl.column('cognome', name_long='Cognome')
        tbl.column('data_nascita', dtype='D', name_long='Data di nascita')
        tbl.column('codice_fiscale',size='22', group='_', name_long='Codice Fiscale'
                    ).relation('genitore.id', relation_name='genitori_pagamenti', mode='foreignkey', onDelete='raise')
        tbl.column('pagamento', dtype='N', name_long='Pagamento')
        tbl.column('mod_pagamento', name_long='Modalità pagamento')

        tbl.formulaColumn('nome_cognome',"$nome || ' ' || $cognome")