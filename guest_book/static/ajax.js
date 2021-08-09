$(document).ready(function() {
  
  console.log( "ready!" );
  
  // Taking entries (in single JSON) from server
  
  function getEntries(response) {
    console.log('PING');
    console.log(response);
    for (let i = 0; len = response.user.length; i++) {
      insert = "<dt> " + response.user[i] + " <span> " + response.date[i] + " </span>\n</dt> " + " <dd> " + response.text[i] + " </dd>";
      $("list").append(insert)};
    };
  
  // Taking data from URL - nr of entries and page
  
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  if (queryString.length > 0) {
    var quantity = urlParams.get('quantity');
    var page = urlParams.get('page');
    } else {
    var quantity = $("#quantity").val();
    var page = 1;};
  
  // First data taken from server

  var firstQuery = {"user": null, "quantity" : quantity, 'page': page};
  $.getJSON("/api", firstQuery, getEntries(data));
  
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
