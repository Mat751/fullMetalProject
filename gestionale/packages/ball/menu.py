#!/usr/bin/env python
# encoding: utf-8


def anagrafica(root,application=None):
    ball = root.branch(u"Anagrafica")
    ball.thpage(u"!!Iscritti", table="ball.iscritto")
    #ball.thpage(u"!!Genitori", table='ball.genitore')
    ball.thpage(u"!!Allenatori", table="ball.allenatore")

def pagamenti(root,application=None):
    ball1 = root.branch(u"Pagamenti")
    ball1.thpage(u"!!Pagamenti Allenatori", table="ball.allenatore_compenso")
    ball1.thpage(u"!!Pagamenti iscritti/genitori", table="ball.genitore_pagamento")
    
def tabelle_fiscali(root,application=None):
    ball1 = root.branch(u"Tabelle fiscali")
    ball1.thpage(u"!!Tabella Fiscale Allenatori", table="ball.allenatore_tabella_fiscale")
    #ball1.thpage(u"!!Tabella Fiscale Genitori", table="ball.genitore_tabella_fiscale")
    ball1.thpage(u"!!Salario annuale allenatori", table="ball.allenatore_compenso_annuale")

def config(root,application=None):
    basket= root.branch(u'!!Basket')
    anagrafica(basket)
    pagamenti(basket)
    tabelle_fiscali(basket)