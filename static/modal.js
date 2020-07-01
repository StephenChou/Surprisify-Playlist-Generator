var open_btn = document.getElementById('options');
var close_btn = document.querySelector('.close');
var submit_btn = document.getElementById('pl_submit');
var pl_name = document.getElementById('playlist-name');
var pl_desc = document.getElementById('playlist-description');
var modal = document.querySelector('.modal');
var levels_btn = document.getElementById('levels-btn');
var generate_btn = document.getElementById('generate-btn');


// Button for opening modal
open_btn.addEventListener('click', ()=> {
    modal.classList.add('modal-active');
});

// Button for closing modal
close_btn.addEventListener('click', ()=> {
    modal.classList.remove('modal-active');
    pl_name.value = "";
    pl_desc.value = "";

});


$(document).ready(function() {

    // Submit custom playlist name and/or description to backend page
    $('#pl_submit').on('click', ()=> {
        event.preventDefault();
        modal.classList.remove('modal-active');
        var name = $('#playlist-name').val();
        var desc = $('#playlist-description').val();

        // Post custom name/desc form data
        req = $.ajax({
            url : '/update',
            method : 'POST',
            data : { name : name, desc : desc}
        });        

    });


    // If user hits generate button, disable enter key to avoid double generation
    $('#generate-btn').on('click', ()=> {
        
        var levels = $('#levels-btn').val();
        
        // Post level data
        if (!levels) {
            event.preventDefault();
        }
            

    });



});

// Prevent posting
pl_name.addEventListener('keypress', function(event) {
        if (event.keyCode == 13) {
            event.preventDefault();
        }
    });

// Prevent posting
pl_desc.addEventListener('keypress', function(event) {
        if (event.keyCode == 13) {
            event.preventDefault();
        }
    });

// Ability to click outside of modal to close
window.onclick = function(event) {
    if (event.target == modal) {
        modal.classList.remove('modal-active');

    }
}