if (jwt) {
    const payload = parseJwt(jwt);
    console.log(payload.permissions)
    if (payload.permissions.includes("delete:public")) {
        $('.public-delete').css('display', 'inline-block');
    }
    if (payload.permissions.includes("post:public")) {
        $('#public-button').css('display', 'inline-block');
    }
}






