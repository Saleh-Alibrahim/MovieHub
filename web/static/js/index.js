// const x = document.getElementById("toast");
// x.classList.add("show");
// x.innerHTML = "تم النسخ";
// setTimeout(function () {
//     x.classList.remove("show");
// }, 3000);



if (jwt) {
    $('.delete-button').css('display', 'block');
}

function deleteButton(id) {
    $.ajax({
        url: `http://127.0.0.1:5000/movie/${id}`,
        type: 'DELETE',
        contentType: 'application/json',
        success: function (result) {
            alert(result)
            location.href = location.href;
        }
    });
}



