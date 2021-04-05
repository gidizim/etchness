
const createJobPosting = (job) => {
    const jobContainer = document.getElementById('job-container')
    if (!jobContainer)
    console.log(job);

    const header = document.createElement('div');
    header.className = 'header-info';
    
    const title = document.createElement('h2');
    title.textContent = job.title;
    header.append(title);
    
    const company = document.createElement('h3');
    company.textContent = job.company;
    header.append(company);
    const location = document.createElement('h4');
    location.textContent = job.location;
    header.append(location);
    
    const jobtype = document.createElement('h4');
    jobtype.textContent = job.job_type;
    header.append(jobtype);
    
    jobContainer.append(header);
    const descripTitle = document.createElement('h2');
    descripTitle.textContent = 'Job Description';
    jobContainer.append(descripTitle);

    const description = document.createElement('h4');
    description.textContent = job.description;
    description.className = 'description';
    jobContainer.append(description);

    const btnContainer = document.createElement('div');
    btnContainer.className = 'btn-container';

    const backBtn = document.createElement('input');
    backBtn.className = 'button';
    backBtn.type = 'button';
    backBtn.value = 'Back to results';
    backBtn.onclick = (event) => {
        event.preventDefault();
        window.location.href = '/results';
    }
    btnContainer.append(backBtn);

    const watchlistBtn = document.createElement('input');
    watchlistBtn.className = 'button';
    watchlistBtn.type = 'button';
    watchlistBtn.value = 'Add to watchlist';
    watchlistBtn.onclick = (event) => {
        event.preventDefault();
        // add to watchlist
        // TODO: actually add to watchlist
        if (watchlistBtn.value == "Add to watchlist") {
            watchlistBtn.value = "Remove from watchlist";
        } else {
            watchlistBtn.value = "Add to watchlist";
        }
    }
    btnContainer.append(watchlistBtn);

    const applyBtn = document.createElement('input');
    applyBtn.className = 'button';
    applyBtn.type = 'button';
    applyBtn.value = 'Apply now';
    applyBtn.onclick = (event) => {
        event.preventDefault();
        window.open = job.url;
    }
    btnContainer.append(applyBtn);
    jobContainer.append(btnContainer);
}