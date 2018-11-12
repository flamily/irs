// Call the dataTables jQuery plugin
var myDataTable;

var dateFormatOptions = {
  weekday: 'long',
  year: 'numeric',
  month: 'short',
  day: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
  timeZone: 'GMT'
}

$(document).ready(function() {
  var latest_time = "";
  $.getJSON('/api/time/get_latest', callback_func);

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
