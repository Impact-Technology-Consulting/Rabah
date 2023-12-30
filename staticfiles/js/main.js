function getCookie(name) {
    var cookieValue = null;

    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');

        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);

            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

function submitForm(form) {
    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST', body: formData, headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken'), // Include CSRF token
        },
    })
        .then(async response => {
            data = await response.json();
            console.log(data)
            if (response.status !== 200) {
                data.errors.forEach(errorMessage => {
                    toastr.error(errorMessage, "Error");
                });
                throw new Error('Network response was not ok');
            }
            return data;
        })
        .then(data => {
            // Handle success response
            toastr.success(data.message, "Success", {"iconClass": 'bg-white text-dark'});
        })
        .catch(error => {
            console.log("error ", error)
            // Handle error
        });
}
