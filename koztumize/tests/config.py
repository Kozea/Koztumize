# Copyright (C) 2011 Kozea
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
The testing config file of kuztumize.

"""
import os


PATH = os.path.dirname(__file__)
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://koztumize:koztumize@localhost/koztumize_test'
PYNUTS_DOCUMENT_REPOSITORY = os.path.join(PATH, 'fake_instance', 'documents.git')
GIT_REMOTE = 'git://github.com/Kozea/Koztumize.git'
SECRET_KEY = 'test'
TESTING = True
