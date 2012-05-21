import os
from flask import url_for
from application import app


class KozDoc(app.Document):
    pass


class CourrierStandard(KozDoc):
    type_name = 'courrier standard'
    model_path = os.path.join(
        app.config['MODELS'], 'Courrier', 'courrier standard')
    document_id_template = '{document_name}'


class FactureAbonnement(KozDoc):
    type_name = 'facture abonnement'
    model_path = os.path.join(
        app.config['MODELS'], 'Facture', 'facture abonnement')
    document_id_template = '{document_name}'
