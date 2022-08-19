#!/usr/bin/env python
# encoding: utf-8
from gnr.app.gnrdbo import GnrDboTable, GnrDboPackage

class Package(GnrDboPackage):
    def config_attributes(self):
        return dict(comment='ball package',sqlschema='ball',sqlprefix=True,
                    name_short='Ball', name_long='Ball', name_full='Ball')
                    
    def config_db(self, pkg):
        pass
        
class Table(GnrDboTable):
    pass
