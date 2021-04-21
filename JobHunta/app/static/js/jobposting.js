
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
const addToWatchlist = (job, id, loggedIn) => {
    console.log(loggedIn);
    if (!loggedIn) {
        window.location.href = "/login";
        return;
    }

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
let jobProgress;
// 2 Buttons, one increments job counter, one resets
const incrementJob = (jobposting, u_id) => {
    console.log(jobProgress);
    if (!jobProgress) {
        jobProgress = {
            applied: jobposting.num_applied, 
            responded: jobposting.num_responded, 
            interviewed: jobposting.num_interviewed, 
            finalised: jobposting.num_finalised
        }
    }
    const button = document.getElementById('application');
    // live update the numbers
    const applied = document.getElementById('applied');
    const resp = document.getElementById('responded');
    const interview = document.getElementById('interviewed');
    const finalised = document.getElementById('finalised');
    // Send Post request, on success update button.value
    
    fetch('/applyToJob', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify({'jobposting': jobposting, 'u_id': u_id})
        
    }).then( (response) =>
    {
        if (response.status === 200) {

            if (button.value == "I've applied")
            {
                button.value = "I've received a response";
                jobProgress['applied'] += 1;
                console.log(jobProgress.applied)
                console.log(jobProgress['applied'])
                applied.textContent = `${jobProgress['applied']} people have applied.`;
            }
            else if (button.value == "I've received a response")
            {
                button.value = "I've received an interview";
                jobProgress['responded'] += 1;
                resp.textContent = `${jobProgress['responded']} people have received a response.`;
            }
            else if (button.value == "I've received an interview")
            {
                button.value = "I've finalised the offer";
                jobProgress['interviewed'] += 1;
                interview.textContent = `${jobProgress['interviewed']} people have received an interview.`;
            }
            else if (button.value == "I've finalised the offer")
            {
                button.value = "Thanks for the response!"
                jobProgress['finalised'] += 1;
                finalised.textContent = `${jobProgress['finalised']} people have finalised their offer.`;
            }
        }
        
    }).catch( (error) => console.log(error))
}

const unmarkJob = (jobposting, u_id) => {
    const button = document.getElementById('application');
    // live update the numbers
    const applied = document.getElementById('applied');
    const resp = document.getElementById('responded');
    const interview = document.getElementById('interviewed');
    const finalised = document.getElementById('finalised');
    // Send Post request, on success update button.value
    console.log(jobProgress);
    if (!jobProgress) {
        jobProgress = {
            applied: jobposting.num_applied, 
            responded: jobposting.num_responded, 
            interviewed: jobposting.num_interviewed, 
            finalised: jobposting.num_finalised
        }
    }
    fetch('/removeFromJob', {
        method: 'DELETE',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify({'jobposting': jobposting, 'u_id': u_id})

    }).then( (response) =>
    {
        if (response.status === 200) {
            console.log(button.value)
            if (button.value == "I've received a response")
            {
                jobProgress['applied'] -= 1;
                applied.textContent = `${jobProgress['applied']} people have applied.`;
            }
            else if (button.value == "I've received an interview")
            {
                jobProgress['applied'] -= 1;
                jobProgress['responded'] -= 1;
                applied.textContent = `${jobProgress['applied']} people have applied.`;
                resp.textContent = `${jobProgress['responded']} people have received a response.`;
            }
            else if (button.value == "I've finalised the offer")
            {
                jobProgress['applied'] -= 1;
                jobProgress['interviewed'] -= 1;
                jobProgress['responded'] -= 1;
                applied.textContent = `${jobProgress['applied']} people have applied.`;
                resp.textContent = `${jobProgress['responded']} people have received a response.`;
                interview.textContent = `${jobProgress['interviewed']} people have received an interview.`;
            }
            else if (button.value == "Thanks for the response!")
            {
                jobProgress['applied'] -= 1;
                jobProgress['finalised'] -= 1;
                jobProgress['interviewed'] -= 1;
                jobProgress['responded'] -= 1;
                applied.textContent = `${jobProgress['applied']} people have applied.`;
                resp.textContent = `${jobProgress['responded']} people have received a response.`;
                interview.textContent = `${jobProgress['interviewed']} people have received an interview.`;
                finalised.textContent = `${jobProgress['finalised']} people have finalised their offer.`;
            }
            button.value = "I've applied";
        }
    }).catch( (error) => console.log(error));
}
