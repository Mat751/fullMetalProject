
# encoding: utf-8
from gnr.core.gnrdecorator import metadata


class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('allenatore_compenso', pkey='id', name_long='Compenso',
                      name_plural='Compensi',caption_filed='protocollo')
        self.sysFields(tbl)
        
        

        tbl.column('protocollo', name_long='Protocollo')
        tbl.column('codice_allenatore',size='22', group='_', name_long='Allenatore'
                    ).relation('allenatore.id', relation_name='compensi', mode='foreignkey', onDelete='cascade')
        tbl.column('data', dtype='D', name_long='Data Pagamento')
        tbl.column('importo', dtype='N', name_long='Importo')
        tbl.column('note', name_long='Note')
        tbl.column('entrate_uscite', name_long='Entrate o Uscite')

    def defaultValues(self):
        return dict(data=self.db.workdate,entrate_uscite="Uscite",importo=500)

    def counter_protocollo(self, record=None):
      pars = dict(format='$K$YY.$NNNNN', period='YY', code='M',
                  date_field='data', showOnLoad=True, recycle=False, date_tolerant=True,
                  message_dateError="Impossibile creare riga in data corrente. Ultima riga in data %(last_used)s",
                  message_failed='La riga ha ricevuto un protocollo differente da quello in precedenza allocato: %(sequence)s')
      return pars