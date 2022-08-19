
from gnr.app.gnrapp import GnrApp

if __name__ == '__main__':
    db = GnrApp('mybasket').db
    tbliscritto= db.table('ball.iscritto')
    f = tbliscritto.query(columns='$terra,$stato_estero').fetch()
    for r in f:
        r = dict(r)
        oldr = dict(r)
        if r['stato_estero'] != "ITALIA":
            r['terra'] = 'Sangue Sporco'
        else:
            r['terra'] = 'Puro Sangue'
        tbliscritto.raw_update(r,oldr,pkey=r['pkey'])
        db.commit()