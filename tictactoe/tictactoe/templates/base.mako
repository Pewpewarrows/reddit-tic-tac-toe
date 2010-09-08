<!doctype html>
	
<!-- Much of this was inspired by the HTML5 Boilerplate and HTML5 Reset projects -->
			
<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ -->

<!--[if lt IE 7]>
<html lang="en" class="no-js ie ie6">
<![endif]-->
<!--[if IE 7]>
<html lang="en" class="no-js ie ie7">
<![endif]-->
<!--[if IE 8]>
<html lang="en" class="no-js ie ie8">
<![endif]-->
<!--[if IE 9]>
<html lang="en" class="no-js ie ie9">
<![endif]-->
<!--[if gt IE 9]>
<html lang="en" class="no-js">
<![endif]-->
<!--[if !IE]><!-->
<html lang="en" class="no-js">
<!--<![endif]-->
<head>
	<meta charset="utf-8" />
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<meta http-equiv="Content-Language" content="en" />
	
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	
	<!-- Give the browser the title before we start making more requests -->
	<title>${self.title()}Tic-Tac-Toe</title>
	
	<meta name="description" content="Play Tic-Tac-Toe versus your friends or a computer!" />
	<meta name="keywords" content="tic-tac-toe,tic,tac,toe" />
	<meta name="author" content="Marco Chomut" />
	
	<!--  Mobile Viewport Fix
	    j.mp/mobileviewport & davidbcalhoun.com/2010/viewport-metatag 
	device-width : Occupy full width of the screen in its current orientation
	initial-scale = 1.0 retains dimensions instead of zooming out if page height > device height
	maximum-scale = 1.0 retains dimensions instead of zooming in if page width < device width
	-->
	<meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0;">
	
	<meta name="google-site-verification" content="" />
	
	<link rel="shortcut icon" href="/static/images/favicon.ico" />
	<link rel="apple-touch-icon" href="/static/images/touch-icon.png" />
	
	<link rel="stylesheet" type="text/css" media="all" href="/static/css/tictactoe.css" />
	
    ${self.extrastyle()}

    ${self.extrahead()}

	<!--[if lt IE 9]>
	<script src="http://ie7-js.googlecode.com/svn/version/2.1(beta4)/IE9.js"></script>
	<![endif]-->
	
	<!-- All JavaScript at the bottom, except for Analytics and Modernizr which enables HTML5 elements & feature detects -->
	<script src="/static/js/modernizr-1.5.min.js"></script>
	
	<!-- Google Analytics Async Tracker -->
	<!-- http://mathiasbynens.be/notes/async-analytics-snippet -->
	<script type="text/javascript">
	//<![CDATA[
//		var _gaq = [['_setAccount', 'UA-XXXXX-X'], ['_trackPageview']];
//		(function(d, t) {
//			var g = d.createElement(t),
//			    s = d.getElementsByTagName(t)[0];
//			g.async = true;
//			g.src = '//www.google-analytics.com/ga.js';
//			s.parentNode.insertBefore(g, s);
//		})(document, 'script');
	//]]
	</script>
</head>
<body>
<div id="wrapper">
	<header>
		<div class="mini-wrap">
		<h1><a class="ir" href="/">Tic-Tac-Toe</a></h1>
        <!--
		<nav>
			<ul>
				<li><a href="/game/">Play!</a></li>
			</ul>
		</nav>
        -->
		</div>
	</header>
	<section id="content">
		<section id="title">
		<div class="mini-wrap">
			<h1>${self.h1()}</h1>
		</div>
		</section>
		<section id="main">
		<div class="mini-wrap">
        ${self.body()}
		</div>
		</section> <!-- end of #main -->
	</section> <!-- end of #content -->
	<div class="push"></div>
</div> <!-- end of #wrapper -->

<footer>
	<div class="mini-wrap">
	<hr/>
	<small>&copy; Copyright Marco Chomut 2010. All Rights Reserved.</small>
	</div>
</footer>
	
	<noscript></noscript>

	<!-- Grab Google CDN's jQuery. fall back to local if necessary -->
	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
	<script>!window.jQuery && document.write('<script src="/static/js/jquery-1.4.2.min.js"><\/script>')</script>

    ${self.extrascript()}
	
	<script src="/static/js/utils.js"></script>
	<script src="/static/js/tictactoe.js"></script>
	
	<!--[if lt IE 7 ]>
	<script src="/static/js/dd_belatedpng.js"></script>
	<![endif]-->
</body>
</html>

<%def name="extrastyle()">
</%def>

<%def name="extrahead()">
</%def>

<%def name="extrascript()">
</%def>
