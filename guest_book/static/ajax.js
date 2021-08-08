$(document).ready(function() {
  
  console.log( "ready!" );
  
  // Taking entries (in single JSON) from server
  
  function getEntries(response) {
    response = JSON.parse(response);
    {for (let i = 0; len = response.user.length; i++) {
      insert = "<dt> " + response.user[i] + " <span> " + response.date[i] + " </span>\n</dt> " + " <dd> " + response.text[i] + " </dd>";
      $("list").append(insert)};
    };
  };
  
  // First data taken from server

  var firstQuery = {"user": null, "quantity" : $("#quantity").val()};
  $.getJSON("/api", firstQuery, function(data) {getEntries(data)});
  
  // Taking data from URL - nr of entries and page
  
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  if (queryString.length > 0) {
    var quantity = urlParams.get('quantity');
    var page = urlParams.get('page');
    };
  
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
