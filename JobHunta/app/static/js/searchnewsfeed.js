const searchBtn = document.getElementById('search-btn');
const searchInput = document.getElementById('search-input');
const timeframe = document.getElementById('timeframe');
const locationfilter = document.getElementById('location');

searchBtn.addEventListener('click', () => {

    let location = locationfilter.value;
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
        'ntime': ntime,
    }
    console.log(info)
    fetch('/newsresults', {
        method: 'POST',
        header: {
            'Accept': 'application/json',
            'Content-type': 'application/json'
        },
        body: JSON.stringify(info)

    }).then((response) => {
        console.log(response);
        if (response.status === 200) {
            window.location.href = "/newsresults";
        }
        return response.json();
    }).then((data) => {
        console.log(data.result);
    }).catch((error) => console.log(error))
})