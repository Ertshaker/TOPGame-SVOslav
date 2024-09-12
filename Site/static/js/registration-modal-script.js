var modal = document.getElementById("errorModal");
var span = document.getElementsByClassName("close")[0];
document.addEventListener("DOMContentLoaded", function () {
    var hasMessages = document.querySelectorAll("#modalMessages .message").length > 0;
    if (hasMessages) {
        modal.style.display = "block";
    }
});

span.onclick = function () {
    modal.style.display = "none";
};

window.onclick = function (event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
};