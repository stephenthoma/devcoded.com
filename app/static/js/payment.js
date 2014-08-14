(function ($) {
    $.fn.serializeObject = function () {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };
})(jQuery);


(function (ctx) {
    'use strict';
    var _options;
    var isCalling;
    var submitPurchase = function (e) {
        var $form = $('form#purchase');
        if ($form.find('input:visible').length == 0) {
            //  this is the repeat flow, let it happen naturally
            return;
        }

        e.preventDefault();

        resetForm($form);

        //  build data to submit
        var cardData = $form.serializeObject();

        // Uncomment to trim WTForms information.
        //for (var key in cardData) {
            //var trimmedKey = key.replace('purchase-', '');
            //cardData[trimmedKey] = cardData[key];
            //delete cardData[key];
        //}

        var name = $('[name$="name"]', $form).val();
        var emailAddress = 'test@gmail.com'; //[TODO]: Get current user's email

        //  validate form
        if (!name) {
            addErrorToField($form, 'name');
        }
        if (!balanced.emailAddress.validate(emailAddress)) {
           //[TODO]: This should probably do something..
        }
        if (!balanced.card.isCardNumberValid(cardData.number)) {
            addErrorToField($form, 'number');
        }
        if (!balanced.card.isExpiryValid(cardData.expiration_month, cardData.expiration_year)) {
            addErrorToField($form, 'expiration_month');
        }

        if ($form.find('.input-group.error').length) {
            return;
        }

        //  submit
        disableForm($form);
        showProcessing('Processing payment...', 33);
        balanced.card.create(cardData, completePurchase);
    };
    var completePurchase = function (response) {
        var $form = $('form#purchase');
        var sensitiveFields = ['number', 'name', 'expiration_month', 'expiration_year'];

        hideProcessing();
        console.log(response);
        switch (response.status_code) {
            case 201:
                showProcessing('Making payment...', 66);
                //  IMPORTANT - remove sensitive data to remain PCI compliant
                removeSensitiveFields($form, sensitiveFields);
                $form.find('input').removeAttr('disabled');
                console.log(response.cards[0].href)
                $('<input type="hidden" name="card_uri" value="' + response.cards[0].href + '">').appendTo($form);
                $form.unbind('submit', submitPurchase).submit();
                break;
            case 400:
                var fields = ['name', 'number', 'expiration_month', 'expiration_year', ''];
                var found = false;
                for (var i = 0; i < fields.length; i++) {
                    var isIn = response.error.description.indexOf(fields[i]) >= 0;
                    console.log(isIn, fields[i], response.error.description);
                    if (isIn) {
                        resetForm($form);
                        addErrorToField($form, fields[i]);
                    }
                }
                if (!found) {
                    console.warn('missing field - check response.error for details');
                    console.warn(response.error);
                }
                break;
            case 402:
                console.warn('we couldn\'t authorize the buyer\'s credit card - check response.error for details');
                console.warn(response.error);
                showError('We couldn\'t authorize this card, please check your card details and try again');
                break;
            case 404:
                console.warn('your marketplace URI is incorrect');
                break;
            case 500:
                console.error('Balanced did something bad, this will never happen, but if it does please retry the request');
                console.error(response.error);
                showError('Balanced did something bad, please retry the request');
                break;
        }
    };
    var showProcessing = function (message, progress) {
        progress = progress || 50;
        var $loader = $('.loading');
        if (!$loader.length) {
            $loader = $(
                '<div class="loading">' +
                    '<div class="progress progress-striped active">' +
                    '<div class="bar"></div>' +
                    '</div>' +
                    '<p>&nbsp;</p>' +
                    '</div>');
            $loader.appendTo('body');
        }
        $loader.find('.bar').css({width:progress + '%'});
        $loader.find('p').text(message);
        $loader.css({
            left:$('body').width() / 2 - $loader.width() / 4,
            top:'400px'
        }).show();
    };
    var hideProcessing = function () {
        $('.loading').hide();
    };
    var showError = function (message) {
        var $alert = $('.alert:visible');
        if ($alert.length) {
            $alert.remove();
        }
        $alert = $(
            '<div class="animated bounceInLeft alert form-error-box" data-animation="bounceInLeft">' +
                '<button class="close" data-dismiss="alert">&times;</button>' +
                '<span>' +
                message +
                '</span></div>');
        $alert.insertBefore('.form-content').show();
    };
    var hideError = function () {
        $('.alert').hide();
    };
    var resetForm = function ($form) {
        if (!$form) {
            $form = $('form');
        control}
        $form.find('.input-group').removeClass('error');
        $form.find('input,button,select').removeAttr('disabled');
    };
    var disableForm = function ($form) {
        $form.find('input, button, select').attr('disabled', 'disabled');
    };
    var addErrorToField = function ($form, fieldName) {
        $form.find('[name$="' + fieldName + '"]')
            .closest('.input-group')
            .addClass('error');
    };
    var removeSensitiveFields = function ($form, sensitiveFields) {
        for (var i = 0; i < sensitiveFields.length; i++) {
            sensitiveFields[i] = '[name$="' + sensitiveFields[i] + '"]';
        }
        sensitiveFields = sensitiveFields.join(',');
        $form.find(sensitiveFields).remove();
    };
    ctx.devcoded = {
        init:function (options) {
            _options = options;
            balanced.init(options.marketplaceUri);
            $('form#purchase').submit(submitPurchase);
            //$('[data-dismiss="alert"]').live('click', function (e) {
                //$(this).closest('.alert').fadeOut('fast');
                //resetForm();
                //e.preventDefault();
            //});
        }
    };
})(this);
