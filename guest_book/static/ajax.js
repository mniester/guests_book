$(document).ready(function() {
  
  console.log( "ready!" );
  
  // Taking data from form - nr of entries and page
  
  $('#quantity_page').click(function (event) {
    event.preventDefault();
    quantity = $("#quantity").val();
    page = $("#page").val();
    console.log(quantity, page);});
  
  // console.log(quantity, page);

});
