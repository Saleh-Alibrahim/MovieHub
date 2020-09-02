const movieId = document.getElementById('movie-id').value;

$('#private-button').click(function (e) {

    if (!jwt) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Sorry you need to register before adding to your private hub',
            confirmButtonColor: '#f1b722',
            background: '#0c2738',
        });
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
            if (res.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Great .',
                    text: res.msg,
                    confirmButtonColor: '#f1b722',
                    background: '#0c2738',
                });
            }
            else {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: res.msg,
                    confirmButtonColor: '#f1b722',
                    background: '#0c2738',
                });
            }
        })
        .catch(err => {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: err.message,
                confirmButtonColor: '#f1b722',
                background: '#0c2738',
            });
        });
});

$('#public-button').click(function (e) {

    if (!jwt) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Sorry you need to register before adding to your private hub',
            confirmButtonColor: '#f1b722',
            background: '#0c2738',
        });
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
            if (res.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Great .',
                    text: res.msg,
                    confirmButtonColor: '#f1b722',
                    background: '#0c2738',
                });
            }
            else {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: res.msg,
                    confirmButtonColor: '#f1b722',
                    background: '#0c2738',
                });
            }
        })
        .catch(err => {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: err.message,
                confirmButtonColor: '#f1b722',
                background: '#0c2738',
            });
        });
});