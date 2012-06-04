#! /usr/bin/env python2

from koztumize.routes import app

app.secret_key = 'Azerty'
app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
