
const createJobPosting = (event, job, prevPage) => {
    console.log(event.target)
    if (event.target.value == 'Remove from Watchlist') return;
    console.log(job);
    const details = {
        'job': job,
        'prev': prevPage
    }
    fetch('/jobposting', {
        method: 'POST',
        body: JSON.stringify(details)
    }).then((response) => {
        console.log(response);
        window.location.href = '/jobposting';
    }).catch((error) => console.log(error))
}


// update db
const addToWatchlist = (job) => {
    console.log(job)
    // console.log(title)
    // console.log(location)
    // console.log(company)
    // console.log(jobtype)
    // console.log(created)
    // console.log(url)
    const button = document.getElementById('add');
    if (button.value == "Add to watchlist") {
        button.value = "Remove from watchlist";
        // const postDetails = {
        //     'title': title,
        //     'company': company,
        //     'location': location,
        //     'jobtype': jobtype,
        //     'created': created,
        //     'description': description,
        //     'url': url            
        // }
        fetch('/addToWatchList', {
            method: 'POST',
            body: JSON.stringify(job)
        }).then((response) => {
            console.log(response);
        }).catch((error) => console.log(error))
        
    } else {
        button.value = "Add to watchlist";
        fetch('/removeFromWatchList', {
            method: 'POST',
            body: JSON.stringify({'url': job['url']})
        }).then((response) => {
            console.log(response);
        }).catch((error) => console.log(error))
    }
}

const removeJob = (job, url) => {
    const watchlistContainer = document.getElementById('recommendation');
    // confirm with user
    const confirm = window.confirm('Are you sure you want to remove this job from your watchlist?\nThis action is irreversible.')
    if (confirm) {
        fetch('/removeFromWatchList', {
            method: 'POST',
            body: JSON.stringify({'url': url})
        }).then((response) => {
            console.log(response);
        }).catch((error) => console.log(error))
        watchlistContainer.removeChild(job);
    }
}
// go back to home or results page
const clickBack = () => {
    location.href='/results'
}