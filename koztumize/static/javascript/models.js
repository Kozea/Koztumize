$(function () {
    $('.last_commits select').change(function () {
        $.ajax({
            url: window.Koztumize.history_url.replace('author', $(this).val()),
            dataType: 'html',
            success: function (data) {
                $("#history").html(data);
            }
        });
    }).trigger('change');
});


