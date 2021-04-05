const searchBtn = document.getElementById('search-btn');
const searchInput = document.getElementById('search-input');
const state = document.getElementById('state');
const suburb = document.getElementById('suburb');
const jobtype = document.getElementById('jobtype');
// const jobResultsContainer = document.getElementById('results-container');
let page = 0;
searchBtn.addEventListener('click', () => {
    // event.preventDefault();
    console.log(state.value);
    console.log(suburb.value);
    console.log(jobtype.value);
    console.log(searchInput.value);
    let location = suburb.value + ', ' + state.value;
    if (suburb.value == 'None' && state.value == 'None') {
        location = 'Australia'
    } else if (suburb.value == 'None') {
        location = state.value
    } else if (state.value == 'None') {
        location = suburb.value
    }
    console.log(location)
    const info = {
        'description': searchInput.value ? searchInput.value : '',
        'job_type': jobtype.value,
        'location': location,
        'page': page,
    }
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
            // location.href= "{{url_for('get_job_results')}}"
            window.location.href = "{{ url_for('get_job_results') }}";
        }
    //     return response.json();
    // }).then((data) => {
    //     console.log(data.result)
    //     for (const job of data.result) {
    //         createJobPost(job.title, job.company, job.created, job.description, job.location, job.url)
    //     }

    }).catch((error) => console.log(error))
})

// const createJobPost = (title, comp, date, description, location, url) => {
//     const job = document.createElement('div');
//     job.className = 'item';
//     job.href = url;

//     const heading = document.createElement('h3');
//     heading.textContent = title;
//     job.append(heading);
    
//     const location = document.createElement('p');
//     location.textContent = location;
//     job.append(location);
    
//     const company = document.createElement('p');
//     company.textContent = comp;
//     job.append(company);
    
//     const descrip = document.createElement('p');
//     descrip.textContent = description.substr(30) + "...";
//     job.append(descrip);
    
//     const created = document.createElement('p');
//     created.textContent = date;
//     job.append(created);

//     jobResultsContainer.append(job);
// }