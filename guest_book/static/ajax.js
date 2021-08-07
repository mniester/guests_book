$(document).ready(function() {
  
  console.log( "ready!" );
  
  // Taking data from URL - nr of entries and page
  
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  if (queryString.length > 0) {
    var quantity = urlParams.get('quantity');
    var page = urlParams.get('page');
    console.log(quantity, page)};
  
  // Taking data from form - nr of entries and page
  
  $('#quantity_page').click(function (event) {
    event.preventDefault();
    quantity = $("#quantity").val();
    page = $("#page").val();
    console.log(quantity, page);});

});
