$(window).on('load', function(){
     $('.loader').fadeOut();
     AOS.init({
  duration: 1200,
  once: true
})
});

 luxy.init({
      wrapper: '#luxy',
      targets : '.luxy-el',
      wrapperSpeed:  0.08,
    });