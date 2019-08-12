setTimeout(function() {
  $("#messages").slideUp();
}, 3000);

function voteOnTicket(id, csrf_token) {
  $("#vote-form").submit(function(e) {
    $('#messages').remove();
    e.preventDefault();
  });

  $.ajax({
    url: "/bugs_&_features/addvote/" + id + "/",
    type: "POST",
    data: {
      csrfmiddlewaretoken: csrf_token
    },
    success: function(result) {
      $("#votes").text(result.numVotes);
      $('#content-container').prepend(function() {
        if ($('#messages')) {
          if (result.status == 'Success') {
            return '<div id="messages" class="alert alert-success"><div class="messages">' + result.msg + '</div></div>';
          }
          else {
            return '<div id="messages" class="alert alert-danger"><div class="messages">' + result.msg + '</div></div>';
          }
        }
      });
    }
  });
}
