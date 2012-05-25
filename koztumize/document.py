# -*- coding: utf-8 -*-

import os
import locale
from application import app
from itertools import islice, chain


def priceformat(amount):
    if isinstance(amount, basestring):
        amount = amount.replace(',', '.')
    return locale.format_string('%.2f', float(amount))


class KozDoc(app.Document):
    def __init__(self, document_id, version=None):
        super(KozDoc, self).__init__(document_id, version)


class CourrierStandard(KozDoc):
    type_name = 'courrier standard'
    model_path = os.path.join(
        app.config['MODELS'], 'Courrier', 'courrier standard')
    document_id_template = '{document_name}'


class FactureAbonnement(KozDoc):
    def __init__(self, document_id, version=None):
        super(FactureAbonnement, self).__init__(document_id, version=None)
        self.jinja_environment.filters['priceformat'] = priceformat

    type_name = 'facture abonnement'
    model_path = os.path.join(
        app.config['MODELS'], 'Facture', 'facture abonnement')
    document_id_template = '{document_name}'

    def render_prix(self, data):

        def batch(iterable, size):
            sourceiter = iter(iterable)
            while True:
                batchiter = islice(sourceiter, size)
                yield tuple(chain([batchiter.next()], batchiter))

        total_ht = 0
        total_tva = 0
        for row in batch(data, 4):
            total_ligne = int(row[1]) * (float(row[2].replace(',', '.')) * 100)
            total_ht = total_ht + total_ligne
            tva_ligne = total_ligne * (float(row[3].replace(',', '.')) / 100)
            total_tva = total_tva + tva_ligne

        return self.jinja_environment.get_template('prix.jinja2').render(
            data=data, total_ht=total_ht, total_tva=total_tva)
