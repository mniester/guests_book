$(document).ready(function main () {
  
  // get default number of pages and max page from server
  
  function getConfig (quantity) {
    $.getJSON('/config', quantity, function(data) {
      page_place = document.getElementById("page");
      page_place.setAttribute("max", data.max_page);
      page_place.setAttribute("value", 1);
      quantity_place = document.getElementById("quantity");
      quantity_place.setAttribute("value", data.quantity);
      });
    };
  
  // Taking entries (in single JSON) from server
  
  function getEntries (query) {
    $.getJSON("/api", query, function (data) { printEntries(data) });
    };
  
  // Cleaning page and putting new entries into it
  
  function printEntries(response) {
    $(".entry").remove();
    for (let i = 0; i < response.user.length; i++) {
      insert = "<dt class = 'entry'> " + response.user[i] + " napisał(a) o " +
      response.date[i] + " </dt> " + " <dd class = 'entry entry_text'><p> " + response.text[i] + " </p></dd>";
      $("#list").append(insert)};
    };
  
  // Taking default data - nr of entries and page
  
  getConfig(null);
  
  // First app tries to take data from URL
  // if not - default number of pages and max page from server
  
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  if (queryString.length > 0) {
    let quantity = urlParams.get('quantity');
    let page = urlParams.get('page');
    let firstQuery = {"user": null, "quantity" : null, "page": 1}
    } else {
    let firstQuery = {"user": null, "quantity" : $('#quantity').val(), "page": 1};
    getEntries (firstQuery);
    };
  
  // Validation error - no proper numeric data provided
  
  function noNumbersError() {alert('Proszę podać dane liczbowe')};
  
  // Taking data from form - nr of entries and page

  $('#quantity_page').click(function (event) {
    event.preventDefault();
    let quantity = $("#quantity").val();
    let page = $("#page").val();
    if (quantity.length == '' || page.length == '') {
      noNumbersError();
      } else {
      quantity = parseInt(quantity);
      page = parseInt(page)};
    getConfig('quantity='+ quantity);
    let query = {"user": null, "quantity" : quantity, "page": page};
    getEntries (query);});

});
