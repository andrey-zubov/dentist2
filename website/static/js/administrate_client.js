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