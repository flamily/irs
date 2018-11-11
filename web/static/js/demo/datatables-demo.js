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
  myDataTable = $('#dataTable').DataTable({
    ajax: {
      url: '/api/reporting/date?dateString=2018-11-08',
      method: "GET",
      xhrFields: {
        withCredentials: true
      }
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
} );
