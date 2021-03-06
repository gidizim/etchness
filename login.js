const login = () => {
    const formDetails = document.querySelectorAll('[required]');
    for (let i = 0; i < formDetails.length; i++) {
        if (formDetails[i].value == "") {
            alert("Please fill in all the fields");
            return;
        };
    }
    
    location.href = "home.html";

}

const edit = () => {
    const profileFeatures = document.getElementsByName('profile');
    if (document.getElementById('edit-btn').value == "Save changes") {
        document.getElementById('edit-btn').value = "Edit profile";
    } else {
        document.getElementById('edit-btn').value = "Save changes";
    }
    for (let i = 0; i < profileFeatures.length; i++) {
        profileFeatures[i].disabled = !profileFeatures[i].disabled;
    }
}