/**
* Template Name: Personal - v2.1.0
* Template URL: https://bootstrapmade.com/personal-free-resume-bootstrap-template/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
!(function($) {
  "use strict";

  function normalizeHash(hash) {
    return hash === '#education' ? '#about' : hash;
  }

  function showPortfolioSection(hash) {
    var sectionHash = normalizeHash(hash);
    var $section = $(sectionHash);
    if (!$section.length || !$section.is('section')) {
      return;
    }
    $('#header').addClass('header-top');
    $('section').removeClass('section-show');
    $section.addClass('section-show');
  }

  function setActiveNav(hash) {
    var navHash = normalizeHash(hash);
    $('.nav-menu .active, .mobile-nav .active').removeClass('active');
    $('.nav-menu, .mobile-nav').find('a[href="' + navHash + '"]').parent('li').addClass('active');
  }

  function navigateToHash(hash, updateNav) {
    var sectionHash = hash || '#about';
    var $target = $(normalizeHash(sectionHash));
    if (!$target.length) {
      return;
    }
    if (updateNav) {
      setActiveNav(sectionHash);
    }
    showPortfolioSection(sectionHash);
  }

  // Nav Menu
  $(document).on('click', '.nav-menu a, .mobile-nav a, #header h1 a', function(e) {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var hash = this.hash || '#about';
      var target = $(normalizeHash(hash));
      if (target.length) {
        e.preventDefault();
        navigateToHash(hash, $(this).parents('.nav-menu, .mobile-nav').length);
        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
          $('.mobile-nav-overly').fadeOut();
        }
        return false;
      }
    }
  });

  $(window).on('hashchange', function() {
    navigateToHash(window.location.hash, true);
  });

  // Default landing is About; other hashes open their section
  var initialHash = window.location.hash;
  var normalizedInitial = normalizeHash(initialHash);
  if (initialHash && normalizedInitial !== '#about' && $(normalizedInitial).is('section')) {
    navigateToHash(initialHash, true);
  } else {
    navigateToHash('#about', true);
  }

  // Mobile Navigation
  if ($('.nav-menu').length) {
    var $mobile_nav = $('.nav-menu').clone().prop({
      class: 'mobile-nav d-lg-none'
    });
    $('body').append($mobile_nav);
    $('body').prepend('<button type="button" class="mobile-nav-toggle d-lg-none"><i class="icofont-navigation-menu"></i></button>');
    $('body').append('<div class="mobile-nav-overly"></div>');

    $(document).on('click', '.mobile-nav-toggle', function(e) {
      $('body').toggleClass('mobile-nav-active');
      $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
      $('.mobile-nav-overly').toggle();
    });

    $(document).click(function(e) {
      var container = $(".mobile-nav, .mobile-nav-toggle");
      if (!container.is(e.target) && container.has(e.target).length === 0) {
        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
          $('.mobile-nav-overly').fadeOut();
        }
      }
    });
  } else if ($(".mobile-nav, .mobile-nav-toggle").length) {
    $(".mobile-nav, .mobile-nav-toggle").hide();
  }

  // jQuery counterUp
  $('[data-toggle="counter-up"]').counterUp({
    delay: 10,
    time: 1000
  });

  // Testimonials carousel (uses the Owl Carousel library)
  $(".testimonials-carousel").owlCarousel({
    autoplay: true,
    dots: true,
    loop: true,
    responsive: {
      0: {
        items: 1
      },
      768: {
        items: 2
      },
      900: {
        items: 3
      }
    }
  });

  // Porfolio isotope and filter
  $(window).on('load', function() {
    var portfolioIsotope = $('.portfolio-container').isotope({
      itemSelector: '.portfolio-item',
      layoutMode: 'fitRows'
    });

    $('#portfolio-flters li').on('click', function() {
      $("#portfolio-flters li").removeClass('filter-active');
      $(this).addClass('filter-active');

      portfolioIsotope.isotope({
        filter: $(this).data('filter')
      });
    });

  });

  // Initiate venobox (lightbox feature used in portofilo)
  $(document).ready(function() {
    $('.venobox').venobox();
  });

})(jQuery);