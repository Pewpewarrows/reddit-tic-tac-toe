<%inherit file="/base.mako"/>

<%!
    from tictactoe.lib.filters import move_to_img, i_to_b
%>

<%def name="title()">
Continue Game | 
</%def>

<%def name="h1()">
Tic-Tac-Toe!
</%def>

<%def name="extrascript()">
<noscript>
    <meta http-equiv="refresh" content="30"/>
</noscript>

<script type="text/javascript">
function comet_poll(first) {
    TicTacToe.my_turn = false;

    $.post('${c.this_url}comet/', {
        my_board: TicTacToe.gen_bitmask()
    }, function(data) {
        if (first && TicTacToe.ignore) {
            return;
        }

        if (data.again == true) {
            setTimeout(comet_poll, 1);
        } else if (data.result || data.message) {
            if (data.message) {
                $('.message').html(data.message);
            }

            if (data.result) {
                TicTacToe.parse(data.result);
            }

            TicTacToe.my_turn = true;
            TicTacToe.ignore = true;
        }
    });
}

$(function() {
    TicTacToe.ignore = false;
    TicTacToe.my_turn = true;

    $('meta[http-equiv="refresh"]').remove();

    $('form.game-move').live('submit', function() {
        $.post('${c.this_url}', {
            move: $('input[name="move"]', this).val()
        }, function(data) {
            TicTacToe.parse(data.result);
            TicTacToe.ignore = true;

            if (TicTacToe.my_turn) {
                comet_poll(false);
            }
        });

        return false;
    });

    comet_poll(true);
    TicTacToe.my_turn = true;
});
</script>
</%def>

<div>Tell your friend to visit <a href="${c.this_url}">this link</a> to play!</div>

<div class="message">${c.message}</div>

<div id="controls">
<!--
<form action="." method="post">
    <input type="hidden" name="reset" value="true"/>
    <input type="submit" value="Reset Game"/>
</form>
-->
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
