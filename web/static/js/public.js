if (jwt) {
    const payload = parseJwt(jwt);

    if (payload.permissions[0] == "delete:movies") {
        console.log('hey');
        $('.public-delete').css('display', 'inline-block');
    }


}






