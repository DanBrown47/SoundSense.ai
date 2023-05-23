var THEMEIM = THEMEIM || {};

(function($) {

  /*!----------------------------------------------
  # This beautiful code written with heart
  # by Aminul Islam <mominul@themeim.com>
  # In Dhaka, BD at the Themeim Themes workstation.
  ---------------------------------------------*/

  // USE STRICT
  "use strict";

  THEMEIM.initialize = {

    init: function() {
      THEMEIM.initialize.general();
      THEMEIM.initialize.sectionBackground();
      THEMEIM.initialize.countDown();
      THEMEIM.initialize.portfolio();
      THEMEIM.initialize.contactForm();
      THEMEIM.initialize.mobileMenu();
    },


    /*=======================================================*/
    /*=           Collection of snippet and tweaks          =*/
    /*=======================================================*/

    general: function() {
        
    //      // block f12 inspect
    //     $(document).keydown(function(e){
    //     if(e.which === 123){
     
    //       return false;
     
    //     }
     
    // });
    //   // block right click
    //     $(document).bind("contextmenu",function(e) { 
    // 	e.preventDefault();
     
    // });
    
    // // block  ctrl u 
    // document.onkeydown = function(e) {
    //     if (e.ctrlKey && 
    //         (e.keyCode === 67 || 
    //          e.keyCode === 86 || 
    //          e.keyCode === 85 || 
    //          e.keyCode === 117)) {
    //         alert('not allowed');
    //         return false;
    //     } else {
    //         return true;
    //     }
        
    // };


      // Convert Image to SVG
      $('img.svg').each(function() {
        var $img = $(this),
          imgID = $img.attr('id'),
          imgClass = $img.attr('class'),
          imgURL = $img.attr('src');

        $.get(imgURL, function(data) {
          // Get the SVG tag, ignore the rest
          var $svg = $(data).find('svg');

          // Add replaced image's ID to the new SVG
          if (typeof imgID !== 'undefined') {
            $svg = $svg.attr('id', imgID);
          }
          // Add replaced image's classes to the new SVG
          if (typeof imgClass !== 'undefined') {
            $svg = $svg.attr('class', imgClass);
          }

          // Remove any invalid XML tags as per http://validator.w3.org
          $svg = $svg.removeAttr('xmlns:a');

          // Replace image with new SVG
          $img.replaceWith($svg);
        }, 'xml');
      });








      /*Smoke start------*/
      $('.smoke-wrqpper').each(function() {

        var smokemachine = function(context, color) {
          color = color || [255, 255, 255]
          var polyfillAnimFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame ||
            window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;
          var lastframe;
          var currentparticles = []
          var pendingparticles = []

          var buffer = document.createElement('canvas'),
            bctx = buffer.getContext('2d')

          buffer.width = 20
          buffer.height = 20

          var opacities = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 5, 5, 7, 4, 4, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 17, 27, 41, 52, 56, 34, 23, 15, 11, 4, 9, 5, 1, 0, 0, 0, 0, 0, 0, 1, 45, 63, 57, 45, 78, 66, 52, 41, 34, 37, 23, 20, 0, 1, 0, 0, 0, 0, 1, 43, 62, 66, 64, 67, 115, 112, 114, 56, 58, 47, 33, 18, 12, 10, 0, 0, 0, 0, 39, 50, 63, 76, 87, 107, 105, 112, 128, 104, 69, 64, 29, 18, 21, 15, 0, 0, 0, 7, 42, 52, 85, 91, 103, 126, 153, 128, 124, 82, 57, 52, 52, 24, 1, 0, 0, 0, 2, 17, 41, 67, 84, 100, 122, 136, 159, 127, 78, 69, 60, 50, 47, 25, 7, 1, 0, 0, 0, 34, 33, 66, 82, 113, 138, 149, 168, 175, 82, 142, 133, 70, 62, 41, 25, 6, 0, 0, 0, 18, 39, 55, 113, 111, 137, 141, 139, 141, 128, 102, 130, 90, 96, 65, 37, 0, 0, 0, 2, 15, 27, 71, 104, 129, 129, 158, 140, 154, 146, 150, 131, 92, 100, 67, 26, 3, 0, 0, 0, 0, 46, 73, 104, 124, 145, 135, 122, 107, 120, 122, 101, 98, 96, 35, 38, 7, 2, 0, 0, 0, 50, 58, 91, 124, 127, 139, 118, 121, 177, 156, 88, 90, 88, 28, 43, 3, 0, 0, 0, 0, 30, 62, 68, 91, 83, 117, 89, 139, 139, 99, 105, 77, 32, 1, 1, 0, 0, 0, 0, 0, 16, 21, 8, 45, 101, 125, 118, 87, 110, 86, 64, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 28, 79, 79, 117, 122, 88, 84, 54, 46, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 6, 55, 61, 68, 71, 30, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 23, 25, 20, 12, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 12, 9, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0]

          var data = bctx.createImageData(20, 20)
          var d = data.data

          for (var i = 0; i < d.length; i += 4) {
            d[i] = color[0]
            d[i + 1] = color[1]
            d[i + 2] = color[2]
            d[i + 3] = opacities[i / 4]
          }

          bctx.putImageData(data, 0, 0)

          var imagewidth = 20 * 5
          var imageheight = 20 * 5

          function particle(x, y, l) {
            this.x = x
            this.y = y
            this.age = 0
            this.vx = (Math.random() * 8 - 4) / 100
            this.startvy = -(Math.random() * 30 + 10) / 100
            this.vy = this.startvy
            this.scale = Math.random() * .5
            this.lifetime = Math.random() * l + l / 2
            this.finalscale = 5 + this.scale + Math.random()

            this.update = function(deltatime) {
              this.x += this.vx * deltatime
              this.y += this.vy * deltatime
              var frac = Math.pow((this.age) / this.lifetime, .5)
              this.vy = (1 - frac) * this.startvy
              this.age += deltatime
              this.scale = frac * this.finalscale
            }

            this.draw = function() {
              context.globalAlpha = (1 - Math.abs(1 - 2 * (this.age) / this.lifetime)) / 8
              var off = this.scale * imagewidth / 2
              var xmin = this.x - off
              var xmax = xmin + this.scale * imageheight
              var ymin = this.y - off
              var ymax = ymin + this.scale * imageheight
              context.drawImage(buffer, xmin, ymin, xmax - xmin, ymax - ymin)
            }
          }


          function addparticles(x, y, n, lifetime) {
            lifetime = lifetime || 4000
            n = n || 10
            if (n < 1) return Math.random() <= n && pendingparticles.push(new particle(x, y, lifetime));
            for (var i = 0; i < n; i++) {
              pendingparticles.push(new particle(x, y, lifetime))
            };
          }

          function updateanddrawparticles(deltatime) {
            context.clearRect(0, 0, canvas.width, canvas.height);
            deltatime = deltatime || 16
            var newparticles = []
            currentparticles = currentparticles.concat(pendingparticles)
            pendingparticles = []

            currentparticles.forEach(function(p) {
              p.update(deltatime)
              if (p.age < p.lifetime) {
                p.draw()
                newparticles.push(p)
              }
            })
            currentparticles = newparticles
          }

          function frame(time) {
            if (running) {
              var deltat = time - lastframe
              lastframe = time;

              updateanddrawparticles(deltat)

              polyfillAnimFrame(frame)
            }
          }

          var running = false

          function start() {
            running = true
            polyfillAnimFrame(function(time) {
              lastframe = time
              polyfillAnimFrame(frame)
            })
          }

          function stop() {
            running = false
          }

          return {
            start: start,
            stop: stop,
            step: updateanddrawparticles,
            addsmoke: addparticles
          }

        }



        var canvas = document.getElementById('canvas')
        var ctx = canvas.getContext('2d')
        canvas.width = innerWidth
        canvas.height = innerHeight

        var party = smokemachine(ctx, [255, 255, 255])
        party.start() // start animating

        onmousemove = function(e) {
          var x = e.clientX
          var y = e.clientY
          var n = .5
          var t = Math.floor(Math.random() * 200) + 3800
          party.addsmoke(x, y, n, t)
        }

        setInterval(function() {
          party.addsmoke(innerWidth / 4, innerHeight, 3)
        }, 100)



      });



      /*Smoke end*/









      /*=========================================*/
      /*=           Magic line       				=*/
      /*=========================================*/




      $('#header-menu-magic-line').each(function() {


        var $el, leftPos, newWidth,
          $mainNav = $("#header-menu-magic-line");

        $mainNav.append("<li id='magic-line'></li>");
        var $magicLine = $("#magic-line");

        $magicLine
          .width($(".current_page_item").width())
          .css("left", $(".current_page_item a").position().left - 20)
          .data("origLeft", $magicLine.position().left)
          .data("origWidth", $magicLine.width());

        $("#header-menu-magic-line > li > a").hover(function() {
          $el = $(this);
          leftPos = $el.position().left - 20;
          newWidth = $el.parent().width();
          $magicLine.stop().animate({
            left: leftPos,
            width: newWidth
          });
        }, function() {
          $magicLine.stop().animate({
            left: $magicLine.data("origLeft"),
            width: $magicLine.data("origWidth")
          });
        });

      });









      $('.swiper-container').each(function() {
        new SwiperRunner($(this));
      });


      $('.popup-video-btn').magnificPopup({
        type: 'iframe'
      });

      /* Magnefic Popup */
      $('.popup-modal').magnificPopup({
        type: 'image',
        mainClass: 'mfp-with-zoom'
      });

      /* Quantity Count */
      (function() {

        return $(".minus,.plus").click(function(e) {
          var inc_dec, qty;
          inc_dec = $(this).hasClass("minus") ? -1 : 1;
          qty = $("[name=quantity]");
          return qty.val(parseInt(qty.val()) + inc_dec);
        });

      }).call(this);

      /* Product Price Filter */
      $("#slider-range").slider({
        range: true,
        min: 50,
        max: 650,
        values: [200, 400],
        slide: function(event, ui) {
          $("#amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
        }
      });
      $("#amount").val("$" + $("#slider-range").slider("values", 0) +
        " - $" + $("#slider-range").slider("values", 1));


      var obj = new SwiperRunner('.gallery-top');

      // The setNav method will make link to main carousel.
      obj.setNav('.gallery-thumbs');

      $('.collapse').on('show.bs.show', function() {
        $(this).siblings('.card-header').addClass('active');
      });

      $('.collapse').on('hide.bs.show', function() {
        $(this).siblings('.card-header').removeClass('active');
      });


      // Open Close PlayList
      $('#playlist-toggle').on('click', function(e) {
        e.preventDefault();
        $(this).toggleClass('close-icon');
        $('#header_player').find(".jp-playlist").fadeToggle(100);

      });

      /* Product Grid and List View */
      var $vw_prod = $('.tim-product-btn-vw');

      if ($vw_prod.length) {
        var $control = $($vw_prod.attr('data-control')),
          $input = $vw_prod.find('input');

        $input.on('change', function() {
          $control.addClass('tim-loading');

          var $this = $(this);

          $input.each(function() {
            var view = $(this).attr('data-view-class');

            $control.removeClass(view);
          });

          $control.addClass($this.attr('data-view-class'));

          $control.removeClass('tim-loading');
        });
      }

      /* Quick View Popup */
      $('.trigger').on('click', function(e) {
        e.preventDefault();
        var mask = '<div class="mask-overlay">';

        $('.quickview-wrapper').toggleClass('open');
        $(mask).hide().appendTo('body').fadeIn('fast');
        $('.mask-overlay, .close-menu').on('click', function() {
          $('.quickview-wrapper').removeClass('open');
          $('.mask-overlay').remove();
        });
      });

      /* Quick View Popup */
      $('.off-opener').on('click', function(e) {
        e.preventDefault();


        $('.offset-menu').addClass('open');
        $('.offset-closer').on('click', function() {
          $('.offset-menu').removeClass('open');
        });

        $('.offset-menu-two').addClass('open');
        $('.offset-closer').on('click', function() {
          $('.offset-menu-two').removeClass('open');
        });
      });




      $('.latest-album-btn .sm2_button').on('click', function() {

        setTimeout(function() {
          $(".player-main").toggleClass("active");
          $(".bubble-wrap").toggleClass("active");
          $(".bubble-wrap-right").toggleClass("active");
          $(".sm2_button").toggleClass("active");


        }, 500);

        $(".record-key").toggleClass("active");

      });


      $('.jp-play').on('click', function() {

        $(".jp-type-playlist").toggleClass("active");

      });



      /*=========================================*/
      /*=           Search toggle class        =*/
      /*=========================================*/

      $(".search-trigger").on('click', function() {
        $(".search-input-wrapper").toggleClass("active");
      });

      /* Rating Star */
      $('.rating li').on('click', function() {
        var selectedCssClass = 'selected';
        var $this = $(this);
        $this.siblings('.' + selectedCssClass).removeClass(selectedCssClass);
        $this
          .addClass(selectedCssClass)
          .parent().addClass('vote-cast');
      });

      /* Product View Slider */

      //Product Single
      $('.slider-for').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: '.slider-nav',
        swipe: false,
      });

      $('.slider-nav').slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        asNavFor: '.slider-for',
        focusOnSelect: true,
        swipe: false,
        infinite: false
      });

      //Product Quick View Slider
      $('.slider-for1').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: '.slider-nav1',
        swipe: false,
      });

      $('.slider-nav1').slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        asNavFor: '.slider-for1',
        focusOnSelect: true,
        swipe: false,
        infinite: false
      });


      $('.banner-five').each(function() {

        var scene = document.getElementById('paralax-1');
        var parallax = new Parallax(scene);

      });




      /* Top Fixed Menu Init */
      var myElement = document.querySelector("header");
      var headroom = new Headroom(myElement);

      headroom.init({
        offset: 200,
        tolerance: {
          up: 5,
          down: 5
        },

        classes: {
          top: "headroom--top"

        }
      });

      /* Top Fixed Menu Init */
      var myElement = document.querySelector("#mobile-nav-wrap");
      var headroom = new Headroom(myElement);

      headroom.init({
        offset: 200,
        tolerance: {
          up: 5,
          down: 5
        },

        classes: {
          top: "headroom--top"

        }
      });


      soundManager.setup({

      });

      /* Plalist Active */

      $(document).on('click', '.sm2_button', function(e) {
        e && e.preventDefault();
        var $this = $(e.target);
        if (!$this.is('a')) $this = $this.closest('a');

        $('.sm2_button').not($this).removeClass('active');
        $('.sm2_button').parent('li').not($this.parent('li')).removeClass('active');

        $this.toggleClass('active');
        $this.parent('li').toggleClass('active');

      });

      // $(".content-three h2").fitText(1.2, {
      // 	minFontSize: '20px',
      // 	maxFontSize: '60px'
      // });


      var backtotop = $(".backtotop");

      var windo = $(window),
        HtmlBody = $('html, body');

      backtotop.on('click', function() {
        HtmlBody.animate({
          scrollTop: 0
        }, 1500);
      });

      /*==================================*/
      /*=           Mobile Menu          =*/
      /*==================================*/
      $('.gmap3-area').each(function() {
        var $this = $(this),
          key = $this.data('key'),
          lat = $this.data('lat'),
          lng = $this.data('lng'),
          mrkr = $this.data('mrkr');

        $this.gmap3({
            center: [lat, lng],
            zoom: 16,
            scrollwheel: false,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            style: [{
              "featureType": "poi.business",
              "elementType": "all",
              "stylers": [{
                "hue": "#ff00ca"
              }, {
                "saturation": "100"
              }, {
                "lightness": "0"
              }, {
                "gamma": "1"
              }]
            }, {
              "featureType": "poi.business",
              "elementType": "labels.icon",
              "stylers": [{
                "hue": "#ff0000"
              }]
            }]
          })
          .marker(function(map) {
            return {
              position: map.getCenter(),
              icon: mrkr
            };
          })

      });


    },

    /*==================================*/
    /*=           Mobile Menu          =*/
    /*==================================*/

    mobileMenu: function() {

      var Accordion = function(el, multiple) {
        this.el = el || {};

        this.multiple = multiple || false;

        var dropdownlink = this.el.find('.dropdownlink');
        dropdownlink.on('click', {
            el: this.el,
            multiple: this.multiple
          },
          this.dropdown);
      };

      Accordion.prototype.dropdown = function(e) {
        e.preventDefault();
        var $el = e.data.el,
          $this = $(this),

          $next = $this.next();

        $next.slideToggle();
        $this.parent().toggleClass('open');

        if (!e.data.multiple) {
          //show only one menu at the same time
          $el.find('.submenuItems').not($next).slideUp().parent().removeClass('open');
        }
      }

      var accordion = new Accordion($('.accordion-menu'), false);

      $('.toggle-inner').on('click', function(e) {
        e.preventDefault();
        var mask = '<div class="mask-overlay">';

        $('body').toggleClass('active');
        $(mask).hide().appendTo('body').fadeIn('fast');
        $('.mask-overlay, .close-menu').on('click', function() {
          $('body').removeClass('active');
          $('.mask-overlay').remove();
        });
      });
    },






    /*=========================================*/
    /*=           Section Background          =*/
    /*=========================================*/

    sectionBackground: function() {

      // Section Background Image
      $('[data-bg-image]').each(function() {
        var img = $(this).data('bg-image');
        $(this).css({
          backgroundImage: 'url(' + img + ')',
        });
      });

      //Parallax Background
      $('[data-parallax="image"]').each(function() {

        var actualHeight = $(this).position().top;
        var speed = $(this).data('parallax-speed');
        var reSize = actualHeight - $(window).scrollTop();
        var makeParallax = -(reSize / 2);
        var posValue = makeParallax + "px";

        $(this).css({
          backgroundPosition: '50% ' + posValue,
        });
      });
    },

    /*=================================*/
    /*=           Count Down          =*/
    /*=================================*/

    countDown: function() {
      $('.countdown').each(function(index, value) {
        var count_year = $(this).attr("data-count-year");
        var count_month = $(this).attr("data-count-month");
        var count_day = $(this).attr("data-count-day");
        var count_date = count_year + '/' + count_month + '/' + count_day;
        $(this).countdown(count_date, function(event) {
          $(this).html(
            event.strftime('<span class="CountdownContent">%D<span class="CountdownLabel">Days</span></span><span class="CountdownSeparator"></span><span class="CountdownContent">%H <span class="CountdownLabel">Hours</span></span><span class="CountdownSeparator"></span><span class="CountdownContent">%M <span class="CountdownLabel">Minutes</span></span><span class="CountdownSeparator"></span><span class="CountdownContent">%S <span class="CountdownLabel">Seconds</span></span>')
          );
        });
      });
    },


    /*========================================*/
    /*=          Portfolio Masonrty          =*/
    /*========================================*/

    portfolio: function() {

      $('.tim-container').imagesLoaded(function() {

        var $container = $('.tim-filter-items');

        // init Isotope
        var $grid = $('.grid').isotope({
          itemSelector: '.grid-item',
          percentPosition: true,
          masonry: {
            columnWidth: '.grid-sizer'
          }
        });


        // layout Isotope after each image loads
        // $grid.imagesLoaded().progress(function() {
        // 	$grid.isotope('layout');
        // });

        // filter items when filter link is clicked
        $('.tim-isotope-filter a').on('click', function() {
          var selector = $(this).attr('data-filter');
          $container.isotope({
            filter: selector
          });
          return false;
        });

        $('.tim-isotope-filter a').on('click', function() {
          $('.tim-isotope-filter').find('.current').removeClass('current');
          $(this).parent().addClass('current');
        });
      });
    },

    /*===================================*/
    /*=           Contact Form          =*/
    /*===================================*/

    contactForm: function() {
      $('[data-deventform]').each(function() {
        var $this = $(this);
        $('.form-result', $this).css('display', 'none');

        $this.submit(function() {

          $('button[type="submit"]', $this).addClass('clicked');

          // Create a object and assign all fields name and value.
          var values = {};

          $('[name]', $this).each(function() {
            var $this = $(this),
              $name = $this.attr('name'),
              $value = $this.val();
            values[$name] = $value;
          });

          // Make Request
          $.ajax({
            url: $this.attr('action'),
            type: 'POST',
            data: values,
            success: function success(data) {
              if (data.error == true) {
                $('.form-result', $this).addClass('alert-warning').removeClass('alert-success alert-danger').css('display', 'block');
              } else {
                $('.form-result', $this).addClass('alert-success').removeClass('alert-warning alert-danger').css('display', 'block');
              }
              $('.form-result > .content', $this).html(data.message);
              $('button[type="submit"]', $this).removeClass('clicked');
            },
            error: function error() {
              $('.form-result', $this).addClass('alert-danger').removeClass('alert-warning alert-success').css('display', 'block');
              $('.form-result > .content', $this).html('Sorry, an error occurred.');
              $('button[type="submit"]', $this).removeClass('clicked');
            }
          });
          return false;
        });

      });
    }
  };

  THEMEIM.documentOnReady = {
    init: function() {
      THEMEIM.initialize.init();

      if (!$('.sm2_button').hasClass('sm2_playing')) {
        $('.bubble-wrap').removeClass('active');

      }

    },
  };

  THEMEIM.documentOnLoad = {
    init: function() {
      // THEMEIM.initialize.init();

      $('.loader').delay(2000).fadeOut(1000);
    },
  };

  THEMEIM.documentOnResize = {
    init: function() {


    },
  };

  THEMEIM.documentOnScroll = {
    init: function() {
      THEMEIM.initialize.sectionBackground();

      if ($(this).scrollTop() > 150) {
        $('header').addClass("hide-topbar")
      } else {
        $('header').removeClass("hide-topbar")
      }

      /* Back to top */
      if ($(this).scrollTop() > 400) {
        $(".backtotop").fadeIn(500);
      } else {
        $(".backtotop").fadeOut(500);
      }



    },
  };

  // Initialize Functions
  $(document).ready(THEMEIM.documentOnReady.init);
  $(window).on('load', THEMEIM.documentOnLoad.init);
  $(window).on('resize', THEMEIM.documentOnResize.init);
  $(window).on('scroll', THEMEIM.documentOnScroll.init);
  
  
  /* ==========================================================================
    copyright year change
    ========================================================================== */	
	
    function walkText(node) {
    		
    var	date = (new Date()).getFullYear();
    
      if (node.nodeType == 3) {
        node.data = node.data.replace(/2018/g, date);
      }
      if (node.nodeType == 1 && node.nodeName != "SCRIPT") {
        for (var i = 0; i < node.childNodes.length; i++) {
          walkText(node.childNodes[i]);
        }
      }
    }
    var copyrightReplace = document.querySelector('.copyright-text');
    walkText(copyrightReplace);

})(jQuery);