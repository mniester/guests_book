$(document).ready(function() {
  
  console.log( "ready!" );
  
  // Taking data from URL - nr of entries and page
  
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  if (queryString.length > 0) {
    var quantity = urlParams.get('quantity');
    var page = urlParams.get('page');
    console.log(quantity, page)};
  
  // Validation error - no data provided
  
  function noNumbersError() {alert('Proszę podać dane liczbowe')};
  
  // Validation error - can't convert string to numeric
  
  function numbersRequired() {alert('Proszę podać liczby')};
  
  // Taking data from form - nr of entries and page

  $('#quantity_page').click(function (event) {
    event.preventDefault();
    var quantity = $("#quantity").val();
    var page = $("#page").val();
    if (quantity.length == '' || page.length == '') {
      noNumbersError();
      } else {
      quantity = parseInt(quantity);
      page = parseInt(page)};
    x = quantity;
    y = page;
    console.log(x, y);});

});
