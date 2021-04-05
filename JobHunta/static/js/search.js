const searchBtn = document.getElementById('search-btn');
const searchInput = document.getElementById('search-input');
const state = document.getElementById('state');
const suburb = document.getElementById('suburb');
const jobtype = document.getElementById('jobtype');

let page = 0;
searchBtn.addEventListener('click', () => {
    // event.preventDefault();
    // return the client ip address and user agent
    console.log('here');
    console.log(state.value);
    console.log(suburb.value);
    console.log(jobtype.value);
    console.log(searchInput.value);
    let location = suburb.value + ", " + state.value;
    if (!suburb.value && !state.value) {
        location = 'Australia';
    } else if (!suburb.value) {
        location = state.value;
    } else if (!state.value) {
        location = suburb.value;
    }

    const info = {
        'description': searchInput.value ? searchInput.value : '',
        'job_type': jobtype.value,
        'location': suburb.value + ", " + state.value,
        'page': page,
    }
    fetch('/search', {
        method: 'POST',
        header: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify(info)
    }).then((response) => {
        console.log(response)
        return response.json();
    }).then((data) => {
        console.log(data.result)
    }).catch((error) => console.log(error))
})
