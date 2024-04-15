$(document).ready(function($) {




// scroll functions
$(window).scroll(function(e) {

    // add/remove class to navbar when scrolling to hide/show
    var scroll = $(window).scrollTop();
    if (scroll >= 50) {
        $('.navbar').addClass("sticky");
    } else {
        $('.navbar').removeClass("sticky");
           $('.navbar-toggler').click(function (){
          $('.navbar').addClass('sticky');
       });
    }

});




$(".cart-nav").click(function(){
  $(".cart-info").toggleClass("visible");
});

$(".s_toggle").click(function(){
	event.preventDefault()
  $(".search_toggle").toggleClass("visible");
});


var btn = $('#backtotop');

$(window).scroll(function() {
  if ($(window).scrollTop() > 300) {
    btn.addClass('show');
  } else {
    btn.removeClass('show');
  }
});

btn.on('click', function(e) {
  e.preventDefault();
  $('html, body').animate({scrollTop:0}, '300');
});



// Video Script Starts

jQuery('.play i').click(function(event){
     event.preventDefault();
    //var url = $(this).html(); //this will not work  
     $(".js-video").append('<iframe width="80%" height="500" src="https://www.youtube.com/embed/HgvIox6ehkM?autoplay=1" frameborder="0" allowfullscreen></iframe>');
    $(this).hide();
    //$('video-poster').css('z-index','-1');
    
  });

// Video Script Ends

	
});