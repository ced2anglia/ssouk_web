$(document).ready(function (){
    var quantity,
        price;

    $('#id_quantity').keyup(function (){
        quantity = parseInt($('#id_quantity').val());
    });

    $('#id_price').keyup(function (){
        price = parseInt($('#id_price').val());
        if (quantity && price) {
        	$('#id_price').after(price/quantity + ' per item' + ' yeah!');
        }
    });
});