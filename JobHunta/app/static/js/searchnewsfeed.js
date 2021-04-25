const searchBtn = document.getElementById('search-btn');
const searchInput = document.getElementById('search-input');
const timeframe = document.getElementById('timeframe');
const categoryfilter = document.getElementById('category');
const locationfilter = document.getElementById('location');

searchBtn.addEventListener('click', () => {

    let ntime= timeframe.value;
    console.log(timeframe.value)
    if (timeframe.value == "") {
        ntime = 1;
    }

    let location = locationfilter.value;
    if (location == 'None') {
        location = 'None';
    }

    let category = categoryfilter.value;
    if (category == 'None') {
        category = 'None';
    }

    const info = {
        'description': searchInput.value ? searchInput.value : '',
        'ntime': ntime,
        'category': category,
        'location': location,
    }

    console.log(info)
    fetch('/newsfeed', {
        method: 'POST',
        header: {
            'Accept': 'application/json',
            'Content-type': 'application/json'
        },
        body: JSON.stringify(info)

    }).then((response) => {
        console.log(response);
        if (response.status === 200) {
            window.location.href = "/newsfeed";
        }
        return response.json();
    }).then((data) => {
        console.log(data.result);
    }).catch((error) => console.log(error))
})
