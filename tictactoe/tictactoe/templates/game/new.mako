<%inherit file="/base.mako"/>

<%!
    from tictactoe.lib.filters import move_to_img
%>

<%def name="title()">
New Game | 
</%def>

<%def name="h1()">
Tic-Tac-Toe!
</%def>

${c.board_size}
${c.positions}

<table id="game-table">
    % for r in range(c.board_size):
    % if r == 0 or r == 1:
    <tr class="bottom-bord">
    % else:
    <tr>
    % endif
        % for i in range(c.board_size):
        % if i == 0 or i == 1:
        <td class="right-bord">
        % else:
        <td>
        % endif
        ${c.positions[r][i] | move_to_img}</td>
        % endfor
    </tr>
    % endfor
</table>
