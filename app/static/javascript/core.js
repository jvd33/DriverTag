//Run on page load
$(function() {
  //Set hover functions for the library button
  $("#reportnav").hover(
    function() {
      $("#reportmenu").css("display", "block");
      //$("#dropdown").stop().slideDown(100);
      },
    function() {
      //$("#dropdown").stop().slideUp(100);
      $("#reportmenu").css("display", "none");
      });
});