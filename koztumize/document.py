"""Documents for Koztumize."""
# -*- coding: utf-8 -*-

import os
import locale
from itertools import islice, chain
from .application import nuts


def priceformat(amount):
    """Return amount formatted according into its locale."""
    if isinstance(amount, basestring):
        amount = amount.replace(',', '.')
    return locale.format_string('%.2f', float(amount))


class KozDoc(nuts.Document):
    """Base class for Koztumize documents."""
    def __init__(self, document_id, version=None):
        super(KozDoc, self).__init__(document_id, version)


class CourrierStandard(KozDoc):
    """Class for Standard Letter document."""
    type_name = 'courrier standard'
    model_path = os.path.join(
        nuts.app.config['MODELS'], 'Courrier', 'courrier standard')
    document_id_template = '{document_name}'


class FactureStandard(KozDoc):
    """Class for Bills document."""
    def __init__(self, document_id, version=None):
        super(FactureStandard, self).__init__(document_id, version)
        self.jinja_environment.filters['priceformat'] = priceformat

    type_name = 'facture standard'
    model_path = os.path.join(
        nuts.app.config['MODELS'], 'Facture', 'facture standard')
    document_id_template = '{document_name}'

    def render_prix(self, data):
        """Render the price for the total table."""
        def batch(iterable, size):
            """Allow list batching."""
            sourceiter = iter(iterable)
            while True:
                batchiter = islice(sourceiter, size)
                yield tuple(chain([batchiter.next()], batchiter))

        total_ht = 0
        total_tva = 0
        for row in batch(data, 4):
            row = list(row)
            if not row[1].isdigit():
                row[1] = '1'
            total_ligne = int(row[1]) * (float(row[2].replace(',', '.')) * 100)
            total_ht = total_ht + total_ligne
            tva_ligne = total_ligne * (float(row[3].replace(',', '.')) / 100)
            total_tva = total_tva + tva_ligne

        return self.jinja_environment.get_template('prix.jinja2').render(
            data=data, total_ht=total_ht, total_tva=total_tva)


class FactureAbonnement(KozDoc):
    """Class for Bills document."""
    def __init__(self, document_id, version=None):
        super(FactureAbonnement, self).__init__(document_id, version)
        self.jinja_environment.filters['priceformat'] = priceformat

    type_name = 'facture abonnement'
    model_path = os.path.join(
        nuts.app.config['MODELS'], 'Facture', 'facture abonnement')
    document_id_template = '{document_name}'

    def render_prix(self, data):
        """Render the price for the total table."""
        def batch(iterable, size):
            """Allow list batching."""
            sourceiter = iter(iterable)
            while True:
                batchiter = islice(sourceiter, size)
                yield tuple(chain([batchiter.next()], batchiter))

        total_ht = 0
        total_tva = 0
        for row in batch(data, 4):
            row = list(row)
            if not row[1].isdigit():
                row[1] = '1'
            total_ligne = int(row[1]) * (float(row[2].replace(',', '.')) * 100)
            total_ht = total_ht + total_ligne
            tva_ligne = total_ligne * (float(row[3].replace(',', '.')) / 100)
            total_tva = total_tva + tva_ligne

        return self.jinja_environment.get_template('prix.jinja2').render(
            data=data, total_ht=total_ht, total_tva=total_tva)
