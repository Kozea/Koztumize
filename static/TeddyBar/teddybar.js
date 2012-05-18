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
			document : function () { return document.getElementById('iframe').contentWindow.document },
			menu : {
				'Gras': 'bold',
				'Italique': 'italic',
				'Souligner': 'underline',
				'Barrer': 'strikethrough',
				'-1': null,
				'Police': ['fontname', {'- Police -': '0','Serif': 'serif', 'Sans-serif': 'sans-serif','Courier': 'courier new'}],
				'Taille': ['fontsize', {'- Taille -': '0','1 (8pt)': '1', '2 (10pt)': '2','3 (12pt)': '3','4 (14pt)': '4','5 (18pt)': '5','6 (24pt)': '6','7 (36pt)': '7'}],
				'Format': ['formatblock', {'- Format -': '0','Heading 1': 'h1','Heading 2': 'h2','Heading 3': 'h3','Heading 4': 'h4','Heading 5': 'h5','Heading 6': 'h6','Paragraph': 'p','Preformatted': 'pre'}],
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
                'Générer le PDF': 'pdf'
			},
			commands : {
                'save': function() { 
					var divs = $('#iframe').contents().find('div[contenteditable]');
                    var data = [];
                    $.each(divs, function () {
                        data.push({
                            "part": $(this).attr('data-part'),
                            "document_type": $(this).attr('data-document-type'),
                            "document_id": $(this).attr('data-document-id'),
                            "version": $(this).attr('data-document-version'),
                            "content": $(this).html()
                        });
                    });
                    // Make ajax
					$.ajax({
						url: "/save/courrier%20standard",
						data: JSON.stringify(data),
						contentType: 'application/json',
						dataType: 'json',
						type: "POST",
						success: function(response){
						    if(response && response.documents) {
                                var message = 'Contenu enregistré.';
                                var div = $('<div>', {'class': 'ok'}).html(message);
                                $('body>section').before(div);
                                div.slideDown(300).delay(3000).fadeOut();
                                $.each(response.documents, function () {
                                    var divs = $('#iframe').contents().find(
                                        'div[contenteditable]' +
                                        '[data-document-type="' + this.document_type + '"]' +
                                        '[data-document-id="' + this.document_id + '"]'
                                    );
                                    divs.attr('data-document-version', this.version);
                                });
                            } else {
                                var message = 'Conflit: Veuillez rafraîchir la page.';
                                var div = $('<div>', {'class': 'error'}).html(message);
                                $('body>section').before(div);
                                div.slideDown(300).delay(3000).fadeOut();
                            }            
                        }
					});			
				},
				'pdf': function() {
				    this.save();
				    var loader = $('<div>', {'class': 'loading'});
				    loader.fadeIn(500);
				    
				    $.ajax({
					    url: "/pdf_link/courrier%20standard/Friday",
					    success: function(response){
						    $('#loader').hide();
						    window.location=response;
					    }
				    });
                }
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
			$('select').change(function() {
				var command = $(this).attr('data-command');
				var value = $(this).val();
				if (command in config.commands) {
					config.commands[command](value);
				} else {
					config.document().execCommand(command,false,value);
				}
				$(this).children().first().attr('selected','true');
			});
            
			// execCommand on input elements
			$('input[type=button]').on('click', function () {
				var command = $(this).attr('data-command');
				if (command in config.commands) {
					config.commands[command]();
				} else {
					config.document().execCommand(command,false,'');
				}
			});
       
			// Puts the body down, according to the toolbar's height
			$('body').css('margin-top', $this.height());
			$(window).resize(function() {
				$('body').css('margin-top', $this.height());
			});
		});
	};
})(jQuery);
