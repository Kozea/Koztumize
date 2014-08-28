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
Helpers for tests, with definition of decorator and function.

"""
from koztumize import application
from functools import wraps
from nose.tools import eq_


def with_client(function):
    """Create the test_client."""
    @wraps(function)
    def wrapper(*args, **kwargs):
        """Decorator for the client login."""
        client = application.app.test_client()
        client.post('login', data={'login': 'Tester', 'passwd': 'pass'})
        return function(client=client, *args, **kwargs)
    return wrapper


def request(method, route, status_code=200, content_type='text/html',
            data=None, data_content_type='application/x-www-form-urlencoded',
            follow_redirects=True):
    """
    Create the test_client  and check status code and content_type.
    """
    response = method(route, content_type=data_content_type, data=data,
                      follow_redirects=follow_redirects)
    eq_(response.status_code, status_code)
    assert content_type in response.content_type
    return response
