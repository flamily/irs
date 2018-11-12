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

  var pageElement;

  var photoCallback = function updatePhotoField(encodedImage){
    $("#customerImg").val(encodedImage);

    $.ajax({
      url: pageElement[0].getAttribute('formaction'),
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

  }

  $('#updateTable').find('input').click(function(event){
    event.preventDefault();

    if($(this).val() == 'Pay'){
      pageElement = $(this);
      irs.photo(photoCallback);
    }
    else{
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
    }

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
        $(element).children('p').first().text('available');
        $(element).data('status', 'available');
        break;

      case 'unavailable':
        $(element).addClass('unavailable-table');
        $(element).children('p').first().text('unavailable');
        $(element).data('status', 'unavailable');
        break;
    }
  }
  // End Exit Interface


  $(document).find('.btn-select-pad').click(function() {
    var size = document.getElementsByName('partySize')[0].value;
    if(size > 10){
      $(document).find('#confirmPartySize').prop('disabled', true);
      $('.seatingDisclaimer').addClass('text-danger');
      $('.seatingDisclaimer').text(
        'Max number of people our Restaurant can seat is 10'
        );
    }
    else if(size < 1){
      $(document).find('#confirmPartySize').prop('disabled', true);
      $('.seatingDisclaimer').addClass('text-danger');
      $('.seatingDisclaimer').text(
        'Please select a number greater than 0. Our restaurant can seat a maximum of 10 people.'
        );
    }
    else{
      $(document).find('#confirmPartySize').prop('disabled', false);
      $('.seatingDisclaimer').removeClass('text-danger');
      $('.seatingDisclaimer').text(
        'Max number of people our Restaurant can seat is 10'
        );
    }
  });

  $(document).find('#confirmPartySize').click(function() {
    var size = document.getElementsByName('partySize')[0].value;
    if (size == ""){
      event.preventDefault();
      $(document).find('#confirmPartySize').prop('disabled', true);
      $('.seatingDisclaimer').addClass('text-danger');
      $('.seatingDisclaimer').text(
        'Number can\'t be blank please enter a number. Our restaurant can seat a maximum of 10 people.'
        );
    }
    $('.modal-body').text(
      'You are confirming a table for ' + size +
      ' people. Please select confirm to continue or cancel to enter again.'
      );
  });

  //Robot Photo
  var robotInputElement;

  $('.robotTableReserve').children('input:submit').click(function(event){
    event.preventDefault();
    robotInputElement = $(this);
    irs.photo(robotPhotoCallback);
  });

  var robotPhotoCallback = function updatePhotoField(encodedImage){
    robotInputElement.siblings('.customerImg').val(encodedImage);
    robotInputElement.parent().submit();
  }

  /********************************
    * START
    * Robot photo
  ********************************/


  if(window.location.pathname.includes('robot')){
    // Standard commands
    // Accept trigger words
    var triggerWords = ['confirm', 'confirmed', 'yes'];
    // Cancel trigger words
    triggerWords = $.merge(triggerWords, ['no', 'cancel']);
    // Back to start trigger words
    triggerWords = $.merge(triggerWords, ['restart', 'back', 'over', 'exit', 'quit']);
    // Numbers for table selection
    triggerWords = $.merge(triggerWords, ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']);
    triggerWords = $.merge(triggerWords, ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']);

    /********************************
     * START
     * Robot photo callbacks and handlers
    ********************************/
    var partyCallback = function(matchedIndex){
      if(matchedIndex != -1){

        var recognisedWord = triggerWords[matchedIndex];

        handleGenericCommands(recognisedWord);

        if(!parseInt(recognisedWord))
          recognisedWord = wordToNumber(recognisedWord)

        $("[name=partySize]").val(recognisedWord);
        $(document).find('#confirmPartySize').click();

        // Handle Modal
        irs.say('Do you want to confirm this or cancel?');
        setTimeout(function(){irs.listen(triggerWords, 10000, modalCallback)}, 3000);
      }
      // Re run voice
      else{
        irs.say("Please enter or say how many people you wish to seat, the max we seat is 10");
        setTimeout(function(){irs.listen(triggerWords, 10000, partyCallback)}, 6000);
      }

    };

    var modalCallback = function(matchedIndex){
      if(matchedIndex != -1){
        var recognisedWord = triggerWords[matchedIndex];

        handleGenericCommands(recognisedWord);

        switch(recognisedWord){
          case 'cancel':
          case 'no':
            $("[data-dismiss='modal']").first().click();
            irs.say("Please enter or say how many people you wish to seat, the max we seat is 10");
            setTimeout(function(){irs.listen(triggerWords, 10000, partyCallback)}, 6000);
            break;
          case 'confirm':
          case 'confirmed':
          case 'yes':
            $($("#findAvailableTables")[0]).trigger('click');
            break;
        }
      }
      // Rerun voice
      else{
        irs.say('Do you want to confirm this or cancel?');
        setTimeout(function(){irs.listen(triggerWords, 10000, modalCallback)}, 3000);
      }
    };

    var tableCallback = function(matchedIndex){
      if(matchedIndex != -1){
        var recognisedWord = triggerWords[matchedIndex];

        handleGenericCommands(recognisedWord);

        if(!parseInt(recognisedWord))
          recognisedWord = wordToNumber(recognisedWord);

        if(!$($("[value='" + recognisedWord + "']")[0]).siblings('button:submit').prop('disabled'))
          $($("[value=" + recognisedWord + "]")[0]).parent().submit();
        else
          irs.say("Table is taken, please select another");
      }
      else 
        irs.say("Please tap a table or say the table number");
      // Rerun voice
      setTimeout(function(){irs.listen(triggerWords, 10000, tableCallback)}, 3000);
    };

    var proceedCallback = function(matchedIndex){
      if(matchedIndex != -1){
        var recognisedWord = triggerWords[matchedIndex];

        handleGenericCommands(recognisedWord);
      }
      // Rerun voice
      else
        irs.listen(triggerWords, 10000, proceedCallback);
    };


    function handleGenericCommands(word){
      switch(word){
        case 'restart':
        // Case for 'start over'
        case 'over':
        case 'exit':
        case 'quit':
           window.location.replace("/robot");
          break;
        case 'back':
          window.history.back();
        default:
        break;
      };
    }
    /********************************
     * END
     * Robot photo callbacks and handlers
    ********************************/


    // Extremely primitive word to number implementation
    function wordToNumber(numberString){
      var numberMap = new Map();

      numberMap.set("one", 1);
      numberMap.set("two", 2);
      numberMap.set("three", 3);
      numberMap.set("four", 4);
      numberMap.set("five", 5);
      numberMap.set("six", 6);
      numberMap.set("seven", 7);
      numberMap.set("eight", 8);
      numberMap.set("nine", 9);
      numberMap.set("ten", 10);

      return numberMap.get(numberString);
    }

    // Actually do something
    if(window.location.pathname.includes('/party')){
      irs.say("Please enter or say how many people you wish to seat, the max we seat is 10");
      setTimeout(function(){irs.listen(triggerWords, 10000, partyCallback)}, 6000);
    }
    else if(window.location.pathname.includes('/table')){
      irs.say("Please tap a table or say the table number");
      setTimeout(function(){irs.listen(triggerWords, 10000, tableCallback)}, 3000);
    }
    else if(window.location.pathname.includes('/proceed')){
      irs.say("Your table is now ready for you");
      setTimeout(function(){irs.listen(triggerWords, 10000, proceedCallback)}, 3000);
    }
    else if(window.location.pathname.includes('/full')){
      irs.say("Sorry, all the tables are taken");
    }
  }

  /********************************
    * END
    * Robot photo
  ********************************/
})(jQuery); // End of use strict
