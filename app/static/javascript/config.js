/********************************/
/* config.js                    */
/********************************/

$( document ).ready(function() {
    $( "#tabs" ).tabs();
    $('#tabs').css('width','100%');
    $("#start_time").datetimepicker({
        datepicker: false,
        format: 'H:i'
    });
    $("#end_time").datetimepicker({
        datepicker: false,
        format: 'H:i'
    });
    showdiv('times')
})

function showdiv(divname) {
    $(".results").hide();
    $("#"+divname).show();
}