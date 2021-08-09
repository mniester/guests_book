$(document).ready(function main () {
  
  // get default number of pages and max page from server
  
  var defaultConfig = $.getJSON('/default', null);
  console.log(defaultConfig);
  
  // Taking entries (in single JSON) from server
  
  function getEntries (query) {
    $.getJSON("/api", query, function (data) { printEntries(data) });
    };
  
  // Clening Putting entries in page
  
  function printEntries(response) {
    for (let i = 0; i < response.user.length; i++) {
      insert = "<dt> " + response.user[i] + " napisał(a) o " +
      response.date[i] + " </dt> " + " <dd><p> " + response.text[i] + " </p></dd>";
      $("#list").append(insert)};
    };
  
  // Taking default data - nr of entries and page
  // First app tries to take data from URL
  // if not - default number of pages and max page from server
  
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  if (queryString.length > 0) {
    var quantity = urlParams.get('quantity');
    var page = urlParams.get('page');
    } else {
    var quantity = $("#quantity").val();
    var page = $("#page").val()};
  
  // First data taken from server
  
  var firstQuery = {"user": null, "quantity" : quantity, "page": 1};
  getEntries (firstQuery);
  
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
    var query = {"user": null, "quantity" : quantity, "page": page};
    getEntries (query);});

});
