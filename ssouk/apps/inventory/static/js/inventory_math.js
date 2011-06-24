
var quantity, price;



$('#id_price').keyup(function (){
	alert('hey!');			
	quantity = parseInt($('#id_quantity').val());
    price = parseFloat($('#id_price').val());
    if (quantity != 0) {
    	$('#id_price_info').html(price/quantity + ' per item');
    } 
    // else {
    	// // $('#id_price_info').html('You can\'t sell 0 thing ;)');
    // }
});
