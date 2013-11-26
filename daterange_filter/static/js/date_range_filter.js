/**
 * Created by ahmetdal on 11/26/13.
 */


$(document).ready(function () {
    $.datepicker.setDefaults($.datepicker.regional[lang])
    $(".vDateField").attr('readonly', true);
    $(".vDateField").datepicker(
        {
            dateFormat: 'yy-mm-dd',
            onSelect: function (dateText, inst) {
                var qs = $.deparam.querystring()
                qs[$(this).attr('name')] = dateText
                window.location.href = $.param.querystring('', qs);
            }
        });
});
