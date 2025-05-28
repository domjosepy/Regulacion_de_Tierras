(function($) {
  "use strict"; 

  // Verificar si jQuery está cargado
  if (typeof jQuery === "undefined") {
      console.error("jQuery no está cargado. Asegúrate de incluirlo antes de este script.");
      return;
  }

  // Toggle del sidebar
  $("#sidebarToggle, #sidebarToggleTop").on("click", function() {
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");

    if ($(".sidebar").hasClass("toggled")) {
      $(".sidebar .collapse").collapse("hide");
    }
  });

  // Cerrar menú si la pantalla es menor a 768px
  $(window).resize(function() {
    if ($(window).width() < 768) {
      $(".sidebar .collapse").collapse("hide");
    }
    if ($(window).width() < 480 && !$(".sidebar").hasClass("toggled")) {
      $("body").addClass("sidebar-toggled");
      $(".sidebar").addClass("toggled");
      $(".sidebar .collapse").collapse("hide");
    }
  });

  // Scroll en sidebar cuando está fijo
  $("body.fixed-nav .sidebar").on("mousewheel DOMMouseScroll wheel", function(e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Botón scroll-to-top aparece/desaparece
  $(document).on("scroll", function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $(".scroll-to-top").fadeIn();
    } else {
      $(".scroll-to-top").fadeOut();
    }
  });

  // Smooth scrolling
  $(document).on("click", "a.scroll-to-top", function(e) {
    var $anchor = $(this);
    $("html, body")
      .stop()
      .animate(
        {
          scrollTop: $($anchor.attr("href")).offset().top
        },
        1000,
        "easeInOutExpo"
      );
    e.preventDefault();
  });

})(jQuery);
