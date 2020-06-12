var open_btn = document.getElementById('options');
var close_btn = document.querySelector('.close');
var modal = document.querySelector('.modal');


open_btn.addEventListener('click', ()=> {
    modal.classList.add('modal-active');
});

close_btn.addEventListener('click', ()=> {
    modal.classList.remove('modal-active');
});

window.onclick = function(event) {
    if (event.target == modal) {
        modal.classList.remove('modal-active');
    }
}