
class Table(object):
  def config_db(self, pkg):
      tbl = pkg.table('allenatore_categoria', pkey='codice', name_long='Allenatore Categoria',
                      name_plural='Allenatori Categorie', caption_field='descrizione', lookup=True)

      self.sysFields(tbl, id=False)

      tbl.column('codice', size=':5', name_long='Codice')
      tbl.column('descrizione', name_long='Descrizione')