<%inherit file="base.mako"/>

<%def name="title()">
Home | 
</%def>

<%def name="h1()">
Tic-Tac-Toe!
</%def>

<%def name="extrascript()">
<script type="text/javascript">
$(function() {
    $('button.big-button').live('click', function() {
        window.location.href = $(this).closest('a').attr('href');
        return false;
    });
});
</script>
</%def>

<a href="/game/new/ai/"><button class="big-button">Play the Computer!</button></a>
<a href="/game/new/versus/"><button class="big-button">Play Versus a Friend!</button></a>
