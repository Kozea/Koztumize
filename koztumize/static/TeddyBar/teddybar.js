// Copyright (C) 2012 Kozea
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.

(function ($) {
    $.fn.teddybar = function (options) {
        var config = {
            document : function () { return document.getElementById('iframe').contentWindow.document; },
            menu : {
                'Gras': 'bold',
                'Italique': 'italic',
                'Souligner': 'underline',
                'Barrer': 'strikethrough',
                '-1': null,
                'Police': ['fontname', {'- Police -': '0','Serif': 'serif', 'Sans-serif': 'sans-serif','Courier': 'courier new'}],
                'Taille': ['fontsize', {'- Taille -': '0','1 (8pt)': '1', '2 (10pt)': '2','3 (12pt)': '3','4 (14pt)': '4','5 (18pt)': '5','6 (24pt)': '6','7 (36pt)': '7'}],
                'Format': ['formatblock', {'- Format -': '0','Titre 1': 'h1','Titre 2': 'h2','Titre 3': 'h3','Titre 4': 'h4','Titre 5': 'h5','Titre 6': 'h6','Paragraphe': 'p','Preformaté': 'pre'}],
                '-2': null,
                'Liste numerotée': 'insertorderedlist',
                'Liste': 'insertunorderedlist',
                '-3': null,
                'Aligner à gauche': 'justifyleft',
                'Aligner à droite': 'justifyright',
                'Centrer': 'justifycenter',
                'Justifier': 'justifyfull',
                '-4': null,
                'Annuler': 'undo',
                'Refaire': 'redo',
                '-5': null,
                'Enregistrer le document': 'save',
                'Enregistrer le document avec un message': 'save_as',
                'Générer le PDF': 'pdf',
                '-6': null,
                'Options': 'settings'
            }
        };
        if (options) {
            $.extend(true, config, options);
        }
        return this.each(function () {
            var $this=$(this);
            var block = $('<ul>').appendTo($this);
            $.each(config.menu, function (name, command) {
                if (command == null) {
                    // make a separator
                    block = $('<ul>').appendTo($this);
                } else if (typeof command == 'string') {
                    // make a button
                    $('<input>', {"title": name, "type": "button", "value": name, "class": command, "data-command": command}).appendTo(block).wrap('<li>');
                } else {
                    // make a select
                    $('<select>', {"title": name, "data-command": command[0]}).appendTo(block).wrap('<li>');
                    $.each(command[1], function(label, value) {
                        $('select[data-command='+command[0]+']').append($('<option>', {"value":value}).html(label));
                    });
                }
            });
            
            // execCommand on select elements
            $this.find('select').change(function() {
                var command = $(this).attr('data-command');
                var value = $(this).val();
                if (command in config.commands) {
                    config.commands[command](value);
                } else {
                    try {
                        config.document().execCommand("styleWithCSS", 0, false);
                    } catch (e) {
                        try {
                            config.document().execCommand("useCSS", 0, true);
                        } catch (e) {
                            try {
                                config.document().execCommand('styleWithCSS', false, false);
                            }
                            catch (e) {
                            }
                        }
                    }
                    config.document().execCommand(command,false,value);
                }
                $(this).find('option').first().attr('selected','selected');
            });
            
            // execCommand on input elements
            $this.find('input[type=button]').on('click', function () {
                var command = $(this).attr('data-command');
                if (command in config.commands) {
                    config.commands[command]();
                } else {
                    try {
                        config.document().execCommand("styleWithCSS", 0, false);
                    } catch (e) {
                        try {
                            config.document().execCommand("useCSS", 0, true);
                        } catch (e) {
                            try {
                                config.document().execCommand('styleWithCSS', false, false);
                            }
                            catch (e) {
                            }
                        }
                    }
                    config.document().execCommand(command,false,'');
                }
            });
        });
    };
})(jQuery);
