<%inherit file="/base.mako"/>

<%def name="title()">
Choose Difficulty | 
</%def>

<%def name="h1()">
Tic-Tac-Toe!
</%def>

<div class="message">Choose a difficulty!</div>
<br/>
<a href="/game/new/ai/easy/"><button class="big-button">Easy</button></a>
<a href="/game/new/ai/med/"><button class="big-button">Medium</button></a>
<a href="/game/new/ai/hard/"><button class="big-button">Hard</button></a>
