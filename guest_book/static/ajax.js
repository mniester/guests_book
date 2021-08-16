$(document).ready(function main () {
  
  var currentUser = null;
  var currentText = null;
  var maxUserNickLength = null;
  var maxEntryLength = null;
  var page = document.getElementById("page");
  var resetButton = null;
  
  // Gets default number of pages and max page from server. 
  
  function getInitConfig () {
    $.getJSON('/config', null, function(data) {
      page.setAttribute("max", data.max_page);
      page.setAttribute("value", 1);
      let quantity = document.getElementById("quantity");
      quantity.setAttribute("value", data.quantity);
      maxUserNickLength = data.max_user_nick_len;
      maxEntryLength = data.max_entry_len;
      resetButton = data.reset_button
      });
    };
   
   // Gets max page from server
   
  function getMaxPage (user, text, quantity) {
    query = {'user': user, 'text': text, 'quantity': quantity};
    console.log(query);
    $.getJSON('/maxpage', query, function(data) {
    page.setAttribute("max", data.max_page);
    page.setAttribute("value", 1)});
    };
  
  // Refreshes page. Uses function below
  // exact is boolean shows whether query 

  function refreshPage (user, text, exact) {
    let quantity = $("#quantity").val();
    let page = $("#page").val();
    getMaxPage(user, text, quantity);
    let query = {"user": user, 'text': text, "quantity" : quantity, "page": page};
    if (exact === true) {
      query.exact = true};
    getEntries (query)};
    
  // Taking entries (in single JSON) from server
  
  function getEntries (query) {
    $.getJSON("/api", query, function (data) {printEntries(data)});
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
      " <dd class = 'entry entry_text'><p><a href = /entry/" + response.entryid[i] + " target='_blank'>" +
      response.text[i] + " </p></dd>";
      
      // Adds entry to list
      $("#list").append(insert)};
    };

  // Taking default data - nr of entries and page
  
  getInitConfig(null);

  // First app tries to take data from URL
  // if not - default number of pages and max page from server
  
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  if (queryString.length > 0) {
    let user = urlParams.get('user');
    if (user === null) {
      user = currentUser};
    let text = urlParams.get('text');
    if (text === null) {
      text = currentText};
    let quantity = urlParams.get('quantity');
    if (quantity === null) {
      quantity = $("#quantity").val()};
    let page = urlParams.get('page');
    if (page = null) {
      page = $("#page").val()};
    let firstQuery = {"user": user, "text": text, "quantity" : quantity, "page": page, "exact": true};
    getEntries (firstQuery);
  } else {
    let quantity = $('#quantity').val();
    let urlQuery = {"user": currentUser, 'text': currentText, "page": 1};
    getEntries (urlQuery);
    };
  
  // Validation error - no proper numeric data provided
  
  function noNumbersError() {alert('Proszę podać dane liczbowe')};
  
  // Validation error - empty "user" input or "text" textarea

  function noEntryError() {alert('Proszę podać nick użytkownika oraz post')};

  // Validation error - too long user nick

  function tooLongUserNick() {alert('Maksymalna długość nicku wynosi ' + maxUserNickLength)};

  // Validation error - too long entry text

  function tooLongText() {alert('Maksymalna długość wpisu wynosi ' + maxEntryLength)};

  // Taking data from upper form - nr of entries and page

  $('#quantity_page').click(function (event) {
    event.preventDefault();
    let quantity = $("#quantity").val();
    let page = $("#page").val();
    if (quantity.length == 0 || page.length == 0) {
      noNumbersError();
    } else {
      refreshPage(currentUser, currentText) };
    });

  // Adding new post to data base

  $('#add').click(function (event) {
    event.preventDefault();
    let user = $("#user").val();
    let text = $("#text").val();
    if (user.length == 0 || text.length == 0) {
      noEntryError();
    } else if ( user.length > maxUserNickLength) {
      tooLongUserNick();
    } else if ( text.length > maxEntryLength) {
      tooLongText();
    } else {
      json = {"user": user, "text":text};
      $.post("/api", json);
      refreshPage(currentUser, currentText)};
    });

    // Searching database
  
  $('#query').click(function (event) {
    event.preventDefault();
    let user = $("#user").val();
    let text = $("#text").val();
    if (user.length == 0 && text.length == 0) {
      noEntryError();
  } else if ( user.length > maxUserNickLength) {
      tooLongUserNick();
  } else if ( text.length > maxEntryLength) {
      tooLongText();
  } else {
    let quantity = $('#quantity').val();
    currentText = text;
    getMaxPage (user, text, quantity);
    query = {"quantity": quantity, "user": user, "text":text};
    getEntries(query)};
    $('#reset').text('Pokaż pozostałe wpisy');
  });

    // Setting user name as current user and quering entries

  $(document).on('click','.entryuser', function(event){
    event.preventDefault();
    currentUser = $(this).text();
    $('#reset').text('Pokaż pozostałe wpisy');
    refreshPage(currentUser, currentText, true);
    });
    
    // Check entries of all users

  $(document).on('click','#reset', function(event){
    event.preventDefault();
    currentUser = null;
    currentText = null;
    $('#reset').text(resetButton);
    refreshPage(currentUser, currentText);
  });
});
