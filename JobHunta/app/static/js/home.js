// currently closes but we dont want it to reappear when home is refreshed
const close = document.getElementById('close');
const popup = document.getElementById('popup-box');
close.addEventListener("click", (event) => {
    event.preventDefault();
    popup.style.display = 'none';
});

window.addEventListener("click", (event) => {
    event.preventDefault();
    if (event.target === popup) {
        popup.style.display = 'none';
    }
});
