const searchBtn = document.getElementById('search-btn');
const searchInput = document.getElementById('search-input');
const timeframe = document.getElementById('timeframe');
const location = document.getElementById('location');

searchBtn.addEventListener('click', () => {

    console.log(timeframe.value);
    console.log(location.value);

    let location = location.value;
    if (location == 'None') {
        location = None;
    } else if (location == 'Local') {
        location = 'NSW';
    } else if (location == 'National') {
        location = 'Australia';
    } else if (location == 'International') {
        location =  None;
    }
    
    let ntime= timeframe.value;
    if (timeframe.value == "") {
        ntime = 0;
    }
    if (ntime == 'day') {
        ntime = 'day';
    } else if (ntime == 'month') {
        ntime = 'month';
    } else if (ntime == 'year') {
        ntime = 'year';
    }

    console.log(location)
    console.log(ntime)

    const info = {
        'description': searchInput.value ? searchInput.value : '',
        'location': location,
        'page': page,
        'ntime': ntime,
    }
    console.log(info)
    fetch('/results', {
        method: 'POST',
        header: {
            'Accept': 'application/json',
            'Content-type': 'application/json'
        },
        body: JSON.stringify(info)

    }).then((response) => {
        console.log(response);
        if (response.status === 200) {
            window.location.href = "/results";
        }
        return response.json();
    }).then((data) => {
        console.log(data.result);
    }).catch((error) => console.log(error))
})