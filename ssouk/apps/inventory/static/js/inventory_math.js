SSOUK.namespace('SSOUK.inventory_math');

SSOUK.inventory_math = function () {
    
   var calcPrice = function (currency) {        
        var quantity = parseFloat($('#id_quantity').val());
        var price = parseFloat($('#id_price').val());
        var type = $('#id_quantity_type').val();
        
        if (quantity && price && type) {
            var quotient = price / quantity;
            // a bit of dance to round this off properly 
            quotient = Math.round(quotient * 100)/100;
            var new_hint = quotient + ' ' + currency + ' per ' + type
            $('#hint_id_price').html(new_hint);
        }
    } 
    return {
        calcPrice : calcPrice
    }
}();

$(document).ready(function(){
    // event listeners
    var currency = $('#hint_id_price').text();
    $('#id_price').keyup(function () {
        SSOUK.inventory_math.calcPrice(currency);
    });
    $('#id_quantity').keyup(function () {
        SSOUK.inventory_math.calcPrice(currency);
    });
    $('#id_quantity_type').change(function () {
        SSOUK.inventory_math.calcPrice(currency);
    });   
});