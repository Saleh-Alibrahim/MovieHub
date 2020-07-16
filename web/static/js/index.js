if (location.hash) {
    jwtValue = location.hash.substr(1).split('&')[0].substring(13);
    localStorage.setItem('jwt', `Bearer ${jwtValue}`);
}
const jwt = localStorage.getItem('jwt');
if (jwt) {
    // Show the add button
    $('#addMovie').css('visibility', 'visible');

    // Hide the login button
    $('#login').css('display', 'none');

    // Show the logout button
    $('#logout').css('display', 'inline-block');

    // Sync the add button
    $('#addMovie').on('click', function () {
        $.ajax({
            url: "/add-movie",
            type: 'GET',
            contentType: 'application/json',
            headers: {
                "Authorization": `Bearer ${jwt}`
            },
            async: false
        });
    });


}
// Sync the add button
$('#logout').on('click', function (e) {
    localStorage.removeItem('jwt');
});


