function playVideo(element) {
    element.play();
}

const menu = document.querySelector('#menu');
console.log(menu);
const sidebar = document.querySelector('.sidebar');
console.log(sidebar);

menu.addEventListener('click', function () {
    sidebar.classList.toggle('show-sidebar');
});

function toggleSidebar(){
    var sidebar = document.getElementById("sidebar");
    if(sidebar.style.display === "none"){
        sidebar.style.display = "inline";
    }
    else{
        sidebar.style.display = "none";
    }
}

function copyToClipboard(text) {
    var inputc = document.body.appendChild(document.createElement("input"));
    inputc.value = window.location.href;
    inputc.focus();
    inputc.select();
    document.execCommand('copy');
    inputc.parentNode.removeChild(inputc);
    // alert("URL Copied.");
}