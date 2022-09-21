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








// $('#myModal').on('shown.bs.modal', function () {
//     $('#video1')[0].play();
// })
// $('#myModal').on('hidden.bs.modal', function () {
//     $('#video1')[0].pause();
// })

