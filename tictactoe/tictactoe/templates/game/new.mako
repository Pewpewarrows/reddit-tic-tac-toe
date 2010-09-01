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

<table>
    % for r in range(c.board_size):
    <tr>
        % for i in range(c.board_size):
        <td>${c.positions[r][i] | move_to_img}</td>
        % endfor
    </tr>
    % endfor
</table>
