/* Declare a namespace for the site */
var TicTacToe = window.TicTacToe || {};

/* Create a closure to maintain scope of the '$'
   and remain compatible with other frameworks.  */
(function($) {

    TicTacToe = {
        init: function() {}
    };
	
	$(function() {
	});

	$(window).bind("load", function() {
	});
	
})(jQuery);
