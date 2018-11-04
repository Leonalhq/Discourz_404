$(document).ready(function(){

    let inputs = $('.op');
    for (let i = 2; i < inputs.length; ++i) {
        inputs[i].style.display = "none";
    }

    $('#select').change(selectedOptions2);
});

function selectedOptions2() {
    let selectVal = this.value;
        
    let inputs = $('.op');

    for (let i = 0; i < inputs.length; ++i) {
        if (i < selectVal) {
          inputs[i].style.display = "block";
        }
        else {
            inputs[i].style.display = "none";
        }
    }

}