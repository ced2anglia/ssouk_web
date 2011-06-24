$(document).ready(function (){
    var quantity,
        price;
	alert('hey!');
    $('#id_quantity').keyup(function (){
        quantity = parseInt($('#id_quantity').val());
    });

    $('#id_price').keyup(function (){
        price = parseFloat($('#id_price').val());
        if (quantity && price) {
            $('#id_price_info').html(price/quantity + ' per item');
        }
    });
});