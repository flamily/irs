/**
* All functions for html generation & endpoint data calls to create a seemless, one page dashboard solution
*
* Author: Jacob Vorreiter
* Date: 12/11/2018
*/

var myDataTable;

$(document).ready(function() {
  var latest_time = "";
  $.getJSON('/api/time/get_latest', callback_func);

  /**
  * Initialises data table with data retrieved from the endpoint call using a callback,
  * allowing for seamless laoding. Additionally, Populates the year options and calls the updateChart method

  @param {JSON} data received from the getJSON callback.
  */
  function callback_func(data){
    latest_time = data.data;
    var today_dt = latest_time;
    var api_string = '/api/reporting/Customer/date?dateString=' + latest_time;
    $('#date-picker').val(today_dt);

    myDataTable = $('#dataTable').DataTable({
      ajax: {
        url: '/api/reporting/Customer/date?dateString=2018-11-11',
      },
      columns: [
        { data: "date",
          render: function(data, type, row){
            return new Date(data);
          }
        },
        { data: 'description' },
        { data: 'table_id' },
        { data: 'staff_id' },
        { data: 'reservation_id' },
        { data: 'score' }
      ]
    });
    populateYearOptions();
    updateChart();
  }
} );
