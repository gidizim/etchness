
const createJobPosting = (job) => {
    console.log(job);
    // const postDetails = {
    //     'title': job.title,
    //     'company': job.company,
    //     'location': job.location,
    //     'job_type': job.job_type,
    //     'created': job.created,
    //     'description': job.description,
    //     'url': job.url            
    // }

    fetch('/jobposting', {
        method: 'POST',
        body: JSON.stringify(job)
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