let order_delivery_limit = JSON.parse(document.getElementById('order_delivery_limit').textContent);
let order_delivery_price = JSON.parse(document.getElementById('order_delivery_price').textContent);
let order_delivery_express = JSON.parse(document.getElementById('order_delivery_express').textContent);
let url_ajax_create_order = JSON.parse(document.getElementById('url_ajax_create_order').textContent);
let url_ajax_cancel_order = JSON.parse(document.getElementById('url_ajax_cancel_order').textContent);
let TOTAL_DATA;
'use strict';
(function ($) {

    var px = ''; //'rt--'

    /**
     * Функция для вывода набора jQuery по селектору, к селектору добавляются
     * префиксы
     *
     * @param {string} selector Принимает селектор для формирования набора
     * @return {jQuery} Возвращает новый jQuery набор по выбранным селекторам
     */
    function $x(selector) {
        return $(x(selector));
    }

    /**
     * Функция для автоматического добавления префиксов к селекторы
     *
     * @param {string} selector Принимает селектор для формирования набора
     * @return {string} Возвращает новый jQuery набор по выбранным селекторам
     */
    function x(selector) {
        var arraySelectors = selector.split('.'),
            firstNotClass = !!arraySelectors[0];

        selector = '';

        for (var i = 0; i < arraySelectors.length; i++) {
            if (!i) {
                if (firstNotClass) selector += arraySelectors[i];
                continue;
            }
            selector += '.' + px + arraySelectors[i];
        }

        return selector;
    }

// Прелоадер
    $(function () {

        // MY LOAD
        console.log('MY LOAD')


        initMasks()

        initCheckCityAddress()

        var menu = function () {
            var $menuMain = $('.menu_main');
            $menuMain.css('position', 'absolute');
            var menuHeight = $('.menu_main').outerHeight();
            $menuMain.css('position', 'static');
            var $body = $('body');

            function refresh() {
                if (window.innerWidth < 991) {
                    // $('.menuModal').each(function(){
                    //     var $this = $(this);
                    //     setTimeout(function(){
                    //         if ($this.attr('height') > 0) {
                    //             $this.css('height', 0);
                    //         }
                    //     }, 100);
                    // });
                    $('.menuModal').css('height', 0);
                    $menuMain.css('position', 'absolute');
                    menuHeight = $('.menu_main').outerHeight();
                    $menuMain.css('position', 'static');
                } else {
                    menuHeight = $('.menu_main').outerHeight();
                    $('.menuModal')
                        .removeClass("menuModal_OPEN")
                        .css('height', '');
                    $body.removeClass("Site_menuOPEN");
                    $('.menuTrigger').removeClass("menuTrigger_OPEN");
                }
            }

            return {
                init: function () {
                    if (window.innerWidth < 991) {
                        $(".menuModal").css('height', menuHeight);
                        // Меню для мобильных
                        $(".menuTrigger").each(function () {
                            $($(this).attr('href')).css('height', 0);
                        });
                    }

                    $(".menuTrigger").click(function (e) {
                        var $this = $(this),
                            href = $this.attr("href");

                        if ($this.hasClass("menuTrigger_OPEN")) {
                            $body.removeClass("Site_menuOPEN");
                            $(href)
                                .removeClass("menuModal_OPEN")
                                .css('height', 0);
                            $this.removeClass("menuTrigger_OPEN");
                        } else {
                            $body.addClass("Site_menuOPEN");
                            $(href)
                                .addClass("menuModal_OPEN")
                                .css('height', menuHeight);
                            $this.addClass("menuTrigger_OPEN");
                        }
                        e.preventDefault();
                    });
                    $(window).on('resize', refresh);
                }
            };
        };
        menu().init();
        var search = function () {
            var $searchLink = $('.Header-searchLink');
            return {
                init: function () {
                    $searchLink.each(function () {
                        var $this = $(this);
                        $this.on('click', function () {
                            var $thisClick = $(this);
                            $thisClick.next('.Header-search').toggleClass('Header-search_open');
                        });
                    });
                }
            };
        };
        search().init();
        var form = function () {
            var $selectList = $('.selectList');
            var $input = $('.form-input, .form-textarea');
            var $form = $('.form');
            var $select = $('.form-select');
            return {
                init: function () {
                    $selectList.each(function () {
                        var $this = $(this),
                            $radio = $this.find('input[type="radio"]');

                        function changeTitle($block, $element) {
                            $block.find('.selectList-title')
                                .text($element.closest('.selectList-item')
                                    .find('.selectList-text').text())
                        }

                        changeTitle($this, $radio.filter('[checked="checked"]'));
                        $radio.on('change', function () {
                            changeTitle($this, $(this));
                        });

                    });
                    $(document).on('click', function (e) {
                        var $this = $(e.target);
                        if (!$this.hasClass('selectList-header')) {
                            $this = $(e.target).closest('.selectList-header');
                        }
                        if ($this.length) {
                            e.preventDefault();
                            $this.closest('.selectList').toggleClass('selectList_OPEN');
                        } else {
                            $('.selectList').removeClass('selectList_OPEN');
                        }
                    });

                    // Валидация полей
                    $input.on('blur', function () {
                        let $this = $(this);
                        let validate = $this.data('validate')
                        let message = '';
                        let error = false;
                        let prevValue = $this.val()
                        if (validate !== undefined) {
                            validate = validate.split(' ');
                            validate.forEach(function (v) {
                                // console.log(v)
                                let val = $this.val().replace(' ', '');
                                val = val + '';
                                // console.log('$this.val()')
                                // console.log($this.val())
                                // console.log('val')
                                // console.log(val)
                                switch (v) {
                                    case 'require':
                                        if (!$this.val()) {
                                            // message = 'Это поле обязательно для заполнения. ';
                                            error = true;
                                            toastr.options = toasterOptions
                                            toastr.error('Это поле обязательно для заполнения. ')
                                            $this.val(prevValue)
                                            // $this.focus()
                                        }
                                        break;
                                    case 'pay':
                                        if (parseFloat(val) % 2 !== 0) {
                                            // message += 'Номер должен быть четным. ';
                                            error = true;
                                            toastr.options = toasterOptions
                                            toastr.error('Номер должен быть четным.')
                                            $this.val(prevValue)
                                            // $this.focus()
                                        }
                                        break;
                                    case 'number':
                                        if (!isNaN(parseFloat(val)) && isFinite(val)) {

                                        } else {
                                            // message += 'Значение должно быть числом';
                                            error = true;

                                            toastr.options = toasterOptions
                                            toastr.error('Значение должно быть числом!')
                                            // $this.val(prevValue)
                                            // $this.focus()
                                            $this.val('')
                                            // $this.focus()
                                        }
                                        break;

                                }
                                if (error) {
                                    if ($this.hasClass('form-input')) {
                                        $this.addClass('form-input_error');
                                    }
                                    if ($this.hasClass('form-textarea')) {
                                        $this.addClass('form-textarea_error');
                                    }
                                    if (!$this.next('.form-error').length) {
                                        $this.after('<div class="form-error">' + message + '</div>');
                                    }
                                    $this.data('errorinput', true);

                                    $('#button_order_payment').prop('disabled', true)

                                } else {
                                    $this.next('.form-error').remove();
                                    $this.removeClass('form-input_error');
                                    $this.removeClass('form-textarea_error');
                                    $this.data('errorinput', false);

                                    $('#button_order_payment').prop('disabled', false)
                                }
                                message = '';

                            });
                        }

                    });
                    $form.on('submit', function (e) {
                        var $this = $(this),
                            $validate = $this.find('[data-validate]');

                        $validate.each(function () {
                            var $this = $(this);
                            $this.trigger('blur');
                            if ($this.data('errorinput')) {
                                e.preventDefault();
                            }
                        });
                    });
                    $select.wrap('<div class="form-selectWrap"></div>');
                    $('[data-mask]').each(function () {
                        var $this = $(this);
                        $this.mask($this.data('mask'), {placeholder: 'x'});
                    });
                }
            };
        };
        form().init();
        let modal = function () {
            let $trigger = $('.trigger'),
                $body = $('body'),
                $modal = $('.modal');

            let template = {
                img: (img) => '<div class="modal">' +
                    '<div class="modal-window">' +
                    '<a href="#" class="modal-close fa fa-close"></a>' +
                    '<img src="' + img + '" />' +
                    '</div>' +
                    '</div>'
            };

            return {
                refresh: function () {
                },
                init: function () {
                    function modalClick(e) {

                        let $target = $(e.target),
                            $this = $(this);

                        if ($target.hasClass('modal-close')) {
                            $target = $this;
                        }

                        if ($this.is($target)) {
                            e.preventDefault();
                            $body.removeClass("Site_modalOPEN");
                            $this.removeClass("modal_OPEN");
                            $('[href="' + $this.attr('id') + '"]').removeClass("trigger_OPEN");
                        }
                    }

                    $trigger.click(function (e) {
                        e.preventDefault();

                        let $this = $(this),
                            href = $this.attr("href"),
                            $href = $(href);

                        if (!$(href).length) {
                            let $img = $(template.img($this.data('src')));
                            $img.attr('id', href.replace('#', ''));
                            $body.append($img);
                            $href = $(href);
                            $modal = $modal.add($href);
                            $href.click(modalClick);
                        }

                        $href.addClass("modal_OPEN");
                        $body.addClass("Site_modalOPEN");
                        $this.addClass("trigger_OPEN");
                    });

                    $modal.click(modalClick);

                }
            };
        };

        modal().init();
        var range = function () {
            return {
                init: function () {
                    var $range = $('.range'),
                        $line = $range.find('.range-line');

                    $line.ionRangeSlider({
                        onStart: function (data) {
                            $('.rangePrice').text(
                                '$' + data.from + ' - $' + data.to
                            )
                        },
                        onChange: function (data) {
                            $('.rangePrice').text(
                                '$' + data.from + ' - $' + data.to
                            )
                        }
                    });
                }
            };
        };
        range().init();
        var table = function () {
            return {
                init: function () {
                }
            };
        };
        table().init();
//END
        var PanelAdd = function () {
            return {
                init: function () {
                }
            };
        };
        PanelAdd().init();
        var ControlPanel = function () {
            return {
                init: function () {
                }
            };
        };
        ControlPanel().init();
        var Slider = function () {
            let $block = $('.Slider').not('.Slider_carousel'),
                $container = $block.children('.Slider-box'),
                $carousel = $('.Slider_carousel'),
                $containerCar = $carousel.children('.Slider-box');
            return {
                init: function () {
                    $container.each(function () {
                        var $this = $(this);
                        var $navigate = $this.closest($block).find('.Slider-navigate');
                        $this.slick({
                            dots: true,
                            arrows: true,
                            autoplay: true,
                            appendArrows: $navigate,
                            appendDots: $navigate,
                            autoplaySpeed: 3000
                        });
                    });
                    $containerCar.each(function () {
                        var $this = $(this);
                        var $navigate = $this.closest($carousel).find('.Slider-navigate');
                        if ($this.hasClass('Cards_hz')) {
                            $this.slick({
                                appendArrows: $navigate,
                                appendDots: $navigate,
                                dots: true,
                                arrows: true,
                                slidesToShow: 3,
                                slidesToScroll: 2,
                                responsive: [
                                    {
                                        breakpoint: 1600,
                                        settings: {
                                            slidesToShow: 2,
                                            slidesToScroll: 2
                                        }
                                    },
                                    {
                                        breakpoint: 900,
                                        settings: {
                                            slidesToShow: 1,
                                            slidesToScroll: 1
                                        }
                                    }
                                ]
                            });

                        } else {
                            $this.slick({
                                appendArrows: $navigate,
                                appendDots: $navigate,
                                dots: true,
                                arrows: true,
                                slidesToShow: 4,
                                slidesToScroll: 2,
                                responsive: [
                                    {
                                        breakpoint: 1600,
                                        settings: {
                                            slidesToShow: 3,
                                            slidesToScroll: 2
                                        }
                                    },
                                    {
                                        breakpoint: 1230,
                                        settings: {
                                            slidesToShow: 2,
                                            slidesToScroll: 2
                                        }
                                    },
                                    {
                                        breakpoint: 570,
                                        settings: {
                                            slidesToShow: 1,
                                            slidesToScroll: 1
                                        }
                                    }
                                ]
                            });

                        }
                    });

                }
            };
        };
        Slider().init();
        var CartBlock = function () {
            return {
                init: function () {
                }
            };
        };
        CartBlock().init();
        var CategoriesButton = function () {
            return {
                init: function () {
                    $(document).on('click', function (e) {
                        var $this = $(e.target);
                        if ($this.is('a.CategoriesButton-arrow') && $this.closest('.CategoriesButton-link').length) {
                            e.preventDefault();
                            if ($this.next('.CategoriesButton-submenu').is(':visible')) {
                                $('.CategoriesButton .CategoriesButton-submenu').hide(0);
                            } else {
                                $('.CategoriesButton .CategoriesButton-submenu').hide(0);
                                $this.next('.CategoriesButton-submenu').show(0);
                            }
                        } else {
                            if (!$this.hasClass('CategoriesButton-title')) {
                                $this = $(e.target).closest('.CategoriesButton-title');
                            }
                            if ($this.length) {
                                e.preventDefault();
                                $this.closest('.CategoriesButton').toggleClass('CategoriesButton_OPEN');
                            } else {
                                $('.CategoriesButton').removeClass('CategoriesButton_OPEN');
                                $('.CategoriesButton .CategoriesButton-submenu').hide(0);
                            }
                        }
                    });
                }
            };
        };
        CategoriesButton().init();
        var Middle = function () {
            return {
                init: function () {
                }
            };
        };
        Middle().init();
        var Section = function () {
            return {
                init: function () {
                }
            };
        };
        Section().init();
        var BannersHome = function () {
            return {
                init: function () {
                }
            };
        };
        BannersHome().init();
        var Card = function () {
            return {
                init: function () {
                }
            };
        };
        Card().init();
        var CountDown = function () {
            var $blocks = $('.CountDown');

            function getTimeRemaining(endtime) {
                endtime = endtime.split(' ');
                var date = endtime[0].split('.');
                var time = endtime[1].split(':');
                var t = new Date(date[2], date[1] - 1, date[0] - 1, time[0], time[1]) - new Date();
                var seconds = Math.floor((t / 1000) % 60);
                var minutes = Math.floor((t / 1000 / 60) % 60);
                var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
                var days = Math.floor(t / (1000 * 60 * 60 * 24));
                return {
                    'total': t,
                    'days': days,
                    'hours': hours,
                    'minutes': minutes,
                    'seconds': seconds
                };
            }

            function initializeClock(clock, endtime) {
                function updateClock() {
                    var t = getTimeRemaining(endtime);
                    clock.find('.CountDown-days').text(t.days);
                    clock.find('.CountDown-hours').text(t.hours);
                    clock.find('.CountDown-minutes').text(t.minutes);
                    clock.find('.CountDown-secs').text(t.seconds);
                    if (t.total <= 0) {
                        clearInterval(timeinterval);
                    }
                }

                updateClock();
                var timeinterval = setInterval(updateClock, 1000);
            }

            return {
                init: function () {
                    $blocks.each(function () {
                        var $this = $(this);
                        initializeClock($this, $this.data('date'));
                    });
                }
            };
        };
        CountDown().init();
        var Rating = function () {
            return {
                init: function () {
                    $('.Rating_input:not(.Rating_inputClick)').on('click', function () {
                        $(this).addClass('Rating_inputClick');
                    });
                }
            };
        };
        Rating().init();
        var Choice = function () {
            return {
                init: function () {
                }
            };
        };
        Choice().init();
        var Map = function () {
            return {
                init: function () {
                }
            };
        };
        Map().init();
        var Pagination = function () {
            return {
                init: function () {
                }
            };
        };
        Pagination().init();
        var Sort = function () {
            return {
                init: function () {
                }
            };
        };
        Sort().init();
        var Compare = function () {
            var $compare = $('.Compare');
            var $products = $compare.find('.Compare-products');
            var $checkDifferent = $('.Compare-checkDifferent input');
            return {
                init: function () {
                    $products.on('scroll', function () {
                        var $this = $(this);
                        $products.each(function () {
                            $(this)[0].scrollLeft = $this[0].scrollLeft;
                        })
                    });
                    $checkDifferent.on('change', function () {
                        var $this = $(this),
                            $rowsHide = $this.closest($compare).find('.Compare-row_hide');
                        if ($this.prop('checked')) {
                            $rowsHide.hide(0);
                        } else {
                            $rowsHide.show(0);
                        }
                    });
                    $checkDifferent.trigger('change');
                }
            };
        };
        Compare().init();
        var Sort = function () {
            return {
                init: function () {
                }
            };
        };
        Sort().init();
        var NavigateProfile = function () {
            return {
                init: function () {
                }
            };
        };
        NavigateProfile().init();
        var Profile = function () {
            var $avatar = $('.Profile-avatar');
            return {
                init: function () {
                    var $avatarfile = $avatar.find('.Profile-file');

                    function readURL(input) {
                        if (input.files && input.files[0]) {
                            var file = input.files[0],
                                ext = 'неизвестно';
                            ext = file.name.split('.').pop();
                            if (ext === 'png' || ext === 'jpg' || ext === 'gif') {
                                var reader = new FileReader();

                                reader.onload = function (e) {
                                    $(input).closest($avatar).find('.Profile-img img').attr('src', e.target.result);
                                }

                                reader.readAsDataURL(file);
                                return true;
                            }
                            return false;
                        }
                    }

                    $avatarfile.change(function () {
                        var $thisAvatar = $(this).closest($avatar);
                        if (readURL(this)) {
                            $thisAvatar.removeClass('Profile-avatar_noimg');
                            $thisAvatar.next('.form-error').remove();
                            $thisAvatar.find('input[type="file"]').data('errorinput', false);
                        } else {
                            if (!$thisAvatar.next('.form-error').length) {
                                $thisAvatar.find('input[type="file"]').data('errorinput', true);
                                $thisAvatar.after('<div class="form-error">Для загрузки допустимы лишь картинки с расширением png, jpg, gif</div>');
                            }
                        }
                        ;
                    });
                }
            };
        };
        Profile().init();
        var Cart = function () {
            return {
                init: function () {
                }
            };
        };
        Cart().init();
        const Amount = function () {
            let $amount = $('.Amount');
            let $add = $('.Amount-add');
            let $input = $('.Amount-input');
            let $remove = $('.Amount-remove');
            return {
                init: function () {
                    $add.on('click', function (e) {
                        e.preventDefault();
                        var $inputThis = $(this).siblings($input).filter($input);
                        var value = parseFloat($inputThis.val());
                        $inputThis.val(value + 1);
                        let THIS = $(this)
                        let product_id = THIS.data('product')
                        change_product_amount(product_id, $inputThis.val(), true)
                    });
                    $remove.on('click', function (e) {
                        e.preventDefault();
                        var $inputThis = $(this).siblings($input).filter($input);
                        var value = parseFloat($inputThis.val());
                        $inputThis.val(value > 1 ? value - 1 : 1);
                        let THIS = $(this)
                        let product_id = THIS.data('product')
                        change_product_amount(product_id, $inputThis.val(), true)
                    });
                    $input.change(function (e) {
                        e.preventDefault()
                        let THIS = $(this)
                        let product_id = THIS.data('product')
                        let amount = THIS.val()
                        if (!isNaN(parseFloat(amount)) && isFinite(amount)) {
                            change_product_amount(product_id, amount, true)
                        } else {
                            toastr.options = toasterOptions
                            toastr.error('Количество должно быть числом!')
                            THIS.val('1')
                            THIS.focus()
                        }

                    })
                }
            };
        };
        Amount().init();
        var Order = function () {
            var $next = $('.Order-next'),
                $blocks = $('.Order-block'),
                $navigate = $('.Order-navigate');
            return {
                init: function () {
                    $next.add($navigate.find('.menu-link')).on('click', function (e) {
                        e.preventDefault();
                        var $this = $(this),
                            href = $this.attr('href'),
                            error = false,
                            $validate = $this.closest($blocks).find('[data-validate]')
                        if ($(e.target).is('.Order-next')) {
                            $validate.each(function () {
                                var $this = $(this);
                                $this.trigger('blur');
                                if ($this.data('errorinput')) {
                                    error = true
                                }
                            });
                        }
                        if (error === false && ($(e.target).is('.Order-next') ||
                            $blocks.index($(href)) < $blocks.index($blocks.filter('.Order-block_OPEN')))
                        ) {
                            $blocks.removeClass('Order-block_OPEN');
                            $(href).addClass('Order-block_OPEN');
                            $navigate.find('.menu-item').removeClass('menu-item_ACTIVE');
                            $navigate.find('.menu-link[href="' + href + '"]')
                                .closest('.menu-item')
                                .addClass('menu-item_ACTIVE');
                        }

                    });
                }
            };
        };
        Order().init();
        var Account = function () {
            return {
                init: function () {
                }
            };
        };
        Account().init();
        var Payment = function () {
            return {
                init: function () {
                    $('.Payment-generate').on('click', function (e) {
                        var $this = $(this),
                            $bill = $this.closest('.Payment').find('.Payment-bill'),
                            billNumber = '';
                        e.preventDefault();
                        do {
                            billNumber = Math.random() + '';
                            billNumber = billNumber.slice(-9, -1);
                        } while (parseFloat(billNumber) % 2 !== 0);
                        billNumber = billNumber.slice(0, 4) + ' ' + billNumber.slice(4, 8);
                        $bill.val(billNumber);
                    });
                    $('.Payment-pay .btn').on('click', function (e) {
                        var $this = $(this),
                            $validate = $this.closest('.form').find('[data-validate]');

                        $validate.each(function () {
                            var $this = $(this);
                            $this.trigger('blur');
                            if ($this.data('errorinput')) {
                                e.preventDefault();
                            }
                        });
                    });
                }
            };
        };
        Payment().init();
        var Tabs = function () {
            var $tabs = $('.Tabs');
            var $tabsLink = $('.Tabs-link');
            var $tabsBlock = $('.Tabs-block');
            return {
                init: function () {
                    // var $steps = $('.Tabs_steps');
                    // var $step = $steps.find($tabsLink).not($steps.find($tabs).find($tabsLink));
                    // var $blocks = $steps.find($tabsBlock).not($steps.find($tabs).find($tabsBlock));
                    // $blocks.hide(0);
                    // var href = $step.eq(0).attr('href');
                    // var $active = $(href);
                    // var $links= $step.add($step.siblings($tabsLink));
                    // $links.removeClass('Tabs-link_ACTIVE');
                    // $step.eq(0).addClass('Tabs-link_ACTIVE');
                    // $active.show(0);

                    $tabsLink.on('click', function (e) {
                        var $this = $(this);
                        var href = $this.attr('href');
                        if (href[0] === "#") {
                            e.preventDefault();
                            var $parent = $this.closest($tabs);
                            if ($parent.hasClass('Tabs_steps')) {
                            } else {
                                var $blocks = $parent.find($tabsBlock).not($parent.find($tabs).find($tabsBlock));
                                var $links = $this.add($this.siblings($tabsLink));
                                var $active = $(href);
                                $links.removeClass('Tabs-link_ACTIVE');
                                $this.addClass('Tabs-link_ACTIVE');
                                $blocks.hide(0);
                                $active.show(0);
                            }
                        }

                    });
                    $('.TabsLink').on('click', function (e) {
                        var $this = $(this);
                        var href = $this.attr('href');
                        var $active = $(href);
                        var $parent = $active.closest($tabs);
                        if ($parent.hasClass('Tabs_steps')) {
                        } else {
                            var $blocks = $parent.find($tabsBlock).not($parent.find($tabs).find($tabsBlock));
                            var $link = $('.Tabs-link[href="' + href + '"]');
                            var $links = $link.add($link.siblings($tabsLink));
                            $links.removeClass('Tabs-link_ACTIVE');
                            $link.addClass('Tabs-link_ACTIVE');
                            $blocks.hide(0);
                            $active.show(0);
                        }

                    });
                    $tabs.each(function () {
                        $(this).find($tabsLink).eq(0).trigger('click');
                    });
                }
            };
        };
        Tabs().init();
// setTimeout(function(){
//     $('body').css('opacity', '1');
// }, 100);
        var ProductCard = function () {
            var $picts = $('.ProductCard-pict');
            var $photo = $('.ProductCard-photo');
            return {
                init: function () {
                    $picts.on('click', function (e) {
                        e.preventDefault();
                        var $this = $(this);
                        var href = $this.attr('href');
                        $photo.empty();
                        $photo.append('<img src="' + href + '" />');
                        $picts.removeClass('ProductCard-pict_ACTIVE');
                        $this.addClass('ProductCard-pict_ACTIVE');
                    });
                }
            };
        };
        ProductCard().init();
        var Comments = function () {
            return {
                init: function () {
                    $('[data-action="comments-show"]').on('click', function (e) {
                        e.preventDefault();
                        var $this = $(this),
                            text = $this.data('text-alt'),
                            $comments = $this.prev('.Comments').find('.Comments-wrap_toggle');
                        $this.data('text-alt', $this.text());
                        $this.text(text);
                        $comments
                            .toggleClass('Comments-wrap_HIDE');
                        $('.fixScrollBlock').trigger('render.airStickyBlock');
                    });
                }
            };
        };
        Comments().init();
        var Product = function () {
            return {
                init: function () {
                }
            };
        };
        Product().init();
        var ProgressPayment = function () {
            return {
                init: function () {
                }
            };
        };
        ProgressPayment().init();
        var Categories = function () {
            return {
                init: function () {
                    if ($(window).width() < 990) {
                        var $more = $('.Categories-more'),
                            $trigger = $('.Categories-trigger');
                        $trigger.on('click', function (e) {
                            e.preventDefault();
                            var $this = $(this),
                                text = $this.data('text-alt'),
                                $block = $this.prev($more);
                            $this.data('text-alt', $this.text());
                            $this.text(text);
                            $this.toggleClass('Categories-trigger_OPEN');
                            $block.toggle(0);
                        });
                    }
                }
            };
        };
        Categories().init();
//ENDion.js
//END


    });


})(jQuery);

function initModalLogin() {
    $('#login-modal-form').modal('show')
}

function initMasks() {
    console.log('initMasks()')
    let mask_phone_dom = $("#id_phoneNumber");
    mask_phone_dom.inputmask(
        {
            mask: "+7-999-999-99-99",
            removeMaskOnSubmit: true,
            autoUnmask: true
        }
    );
}

function initCheckCityAddress() {
    let checker = setInterval(() => {
        let city = $('#id_city')
        let address = $('#id_address')
        let btn_to_step_3 = $('#btn_to_step_3')
        let errorsField = $('#show-me-pls')
        if (city.length > 0 && address.length > 0) {
            if (city.val().length < 3 || address.val().length < 3) {
                errorsField.show()
                btn_to_step_3.hide()
                // btn_to_step_3.removeClass('btn_success')
                // btn_to_step_3.removeClass('Order-next')
                // btn_to_step_3.addClass('btn_muted')
                // btn_to_step_3.attr('href', '#')
            } else {
                errorsField.hide()
                btn_to_step_3.show()
                // btn_to_step_3.removeClass('btn_muted')
                // btn_to_step_3.addClass('btn_success')
                // btn_to_step_3.addClass('Order-next')
                // btn_to_step_3.attr('href', next_step_href)
            }
            // let validator = $('#step_2_form').validate();
            // console.log(validator)
        } else {
            // console.log('fields not found')
        }


    }, 100);
}

function editOrderData() {
    let full_name_dom = $('#id_full_name')
    let full_name = full_name_dom.val()

    let phoneNumber_dom = $('#id_phoneNumber')
    let phoneNumber = phoneNumber_dom.val()

    let email_dom = $('#id_email')
    let email = email_dom.val()

    let city_dom = $('#id_city')
    let city = city_dom.val()

    let address_dom = $('#id_address')
    let address = address_dom.val()

    let delivery_dom = $('input[name=delivery]:checked')
    let delivery = delivery_dom.data('value')
    let delivery_value = delivery_dom.val()

    let pay_dom = $('input[name=pay]:checked')
    let pay = pay_dom.data('value')
    let pay_value = pay_dom.val()

    let data = {
        full_name,
        phoneNumber,
        email,
        city,
        address,
        delivery_value,
        pay_value
    }

    $('#order_full_name').html(full_name)
    $('#order_phone').html(phoneNumber)
    $('#order_email').html(email)
    $('#order_delivery').html(delivery)
    $('#order_city').html(city)
    $('#order_address').html(address)
    $('#order_payment').html(pay)

    let total_price_dom = $('#total-price')
    let total_price = total_price_dom.data('totalprice')

    let delivery_title = $('#delivery_title')
    let delivery_price = $('#delivery_price')
    let delivery_description = $('#delivery_description')

    let delivery_add_price = 0

    if (delivery_dom.val() === "1") {
        delivery_title.html(delivery)
        if (total_price < order_delivery_limit) {
            delivery_add_price = order_delivery_price
            delivery_price.html(order_delivery_price + '$')
            delivery_description.html('Доставка платная, так как сумма заказа менее ' + order_delivery_limit + '$')
        } else {
            delivery_price.html(0 + '$')
            delivery_description.html('Доставка бесплатная, так как сумма заказа более ' + order_delivery_limit + '$')
        }
    }

    if (delivery_dom.val() === "2") {
        delivery_title.html(delivery)
        delivery_add_price = order_delivery_express
        delivery_price.html(order_delivery_express + '$')
        delivery_description.html('Стоимость экспресс-доставки')
    }

    let summary = total_price + delivery_add_price

    total_price_dom.html(summary + '$')

    TOTAL_DATA = data
}

function createOrder() {
    console.log(TOTAL_DATA)
    let data = {
        csrfmiddlewaretoken: csrf_token,
        ...TOTAL_DATA
    }
    // console.log(data)
    $.ajax({
        data: data,
        method: 'POST',
        url: url_ajax_create_order,
        dataType: 'json',
        success: function (json) {
            if (json.result) {
                console.log(json)
                window.location.href = '/order/' + json.order + '/payment'
                // toastr.options = toasterOptions;
                // toastr.success(json.msg);
                // update_cart_view()
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

function cancel_order(order_id) {
    if (confirm('Вы действительно желаете отменить данный заказ?')) {
        let data = {
            csrfmiddlewaretoken: csrf_token,
            order_id
        }
        // console.log(data)
        $.ajax({
            data: data,
            method: 'POST',
            url: url_ajax_cancel_order,
            dataType: 'json',
            success: function (json) {
                if (json.result) {
                    console.log(json)
                    window.location.href = '/order-canceled'
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
    }
    return false;
}

function generate_bill() {
    console.log('here1')
    let card_number_dom = $('#id_card_number')
    let min = 10000000;
    let max = 99999999;
    let result = Math.floor(Math.random() * (max - min + 1)) + min;
    console.log('here2')
    card_number_dom.val(result);
    // $('#id_card_number').focus()
    console.log('here3')
    setTimeout(function () {
        console.log('here4')
        card_number_dom.focus();
    }, 500);
    console.log('here5')
    // $('#id_card_number').click()
    // $('#id_card_number').blur()
}