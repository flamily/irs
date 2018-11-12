/**
* All functions for html generation & endpoint data calls to create a seemless, one page dashboard solution
*
* Author: Jacob Vorreiter
* Date: 12/11/2018
*/

var options = "";
var mode = "Customer";

/**
* One time endpoint call make ready the options for a year selector
*/
function populateYearOptions(){
  function callback(data){
    $.each(data.years, function(k, v){
      options += "<option value='" + v + "'>" + v + "</option>";
    });
  }

  if (options.length == 0){
    $.getJSON('/api/time/get_years', callback);
  }
}

/**
* JS HTML generator for date format change (date, week, month, year)
* @param {String} inputType String for date format change
*/
function changeDatePicker(inputType){
  var decoration = "id='date-picker' class='form-control form-control-sm' onchange='updateAll()'";
  if (inputType == "year"){
    var selector = document.getElementById("date-picker-module");
    selector.innerHTML = "<select name='year'" + decoration + ">" + options + "</select>";
  } else {
    document.getElementById("date-picker-module").innerHTML = "<input name='" + inputType + "' type=" + inputType + " " + decoration + ">";
  }
}

/**
* Generates the string to call the correct endpoint
* @return {String} A formatted, populated api call (eg /api/reporting/Customer/week?dateString=2018-W45)
*/
function getAPIString(){
  var date_type = document.getElementById('date-picker').getAttribute("name");
  var date_string = $("#date-picker").val();
  var item_selector_value = $("select#item-selector>option:selected").attr("value");

  if (typeof item_selector_value == "undefined"){
    item_selector_value = 1;
  }
  if (mode == "Customer"){
      var api_string = '/api/reporting/' + mode + '/' + date_type + '?dateString=' + date_string;
  } else {
    var api_string = '/api/reporting/' + mode + '/' + item_selector_value + '/' + date_type + '?dateString=' + date_string;
  }

  return api_string;
}

/**
* Updates the chart and table, calling appropriate functions to get data from the endpoint
*/
function updateAll(){
  updateChart();
  updateTable();
}

/**
* Updates the Chart.js chart data by reading data from the endpoint
*/
function updateChart(){
  api_string = getAPIString();

  $.getJSON(api_string, function(data){
    document.getElementById("average_score").innerHTML = "<strong>Average Score: " + data.average + "</strong>"
    myLineChart.data.datasets[0].data = data.scores;
    myLineChart.data.labels = data.labels;
    myLineChart.update();
    document.getElementById('chart-updated').innerHTML = "Updated " + new Date();
  });
}

/**
* Updates the DataTable table by reading data from the endpoint and reloading the DataTable ajax url
*/
function updateTable(api_string){
  api_string = getAPIString();
  myDataTable.ajax.url(api_string).load();
  document.getElementById('table-updated').innerHTML = "Updated " + new Date();
}

/**
* Obtains selector data from the endpoint and populates the select with options according to the current mode (ie Staff or Menu)
*/
function populateListItems(){
  $.getJSON('/api/reporting/list_items', function(data){
    document.getElementById('item-selector').innerHTML = "";
    $.each(data[mode.toLowerCase()], function(k, v){
      document.getElementById('item-selector').innerHTML += "<option value='" + v.value + "'>" + v.name + "</option>";
    });
  });
}

/**
* Changes the Graph mode to view different satisfaction visualisations (ie Customer, Staff, Menu)
*/
function changeGraphMode(elem){
  mode = elem.name;
  document.getElementById("graph_title").innerHTML = elem.name + " Satisfaction Graph";
  if (elem.name == "Menu"){
    document.getElementById('table-changable-head').innerHTML = "Quantity";
    document.getElementById('table-changable-foot').innerHTML = "Quantity";
  } else {
    document.getElementById('table-changable-head').innerHTML = "Event Description";
    document.getElementById('table-changable-foot').innerHTML = "Event Description";
  }
  if (elem.name == "Customer"){
    document.getElementById('item-selector-area').style.display = "none";
  } else {
    document.getElementById('item-selector-area').style.display = "block";
    document.getElementById('item-select-label').innerHTML = elem.name + " ID";
    populateListItems();
  }
  updateAll();
}
