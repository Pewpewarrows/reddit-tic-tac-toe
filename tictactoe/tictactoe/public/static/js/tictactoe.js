/* Declare a namespace for the site */
var TicTacToe = window.TicTacToe || {};

/* Create a closure to maintain scope of the '$'
   and remain compatible with other frameworks.  */
(function($) {

    TicTacToe = {
        init: function() {},
        parse: function(grid) {
            for (var r in grid) {
                for (var c in grid[r]) {
                    if (grid[r][c] == 'X') {
                        $('#game-table tbody tr:nth-child(' + (parseInt(r)+1) +
                                ')').find('td:nth-child(' + (parseInt(c)+1) +
                                ')').html('<img src="/static/images/x-symbol.png"/>');
                    } else if (grid[r][c] == 'O') {
                        $('#game-table tbody tr:nth-child(' + (parseInt(r)+1) +
                                ')').find('td:nth-child(' + (parseInt(c)+1) +
                                ')').html('<img src="/static/images/o-symbol.png"/>');
                    } else {
                    }
                }
            }
        },
        gen_bitmask: function() {
            mask = '';

            $('#game-table tbody tr').each(function() {
                $('td', this).each(function() {
                    if ($('img', this).attr('src') == '/static/images/x-symbol.png') {
                        mask += '1';
                    } else if ($('img', this).attr('src') == '/static/images/o-symbol.png') {
                        mask += '1';
                    } else {
                        mask += '0';
                    }
                });
            });

            return mask;
        }
    };
	
	$(function() {
	});

	$(window).bind("load", function() {
	});
	
})(jQuery);
