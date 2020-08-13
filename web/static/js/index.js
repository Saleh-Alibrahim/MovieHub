
function deleteButton(id) {

    $.ajax({
        url: `/movie/${id}`,
        type: 'DELETE',
        contentType: 'application/json',
        success: function () {
            window.location.reload(true);
        },
        error: function (request, status, error) {
            alert(request.statusText);
        }
    });
}





