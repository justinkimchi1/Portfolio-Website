// function toggleTheme() {
//     document.body.classList.toggle("dark-mode");
// }
function checkLogin(button) {
    let url = button.getAttribute("data-url");

    // Replace this with your actual login check logic
    let isLoggedIn = true; // Set to false if the user is not logged in

    if (isLoggedIn) {
        window.location.href = url;
    } else {
        window.location.href = "/login"; // Redirect to login page if not logged in
    }
}


function openModal() {
    document.getElementById("contactModal").style.display = "flex";
}

function closeModal() {
    document.getElementById("contactModal").style.display = "none";
}

// Close modal if user clicks outside it
window.onclick = function(event) {
    let modal = document.getElementById("contactModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
};
