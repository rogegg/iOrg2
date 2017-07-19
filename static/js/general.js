/**
 * Created by roge on 21/06/17.
 */
var LOCK = false

$(document).ready(function(){

    iniMaterializeJs();
    
    bindEvents();
});

/**
 * Initialize MaterializCss
 */
function iniMaterializeJs(){
    //Ini modal-popup.
    $('.modal').modal();

    //Ini sideNav
    $('.button-collapse').sideNav();

    //Fixed inputs materializecss
    fixedInputsMaterializecss();
}


/**
 * Bind general events
 */
function bindEvents() {
    $('.settings-button-container a').click(function(event){
        $(event.currentTarget).parent().find('.button-description').addClass("active");
    })
}

/**
 * Fix the inputs inside a label of django.
 * put inputs outside the label.
 */
function fixedInputsMaterializecss(){
    var $myRadioButton = $('input.iorg-input');
    var $form = $myRadioButton.closest('form');
    for ( var i=0 ; i<$myRadioButton.length ; i++){
        console.log($($myRadioButton[i]).parent().parent());
        $($myRadioButton[i]).parent().parent().prepend($myRadioButton[i]);

    }
}



