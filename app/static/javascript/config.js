/********************************/
/* config.js                    */
/********************************/

$( document ).ready(function() {
    $("#start_time").datetimepicker({
        datepicker: false,
        format: 'H:i'
    });
    $("#end_time").datetimepicker({
        datepicker: false,
        format: 'H:i'
    });
})