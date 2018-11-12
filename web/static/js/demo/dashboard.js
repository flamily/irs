var options = "";
var mode = "Customer";

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

function changeDatePicker(inputType){
  var decoration = "id='date-picker' class='form-control form-control-sm' onchange='updateAll()'";
  if (inputType == "year"){
    var selector = document.getElementById("date-picker-module");
    selector.innerHTML = "<select name='year'" + decoration + ">" + options + "</select>";
  } else {
    document.getElementById("date-picker-module").innerHTML = "<input name='" + inputType + "' type=" + inputType + " " + decoration + ">";
  }
}

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

function updateAll(){
  updateChart();
  updateTable();
}

function updateChart(){
  api_string = getAPIString();

  $.getJSON(api_string, function(data){
    document.getElementById("average_score").innerHTML = "<strong>Average Score: " + data.average + "</strong>"
    myLineChart.data.datasets[0].data = data.scores;
    myLineChart.data.labels = data.labels;
    myLineChart.update();
  });
}

function updateTable(api_string){
  api_string = getAPIString();

  myDataTable.ajax.url(api_string).load();
}

function populateListItems(){
  $.getJSON('/api/reporting/list_items', function(data){
    document.getElementById('item-selector').innerHTML = "";
    $.each(data[mode.toLowerCase()], function(k, v){
      document.getElementById('item-selector').innerHTML += "<option value='" + v.value + "'>" + v.name + "</option>";
    });
  });
}

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
