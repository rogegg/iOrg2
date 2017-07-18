/**
 * Created by roge on 21/06/17.
 */


$(document).ready(function(){

    iniMaterializeJs();
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