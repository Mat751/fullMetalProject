class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('iscritto', pkey='id', name_long='Iscritto', name_plural='Iscritti',caption_field='nome_completo')
        self.sysFields(tbl)
        
    
        tbl.column('nome', name_long='Nome')
        tbl.column('cognome', name_long='Cognome')
        tbl.column('data_nascita', dtype='D', name_long='Data Nascita')
        tbl.column('sex', size=':1', name_long='Sesso')
        tbl.column('stato_estero', name_long='Stato Nascita')
        
        
        tbl.column('comune_id', name_long='Comune Nascita')
        #comune.relation('glbl.comune.id',relation_name='iscritti',
        #               mode='foreignkey',onDelete='raise')
        tbl.column('provincia', size=':4', name_long='Provincia', name_short='Prov.')
         #provincia.relation('glbl.provincia.sigla',
        #                   relation_name='iscritti',
         #                  mode='foreignkey',
          #                 onDelete='raise')

        tbl.column('codice_fiscale', name_long='Codice Fiscale')

        tbl.column('data_iscrizione', dtype='D', name_long='Data Iscrizione')
        tbl.formulaColumn('nome_completo',"$nome || ' ' || $cognome")
        
        
        tbl.column('anni', dtype='N', name_long='Anni')
        tbl.column('categoria', name_long='Categoria')

        tbl.column('peso', dtype='N', name_long='Peso')
        tbl.column('altezza', dtype='N', name_long='Altezza')
        tbl.column('ruolo', name_long='Ruolo')
        tbl.column('voto', name_long='Valutazione')
        tbl.column('photo_url', dtype='P',name_long='Foto')
        tbl.column('email', name_long='Email')
        tbl.column('note_iscritto',name_long='Note')
        #tbl.column('modulo_iscrizione', name_long='Iscrizione',dtype='B')
        #tbl.column('terra', name_long='Terra')

        tbl.column('nome_genitore',name_long='Nome genitore')
        tbl.column('cognome_genitore',name_long='Cognome genitore')
        tbl.column('codice_fiscale_genitore',name_long='Codice Fiscale gen.')
        tbl.column('pagamento', name_long='Tipo pagamento')
        tbl.column('pagamento2', name_long='Tipo pagamento')
        tbl.column('pagamento_iscritto',name_long='Pagamento:')    

        tbl.column('importo1', dtype='N', name_long='Importo 1:')
        tbl.column('data1', dtype='D', name_long='Data 1:')
        tbl.column('importo2', dtype='N', name_long='Importo 2:')
        tbl.column('data2', dtype='D', name_long='Data 2:')

        tbl.formulaColumn('pag_completo',"""CASE WHEN $importo1 IS NOT NULL AND
                                            $importo2 IS NOT NULL THEN TRUE
                                            WHEN $importo1 IS NOT NULL AND 
                                            $importo2 IS NULL THEN FALSE
                                            WHEN $importo1 IS NULL AND
                                            $importo2 IS NOT NULL THEN FALSE
                                            ELSE NULL END""",
                                            dtype='B',name_long='Pagamenti anno corrente')

        tbl.formulaColumn('num_figli',select=dict(table='ball.iscritto',
                                                columns='COUNT(*)',
                                                where="$codice_fiscale_genitore=#THIS.codice_fiscale_genitore AND $pagamento_iscritto='Genitore'"),
                                    dtype='L',name_long='Figli a carico del genitore: ')

    def defaultValues(self):
        return dict(stato_estero='ITALIA')