const searchBtn = document.getElementById('search-btn');
const searchInput = document.getElementById('search-input');
const state = document.getElementById('state');
const suburb = document.getElementById('suburb');
const jobtype = document.getElementById('jobtype');
const salary = document.getElementById('salary');
let page = 0;
searchBtn.addEventListener('click', () => {
    let location = suburb.value + ', ' + state.value + ', ' + 'Australia';
    if (suburb.value == 'None' && state.value == 'None') {
        location = 'Australia';
    } else if (suburb.value == 'None') {
        location = state.value + ', ' + 'Australia';
    } else if (state.value == 'None') {
        location = suburb.value + ', ' + 'Australia';
    }
    
    let nSalary = parseInt(salary.value);
    if (salary.value == 'None' || salary.value == "") {
        nSalary = 0;
    }
    const info = {
        'description': searchInput.value ? searchInput.value : '',
        'job_type': jobtype.value,
        'location': location,
        'page': page,
        'salary': nSalary,
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