// currently closes but we dont want it to reappear when home is refreshed
const close = document.getElementById('close');
const popup = document.getElementById('popup-box');
const yes = document.getElementById('yesButton');
const no = document.getElementById('noButton');
close.addEventListener("click", (event) => {
    event.preventDefault();
    popup.style.display = 'none';
});

const updateJob = (jobposting, u_id) => {
    fetch('/applyToJob', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify({'jobposting': jobposting, 'u_id': u_id})

    }).then( (response) =>
    {
        if (response.status === 200) {
            popup.style.display = 'none';
        }

    }).catch( (error) => console.log(error))
};

const updateDateJob = (jobposting, u_id) => {
    fetch('/updateJob', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify({'jobposting': jobposting, 'u_id': u_id})

    }).then( (response) =>
    {
        if (response.status === 200) {
            popup.style.display = 'none';
        }

    }).catch( (error) => console.log(error))
};

