#! /usr/bin/env python2
"""Executable file for Koztumize."""

from koztumize.routes import nuts
app = nuts.app

app.secret_key = 'Azerty'
if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
