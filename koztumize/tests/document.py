import os

from koztumize.document import KozDoc
from koztumize import application


class Test(KozDoc):
    type_name = 'test'
    model_path = os.path.join(
        application.app.config['MODELS'], 'Test', 'test')
    document_id_template = '{document_name}'