

if (jwt) {
    $('.delete-button').css('display', 'block');
}

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

const url = window.location.origin;
// document.getElementById('private-nav').href = `https://moviehub.eu.auth0.com/authorize?response_type=token&audience=moviehub&client_id=DMqcGxMMzfF2MKkrlt2F360RSi2D1PK9&redirect_uri=
// ${url}/private`;
document.getElementById('login').href = `https://moviehub.eu.auth0.com/authorize?response_type=token&audience=moviehub&client_id=DMqcGxMMzfF2MKkrlt2F360RSi2D1PK9&redirect_uri=
${url}`;
document.getElementById('logout').href = `https://moviehub.eu.auth0.com/v2/logout?returnTo=${url}&client_id=DMqcGxMMzfF2MKkrlt2F360RSi2D1PK9`;



