
# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('allenatore_compenso_annuale', pkey='codice_allenatore', 
                       name_long='Compenso Annuale')
        self.sysFields(tbl,id=False)

        tbl.column('codice_allenatore', group='_',name_long='Codice allenatore'
                    ).relation('allenatore.id', relation_name='compenso_annuale',
                     mode='foreignkey', onDelete='raise')

        tbl.column('gennaio', dtype='N', name_long='Gennaio')
        tbl.column('febbraio', dtype='N', name_long='Febbraio')
        tbl.column('marzo', dtype='N', name_long='Marzo')
        tbl.column('aprile', dtype='N', name_long='Aprile')
        tbl.column('maggio', dtype='N', name_long='Maggio')
        tbl.column('giugno', dtype='N', name_long='Giugno')
        tbl.column('luglio', dtype='N', name_long='Luglio')
        tbl.column('agosto', dtype='N', name_long='Agosto')
        tbl.column('settembre', dtype='N', name_long='Settembre')
        tbl.column('ottobre', dtype='N', name_long='Ottobre')
        tbl.column('novembre', dtype='N', name_long='Novembre')
        tbl.column('dicembre', dtype='N', name_long='Dicembre')
        tbl.column('totale', dtype='N', name_long='Totale')
        tbl.column('anno')   
        

         