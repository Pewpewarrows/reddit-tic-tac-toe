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

<%def name="extrascript()">
<script type="text/javascript">
function comet_poll() {
    $.post('${c.this_url}comet/', {
        my_board: TicTacToe.gen_bitmask()
    }, function(data) {
        if (data.again == true) {
            setTimeout(comet_poll, 1);
        } else if (data.results) {
            TicTacToe.parse(data.results);
        }
    });
}

$(function() {
    $('form.game-move').live('submit', function() {
        $.post('${c.this_url}', {
            move: $('input[name="move"]', this).val()
        }, function(data) {
            TicTacToe.parse(data.result);
        });

        return false;
    });
});
</script>
</%def>


<div class="message">${c.message}</div>

<div id="controls">
<form action="." method="post">
    <input type="hidden" name="reset" value="true"/>
    <input type="submit" value="Reset Game"/>
</form>
</div>

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
        % if (not c.finished) and (c.positions[r][i] == ''):
        <form class="game-move" action="." method="post">
        <input type="hidden" name="move" value="${(1 << ((c.board_size**2) - (r * c.board_size + i) - 1)) | i_to_b}"/>
        % endif
        % if (c.positions[r][i] != '') or ((not c.finished and c.positions[r][i] == '')):
        ${c.positions[r][i] | move_to_img}
        % endif
        % if (not c.finished) and (c.positions[r][i] == ''):
        </form>
        % endif
        </td>
        % endfor
    </tr>
    % endfor
</table>
