
#!/usr/bin/env python
# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('allenatore', pkey='id', name_long='Allenatore',
                        name_plural='Allenatori', caption_field='nome_completo')
        self.sysFields(tbl)
        
        tbl.column('nome', name_long='Nome')
        tbl.column('cognome', name_long='Cognome')
        tbl.column('data_nascita', dtype='D', name_long='Data Nascita')
        tbl.column('sesso', name_long='Sesso')
        provincia = tbl.column('provincia', size='2', name_long='Provincia',
                               name_short='Pr.')

        provincia.relation('glbl.provincia.sigla',
                           relation_name='allenatori',
                           mode='foreignkey',
                           onDelete='raise')
        tbl.column('comune_id', size='22', group='_', name_long='Comune').relation('glbl.comune.id',
                                                                                    relation_name='allenatori',
                                                                                    mode='foreignkey',
                                                                                    onDelete='raise')
        tbl.column('codice_fiscale', name_long='Codice Fiscale')

        tbl.column('email', name_long='Email')
        tbl.column('ruolo', name_long='Ruolo')
        tbl.column('note', name_long='Note')
        tbl.column('voto', name_long='Valutazione')
        
        tbl.formulaColumn('nome_completo',"$nome || ' ' || $cognome",onDelete='cascade')