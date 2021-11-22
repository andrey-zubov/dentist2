$(document).ready(function () {
    $('.change_client').click(function (f) {
        let form = $(this).parent().parent();
        let cells = form.find('input');
        let client_id = $(this).attr('id').split('_')[1]
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

    $('.delete_client').click(function (f) {
        if (confirm('Вы действительно хотите удалить клиента?')) {
            let client_id = $(this).attr('id').split('_')[1]
            let csrf = $('input[name="csrfmiddlewaretoken"]').val();
            $('#table_' + client_id).hide()

            $.ajax({
                'type': 'post',
                'data': {
                    'client_id': client_id,
                    'csrfmiddlewaretoken': csrf,
                },
                'url': '/ajax_delete_client',
                success: function (suc) {
                    console.log('suc');
                },
                error: function (err) {
                    console.log(err);
                },
            });
        };
    });

    $('.change_doctor').click(function (f) {
        let form = $(this).parent().parent();
        let cells = form.find('input');
        let doctor_id = $(this).attr('id').split('_')[1]
        cells.each(function () {
            $(this).attr('readonly', false);
        });
        $('.change_doctor').toggle();
        $('.delete_doctor').toggle();
        $('#save_'+doctor_id).toggle();
        $('#cancel_'+doctor_id).toggle();
    });

    $('.doctor_administration').submit(function (f) {
        f.preventDefault();
        let form_data = $(this).serializeArray();
        $.ajax({
            'type': 'post',
            'data': form_data,
            'url': '/ajax_save_doctor',
            success: function (suc) {
              console.log('suc');
              },
              error: function (err) {
                  console.log(err);
              },
        });

        let doctor_id = $(this).attr('id').split('_')[1]
        $('.change_doctor').toggle();
        $('.delete_doctor').toggle();
        $('#save_'+doctor_id).toggle();
        $('#cancel_'+doctor_id).toggle();

    });

    $('.cancel_doctor').click(function (f) {
        let doctor_id = $(this).attr('id').split('_')[1]
        $('.change_doctor').toggle();
        $('.delete_doctor').toggle();
        $('#save_'+doctor_id).toggle();
        $('#cancel_'+doctor_id).toggle();
    });

    $('.delete_doctor').click(function (f) {
        if (confirm('Вы действительно хотите удалить врача?')) {
            let doctor_id = $(this).attr('id').split('_')[1]
            let csrf = $('input[name="csrfmiddlewaretoken"]').val();
            $('#table_' + doctor_id).hide()

            $.ajax({
                'type': 'post',
                'data': {
                    'client_id': doctor_id,
                    'csrfmiddlewaretoken': csrf,
                },
                'url': '/ajax_delete_doctor',
                success: function (suc) {
                    console.log('suc');
                },
                error: function (err) {
                    console.log(err);
                },
            });
        };
    });
  });