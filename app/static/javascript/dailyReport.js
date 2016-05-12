$(document).ready(function(){
    $('#toggle').click(function(){
        if($(this).data('name') == 'hide') {
            $('#collapse').css('display', 'inline');
            $(this).data('name', 'show');
            $(this).data('value', 'Hide Numerical Values');
        } else {
            $('#collapse').css('display', 'none');
            $(this).data('name', 'hide');
            $(this).data('value', 'Show Numerical Values');

        }
    });

});