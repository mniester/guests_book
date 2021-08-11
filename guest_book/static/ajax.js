$(document).ready(function main () {
  
  var currentUser = null;
  
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
  
  // Refreshes page. Uses funtion below

  function refreshPage (user) {
    let quantity = $("#quantity").val();
    let page = $("#page").val();
    getConfig('quantity='+ quantity);
    let query = {"user": user, "quantity" : quantity, "page": page};
    getEntries (query)};

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
    let firstQuery = {"user": currentUser, "quantity" : $('#quantity').val(), "page": 1};
    getEntries (firstQuery);
    };
  
  // Validation error - no proper numeric data provided
  
  function noNumbersError() {alert('Proszę podać dane liczbowe')};
  
  // Validation error - empty "user" input or "text" textarea

  function noEntryError() {alert('Proszę podać nick użytkownika oraz post')};

  // Taking data from upper form - nr of entries and page

  $('#quantity_page').click(function (event) {
    event.preventDefault();
    let quantity = $("#quantity").val();
    let page = $("#page").val();
    if (quantity.length == 0 || page.length == 0) {
      noNumbersError();
      } else { refreshPage(currentUser) };
    });

  // Adding new post to data base

  $('#add').click(function (event) {
    event.preventDefault();
    let user = $("#user").val();
    let text = $("#text").val();
    if (user.length == 0 || text.length == 0) {
    noEntryError();
    } else {
    json = {"user": user, "text":text};
    $.post("/api", json);
    refreshPage(currentUser)};
    });

});
