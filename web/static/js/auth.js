let cookie;

if (location.hash) {
    jwtValue = location.hash.substr(1).split('&')[0].substring(13);
    createCookie("jwt", jwtValue, 30);
}
const jwt = getCookie("jwt");

if (jwt) {
    // Hide the login button
    $('#login').css('display', 'none');
    // Show the logout button
    $('#logout').css('display', 'inline-block');
}
function createCookie(name, value, expires) {
    cookie = name + "=" + escape(value) + ";";

    if (expires) {
        // If it's a date
        if (expires instanceof Date) {
            // If it isn't a valid date
            if (isNaN(expires.getTime()))
                expires = new Date();
        }
        else
            expires = new Date(new Date().getTime() + parseInt(expires) * 1000 * 60 * 60 * 24);

        cookie += "expires=" + expires.toGMTString() + ";";
    }

    cookie += "expires=" + expires.toGMTString() + ";";

    document.cookie = cookie;
}
function deleteCookie(name) {
    // If the cookie exists
    if (getCookie(name))
        createCookie(name, "", -1,);
}
function getCookie(name) {
    var regexp = new RegExp("(?:^" + name + "|;\s*" + name + ")=(.*?)(?:;|$)", "g");
    var result = regexp.exec(document.cookie);
    return (result === null) ? null : result[1];
}
// Sync the add button
$('#logout').on('click', function (e) {
    deleteCookie('jwt');
});


