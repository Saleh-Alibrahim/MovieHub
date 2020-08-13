const movieId = document.getElementById('movie-id').value;
document.getElementById('add-movie').addEventListener('click', function (e) {

    console.log('movieId', movieId);
    fetch('/private', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(movieId)
    })
        .then(res => res.json())
        .then(data => {
            console.log(data);
        })
        .catch(err => console.error('Error:', err));
});