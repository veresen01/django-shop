let url_ajax_cart_add_product,
    url_ajax_cart_update,
    url_ajax_update_product_amount,
    url_ajax_remove_product;

let csrf_token;

let Cart_amount_dom;
let Cart_price_dom;

let toasterOptions = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": true,
    "progressBar": true,
    "positionClass": "toast-top-right",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}

$(document).ready(function () {
    url_ajax_cart_add_product = JSON.parse(document.getElementById('url_ajax_cart_add_product').textContent);
    url_ajax_cart_update = JSON.parse(document.getElementById('url_ajax_cart_update').textContent);
    url_ajax_update_product_amount = JSON.parse(document.getElementById('url_ajax_update_product_amount').textContent);
    url_ajax_remove_product = JSON.parse(document.getElementById('url_ajax_remove_product').textContent);

    csrf_token = $('input[name="csrfmiddlewaretoken"]:first').val()

    Cart_amount_dom = $('.CartBlock-amount')
    Cart_price_dom = $('.CartBlock-price, .Cart-price-total')
});

/**
 * Единичное добавление продукта в корзину (из каталога)
 * @param product_id
 * @returns {boolean}
 */
function add_product_in_cart(product_id) {
    let product_amount = 1
    let Amount_dom = $('#Product-amount')
    if (Amount_dom.length > 0)
    {
        product_amount = Amount_dom.val()
    }

    let data = {
        csrfmiddlewaretoken: csrf_token,
        product_id,
        product_amount
    }
    $.ajax({
        data: data,
        method: 'POST',
        url: url_ajax_cart_add_product,
        dataType: 'json',
        success: function (json) {
            if (json.result) {
                toastr.options = toasterOptions;
                toastr.success(json.msg);
                update_cart_view()
            } else {
                toastr.options = toasterOptions
                toastr.error(json.msg)
            }
        },
        error: function (response) {
            console.log(response)
            toastr.options = toasterOptions
            toastr.error(response)
        }
    });
    return false;
}

/**
 * Обновление корзины в шапке
 * @returns {boolean}
 */
function update_cart_view() {
    let data = {
        csrfmiddlewaretoken: csrf_token
    }
    $.ajax({
        data: data,
        method: 'POST',
        url: url_ajax_cart_update,
        dataType: 'json',
        success: function (json) {
            if (json.result) {
                Cart_amount_dom.html(json.total_items)
                let cart_amount = number_format(json.total_price, 2, ',', '`')
                Cart_price_dom.html(cart_amount + '$')
            } else {
                toastr.options = toasterOptions
                toastr.error(json.msg)
            }
        },
        error: function (response) {
            console.log(response)
            toastr.options = toasterOptions
            toastr.error(response)
        }
    });
    return false;
}

/**
 * Обновление количества товара в корзине
 * @param product_id
 * @param product_amount
 * @param product_update_amount
 * @returns {boolean}
 */
function change_product_amount(product_id, product_amount, product_update_amount) {
    let data = {
        csrfmiddlewaretoken: csrf_token,
        product_id,
        product_amount,
        product_update_amount
    }
    $.ajax({
        data: data,
        method: 'POST',
        url: url_ajax_update_product_amount,
        dataType: 'json',
        success: function (json) {
            if (json.result) {
                let cart_product_total_price = number_format(json.new_total_price, 2, ',', '`')
                $('#product_' + product_id + '_price_total_item').html(cart_product_total_price + '$')
                update_cart_view()
                toastr.options = toasterOptions
                toastr.success(json.msg)
                if ( json.granted_amount )
                {
                    $('#product_'+product_id+'_items').val(json.granted_amount)
                }
            } else {
                // toastr.options = toasterOptions
                // toastr.error(json.msg)
            }
        },
        error: function (response) {
            console.log(response)
            toastr.options = toasterOptions
            toastr.error(response)
        }
    });
    return false;
}

/**
 * Удаления продукта из корзины
 * @param product_id
 */
function remove_product(product_id) {
    if (confirm('Вы действительно желаете удалить данный продукт из корзины?')) {
        let data = {
            csrfmiddlewaretoken: csrf_token,
            product_id
        }
        $.ajax({
            data: data,
            method: 'POST',
            url: url_ajax_remove_product,
            dataType: 'json',
            success: function (json) {
                if (json.result) {
                    if ( json.cart_amount > 0 )
                    {
                        toastr.options = toasterOptions;
                        toastr.success(json.msg);
                        update_cart_view()
                        $('#product_' + product_id).hide(1000)
                    } else window.location.reload()

                } else {
                    toastr.options = toasterOptions
                    toastr.error(json.msg)
                }
            },
            error: function (response) {
                console.log(response)
                toastr.options = toasterOptions
                toastr.error(response)
            }
        });
        return false;
    }
}