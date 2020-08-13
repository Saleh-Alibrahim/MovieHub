const movieId = document.getElementById('movie-id').value;

$('#private-button').click(function (e) {

    if (!jwt) {
        alert('Sorry you need to register before adding to your private hub');
        return;
    }
    fetch('/private', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(movieId)
    })
        .then(res => res.json())
        .then(res => {
            alert(res.msg);
        })
        .catch(err => alert(err.message));
});

$('#public-button').click(function (e) {

    if (!jwt) {
        alert('Sorry you need to register before adding to your private hub');
        return;
    }

    fetch('/public', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(movieId)
    })
        .then(res => res.json())
        .then(res => {
            alert(res.msg);
        })
        .catch(err => alert(err.message));
});