(function($) {
  "use strict"; // Start of use strict

  // Toggle the side navigation
  $("#sidebarToggle").on('click',function(e) {
    e.preventDefault();
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Scroll to top button appear
  $(document).on('scroll',function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function(event) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    event.preventDefault();
  });

  // Build query string
  $(document).find('#findAvailableTables').click(function() {
    var size = document.getElementsByName('partySize')[0].value;
    document.location = "/robot/table?people=" + size
  });

  $('#table-layout').find('button').click(function(){
    $('#statusModal').modal('show');
    $('#modalTableNumber').text($(this).data('tableid'));
    $('#tableId').val($(this).data('tableid'));
  });

<<<<<<< HEAD
  $(document).find('#confirmPartySize').click(function() {
    var size = document.getElementsByName('partySize')[0].value
    $('.modal-body').text('You are confirming a table for ' + size + ' people. Please select confirm to continue or cancel to enter again.')
  });
=======
  var photoCallback = function updatePhotoField(encodedImage){
    $("#customerImg").val(encodedImage);
  }

  $('#updateTable').find('input').click(function(event){
    event.preventDefault();

    if($(this).val() == 'Pay')
      irs.photo(photoCallback);

    $.ajax({
      url: $(this)[0].getAttribute('formaction'),
      data: $('#tableInfo').serialize(),
      type: 'POST',
      success: function(response) {
        updateTableStatuses(response);
      },
      error: function(error) {
        console.log('Something went wrong');
      }
    });
    // Clear out image field to prevent issues with other buttons
    $("#customerImg").val('');
  });

  function updateTableStatuses(response){
    var className;
    var element = $("[data-tableId=" + $('#tableId').val() +"]")[0];
    switch(response.status){
      case 'available':
        $(element).removeClass('unavailable-table');
        $(element).addClass('available-table');
        break;

      case 'unavailable':
        $(element).removeClass('available-table');
        $(element).addClass('unavailable-table');
        break;
    }
  }

>>>>>>> master
})(jQuery); // End of use strict
