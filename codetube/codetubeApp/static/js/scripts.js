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

// function toggleSidebar(){
//     var sidebar = document.getElementById("sidebar");
//     if(sidebar.style.display === "none"){
//         sidebar.style.display = "block";
//     }else{
//         sidebar.style.display = "none";
//     }
// }


// if($(window).width() > "768px" )






// $('#myModal').on('shown.bs.modal', function () {
//     $('#video1')[0].play();
// })
// $('#myModal').on('hidden.bs.modal', function () {
//     $('#video1')[0].pause();
// })

