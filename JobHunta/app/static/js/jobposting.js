
const createJobPosting = (event, job, prevPage) => {
    console.log(event.target)
    // do nothing if buttons are clicked
    if (event.target.value == 'Remove from watchlist') return;
    if (event.target.value == 'Add to watchlist') return;

    console.log(job);
    const details = {
        'job': job,
        'prev': prevPage
    }
    fetch('/jobposting', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify(details)
    }).then((response) => {
        console.log(response);
        window.location.href = '/jobposting';
    }).catch((error) => console.log(error))
}


// update db
const addToWatchlist = (job, id) => {
    console.log(id);
    const button = document.getElementById(id);
    if (button.value == "Add to watchlist") {
        fetch('/addToWatchlist', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify({'job': job})
        }).then((response) => {
            console.log(response);
            if (response.status === 200) {
                button.value = "Remove from watchlist";
            }
        }).catch((error) => console.log(error))
        
    } else {
        fetch('/removeFromWatchlist', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify({'url': job['url']})
        }).then((response) => {
            if (response.status === 200) {
                button.value = "Add to watchlist";
            }
            console.log(response);
        }).catch((error) => console.log(error))
    }
}

const removeJob = (job, url) => {
    const watchlistContainer = document.getElementById('watchlist-container');
    // confirm with user
    console.log(url)
    const confirm = window.confirm('Are you sure you want to remove this job from your watchlist?\nThis action is irreversible.')
    if (confirm) {
        fetch('/removeFromWatchlist', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({'url': url})
        }).then((response) => {
            if (response.status === 200) {
                watchlistContainer.removeChild(job);
            }
            console.log(response);
        }).catch((error) => console.log(error))
    }
}
