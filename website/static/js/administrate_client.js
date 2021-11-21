$(document).ready(function () {

    $('.change_client').click(function (f) {
        console.log('ds')
        let form = $(this).parent().parent();
        let cells = form.find('input');
        let client_id = $(this).attr('id').split('_')[1]
        console.log(client_id)
        cells.each(function () {
            $(this).attr('readonly', false);
        });
        $('.change_client').toggle();
        $('.delete_client').toggle();
        $('#save_'+client_id).toggle();
        $('#cancel_'+client_id).toggle();
    });

    $('.client_administration').submit(function (f) {
        f.preventDefault();
        let form_data = $(this).serializeArray();
        $.ajax({
            'type': 'post',
            'data': form_data,
            'url': '/ajax_save_client',
            success: function (suc) {
              console.log('suc');
              },
              error: function (err) {
                  console.log(err);
              },
        });

        let client_id = $(this).attr('id').split('_')[1]
        $('.change_client').toggle();
        $('.delete_client').toggle();
        $('#save_'+client_id).toggle();
        $('#cancel_'+client_id).toggle();

    });

    $('.cancel_client').click(function (f) {
        let client_id = $(this).attr('id').split('_')[1]
        $('.change_client').toggle();
        $('.delete_client').toggle();
        $('#save_'+client_id).toggle();
        $('#cancel_'+client_id).toggle();
    });



    // $('.answer_question').submit(function (f) {
    //   f.preventDefault();
    //   let form_data = $(this).serializeArray();
    //   $.ajax({
    //       'type': 'POST',
    //       'url': '/ajax_save_question',
    //       'data': form_data,
    //       success: function (suc) {
    //           console.log('suc');
    //       },
    //       error: function (err) {
    //         console.log(err);
    //       }
    //   });
    // });
  });