
# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('iscritto_ricevute_fiscali', pkey='id', name_long='Tesserato ricevuta fiscale', name_plural='Tesserati ricevute fiscali')
        self.sysFields(tbl)
        
        #nome (genitore),cognome (genitore), data nascita (genitore),
        #luogo nascita (genitore), totale pagato - mod. pagamento (bonifico e assegno)