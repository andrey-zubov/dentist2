$(document).ready(function () {
    $('.answer_question').submit(function (f) {
      f.preventDefault();
      let form_data = $(this).serializeArray();
      $.ajax({
          'type': 'POST',
          'url': '/ajax_save_question',
          'data': form_data,
          success: function (suc) {
              console.log('suc');
          },
          error: function (err) {
            console.log(err);
          }
      });
    });
  });