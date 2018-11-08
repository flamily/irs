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

  // Start Exit Interface
  function disableModalButtons(){
    $('#updateTable').find('input').each(function(){
     $(this).prop("disabled", true);
    });
  }

  function enableAppropriateModalButtons(tableStatus){
    switch(tableStatus){
      case 'occupied':
        $("[value='Pay']").first().prop("disabled", false);
        break;

      case 'available':
        $("[value='Maintain']").first().prop("disabled", false);
        break;

      case 'unavailable':
        $("[value='Ready']").first().prop("disabled", false);
        break;
    }
  }

  $('#table-layout').find('button').click(function(){
    disableModalButtons();
    enableAppropriateModalButtons($(this).data('status'));
    $('#statusModal').modal('show');
    $('#modalTableNumber').text($(this).data('tableid'));
    $('#tableId').val($(this).data('tableid'));
  });

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
        $('#statusModal').modal('hide');
      },
      error: function(error) {
        console.log(error.statusText);
      }
    });
    // Clear out image field to prevent issues with other buttons
    $("#customerImg").val('');
  });

  function removeTableStatusClasses(element){
    $(element).removeClass('available-table');
    $(element).removeClass('unavailable-table');
    $(element).removeClass('occupied-table');
  }

  function updateTableStatuses(response){
    var className;
    var element = $("[data-tableId=" + $('#tableId').val() +"]")[0];
    removeTableStatusClasses(element);
    switch(response.status){
      case 'available':
        $(element).addClass('available-table');
        $(element).data('status', 'available')
        break;

      case 'unavailable':
        $(element).addClass('unavailable-table');
        $(element).data('status', 'unavailable')
        break;
    }
  }
  // End Exit Interface

  $(document).find('#confirmPartySize').click(function() {
    var size = document.getElementsByName('partySize')[0].value
    $('.modal-body').text('You are confirming a table for ' + size + ' people. Please select confirm to continue or cancel to enter again.')
  });

  // Robot Photo
  var photoCallback = function updatePhotoField(encodedImage){
    $("#customerPhoto").val(encodedImage);
  }

  $('#robotTableReserve').find('input').click(function(event){
    event.preventDefault();
    irs.photo(photoCallback);

    // Clear out image field to prevent issues with other buttons
    $("#customerImg").val('');
  });
  // Robot Photo
})(jQuery); // End of use strict
