let jwt = localStorage.getItem('jwt');
if (!jwt && location.hash) {
    jwt = location.hash.substr(1).split('&')[0].substring(13);
    localStorage.setItem('jwt', `Bearer ${jwt}`);
}
