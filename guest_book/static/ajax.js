$(document).ready(function main () {
  
  console.log( "ready!" );
  
  // Taking entries (in single JSON) from server
  
  function printEntries(response) {
    for (let i = 0; i < response.user.length; i++) {
      insert = "<dt><p> " + response.user[i] + " <span> " + response.date[i] + "  </p></span></dt> " + " <dd><p> " + response.text[i] + " </p></dd>";
      $("#list").append(insert)};
    };
  
  // Taking default data - nr of entries and page
  // First app tries to take data from URL
  // if not - takes quantity of pages from form and show first page
  
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  if (queryString.length > 0) {
    var quantity = urlParams.get('quantity');
    var page = urlParams.get('page');
    } else {
    var quantity = $("#quantity").val();
    var page = 1};
  
  // First data taken from server
  
  var firstQuery = {"user": null, "quantity" : quantity, "page": page};
  $.getJSON("/api", firstQuery, function (data) { printEntries(data) });
  
  // Validation error - no proper numeric data provided
  
  function noNumbersError() {alert('Proszę podać dane liczbowe')};
  
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
    console.log(quantity, page);});

});
