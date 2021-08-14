$(document).ready(function main () {
  
  var currentUser = null;
  
  // Gets default number of pages and max page from server. 
  
  function getInitConfig (quantity) {
    $.getJSON('/config', quantity, function(data) {
      page_place = document.getElementById("page");
      page_place.setAttribute("max", data.max_page);
      page_place.setAttribute("value", 1);
      quantity_place = document.getElementById("quantity");
      quantity_place.setAttribute("value", data.quantity);
      });
    };
   
   // Gets max page from server
   
  function getMaxPage (user, quantity) {
    query = {'user': user, 'quantity': quantity};
    $.getJSON('/maxpage', query, function(data) {
    page_place.setAttribute("max", data.max_page);
    page_place.setAttribute("value", 1)});
    };
  
  // Refreshes page. Uses funtion below

  function refreshPage (user) {
    let quantity = $("#quantity").val();
    let page = $("#page").val();
    getMaxPage(user, quantity);
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
      
      // First creates user name
      insert = "<dt class = 'entry entry'> " + 
      '<a href=/user/' + response.user[i]  +  ' class = "entryuser" name = "entryuser">' + response.user[i] + "</a> napisał(a) o " +
      
      // Adds date
      response.date[i] + " </dt> " + 
      
      // Shows snippet of entry with hyperlink 
      " <dd class = 'entry entry_text'><p><a href = /entry/" + response.entryid[i] + " >" +
      response.text[i] + " </p></dd>";
      
      // Adds entry to list
      $("#list").append(insert)};
    };
  
  // First app tries to take data from URL
  // if not - default number of pages and max page from server
  
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  if (queryString.length > 0) {
    let quantity = urlParams.get('quantity');
    let page = urlParams.get('page');
    let firstQuery = {"user": currentUser, "quantity" : quantity, "page": page};
    getEntries (firstQuery);
    } else {
    let firstQuery = {"user": currentUser, "quantity" : $('#quantity').val(), "page": 1};
    getEntries (firstQuery);
    };
  
  // Taking default data - nr of entries and page
  
  getInitConfig(null);
  
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
    
    // Setting user name as current user and quering entries

    $(document).on('click','.entryuser', function(event){
      event.preventDefault();
      //$(this).text("It works!");
      currentUser = $(this).text();
      refreshPage(currentUser);
    });
     

});
