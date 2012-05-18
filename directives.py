from docutils.parsers.rst import directives, Directive, roles
import docutils.core
import os

import pynuts.directives


class Button(Directive):
    """A rest directive who create a button in HTML."""
    required_arguments = 2
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False
    option_spec = {'class': directives.class_option}

    def run(self):
        content = ('<input type="button" class="%s" value="%s" onclick="%s"/>'
                  % (
                      ' '.join(self.options.get('class', [])),
                      self.arguments[0], self.arguments[1],
                  ))
        return [docutils.nodes.raw('', content, format='html')]


# The signature of this function is given by docutils
# pylint: disable=R0913,W0613
def editable(name, rawtext, text, lineno, inliner, options=None,
             content=None):
    """."""
    content = '<span contenteditable="true">%s</span>' % text
    return [docutils.nodes.raw('', content, format='html')], []

roles.register_canonical_role('editable', editable)


class Script(Directive):
    """A rest directive which creates a script tag in HTML."""
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False

    def run(self):
        document_type, document_id, version, filename = \
            self.arguments[0].split('/')
        cls = self.state.document.settings._pynuts.documents[document_type]
        document = cls(document_id, version)
        path = document.resource_url(os.path.join('javascript', filename))
        content = ('<script src="%s.js" type="text/javascript"></script>'
                   % path)
        return [docutils.nodes.raw('', content, format='html')]


class Button(Directive):
    """A rest directive who create a button in HTML."""
    required_arguments = 2
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False
    option_spec = {'class': directives.class_option}

    def run(self):
        content = ('<input type="button" class="%s" value="%s" onclick="%s"/>'
                  % (
                      ' '.join(self.options.get('class', [])),
                      self.arguments[0], self.arguments[1],
                  ))
        return [docutils.nodes.raw('', content, format='html')]


class JQuery(Directive):
    """A rest directive which includes JQuery."""
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False

    def run(self):
        content = ('<script src="http://code.jquery.com/jquery.min.js"\
                   type="text/javascript"></script>')
        return [docutils.nodes.raw('', content, format='html')]


class Checkbox(Directive):
    """A rest directive who create a checkbox in HTML."""
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False

    def run(self):
        content = (
            '<input type="checkbox" '
            'onChange="this.setAttribute('
            '\'checked\', this.checked?\'checked\':\'\');"/>')
        return [docutils.nodes.raw('', content, format='html')]


directives.register_directive('checkbox', Checkbox)
directives.register_directive('editable', pynuts.directives.Editable)
directives.register_directive('script', Script)
directives.register_directive('jquery', JQuery)
directives.register_directive('button', Button)
