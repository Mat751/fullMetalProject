#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('protocollo')
        r.fieldcell('genitore')
        r.fieldcell('gen_cod_fisc')
        r.fieldcell('iscritto')
        r.fieldcell('isc_cod_fisc')
        r.fieldcell('data')
        r.fieldcell('modalita')
        r.fieldcell('importo')
        r.fieldcell('data2')
        r.fieldcell('modalita2')
        r.fieldcell('importo2')
        r.fieldcell('totale')

    def th_order(self):
        return 'protocollo'

    def th_query(self):
        return dict(column='protocollo', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('protocollo')
        fb.field('genitore')
        fb.field('gen_cod_fisc')
        fb.field('iscritto')
        fb.field('isc_cod_fisc')
        fb.field('data')
        fb.field('modalita')
        fb.field('importo')
        fb.field('data2')
        fb.field('modalita2')
        fb.field('importo2')
        fb.field('totale')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
