<%inherit file="/base.mako"/>

<%def name="title()">
Choose Difficulty | 
</%def>

<%def name="h1()">
Tic-Tac-Toe!
</%def>

<%def name="extrascript()">
<script type="text/javascript">
$(function() {
    $('button.big-button').live('click', function() {
        window.location.href =
        $(this).closest('a').attr('href');
    });
});
</script>
</%def>


<div class="message">Choose a difficulty!</div>
<br/>
<a href="/game/new/ai/easy/"><button class="big-button">Easy</button></a>
<a href="/game/new/ai/med/"><button class="big-button">Medium</button></a>
<a href="/game/new/ai/hard/"><button class="big-button">Hard</button></a>
