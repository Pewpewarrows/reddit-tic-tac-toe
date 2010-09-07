<%inherit file="/base.mako"/>

<%!
    from tictactoe.lib.filters import move_to_img, i_to_b
%>

<%def name="title()">
New Game | 
</%def>

<%def name="h1()">
Tic-Tac-Toe!
</%def>

<form action="." method="post">
    <input type="hidden" name="reset" value="true"/>
    <input type="submit" value="Reset Game"/>
</form>

${c.message}

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
        % if not c.finished:
        <form action="." method="post">
        <input type="hidden" name="move" value="${(1 << ((c.board_size**2) - (r * c.board_size + i) - 1)) | i_to_b}"/>
        % endif
        ${c.positions[r][i] | move_to_img}
        % if not c.finished:
        </form>
        % endif
        </td>
        % endfor
    </tr>
    % endfor
</table>
