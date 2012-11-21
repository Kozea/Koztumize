#! /usr/bin/env python2
"""Executable file for Koztumize."""

from koztumize.routes import nuts

nuts.app.secret_key = 'Azerty'
nuts.app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
