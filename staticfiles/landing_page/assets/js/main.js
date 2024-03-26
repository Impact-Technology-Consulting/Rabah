(function($) {
    "use strict";

    // Preloader
    $(".preloader").delay(1600).fadeOut("slow");


    // Sticky Menu
    $(window).on('scroll', function() {
        var scroll = $(window).scrollTop();
        if (scroll >= 10) {
            $(".header-menu-area").addClass("sticky");
        } else {
            $(".header-menu-area").removeClass("sticky");
        }
    });



    // Mobile menu
    $('.hamburger').on('click', function(event) {
        $(this).toggleClass('h-active');
        $('.main-nav').toggleClass('slidenav');
    });
    $('.header-home .main-nav ul li  a').on('click', function(event) {
        $('.hamburger').removeClass('h-active');
        $('.main-nav').removeClass('slidenav');
    });

    $(".main-nav .fl").on('click', function(event) {
        var $fl = $(this);
        $(this).parent().siblings().find('.sub-menu').slideUp();
        $(this).parent().siblings().find('.fl').addClass('flaticon-plus').text("+");
        if ($fl.hasClass('flaticon-plus')) {
            $fl.removeClass('flaticon-plus').addClass('flaticon-minus').text("-");
        } else {
            $fl.removeClass('flaticon-minus').addClass('flaticon-plus').text("+");
        }
        $fl.next(".sub-menu").slideToggle();
    });


    // Magnific Popup gallery
    $('.single-sidebar-gallery').magnificPopup({
        delegate: 'a', // child items selector, by clicking on it popup will open
        gallery: {
            enabled: true
        },
        type: 'image'
        // other options
    });

    // Pricing Toggle
    var checkBox = document.querySelectorAll("#checbox")

    for (let i = 0; i < checkBox.length; i++) {
        checkBox[i].addEventListener("click", () => {
            var text1 = document.querySelectorAll(".text1")
            var text2 = document.querySelectorAll(".text2")

            if (checkBox[i].checked === true) {
                text1.forEach((e) => {
                    e.style.display = "block";
                })
                text2.forEach((e) => {
                    e.style.display = "none";
                })
            } else if (checkBox[i].checked === false) {
                text1.forEach((e) => {
                    e.style.display = "none";
                })
                text2.forEach((e) => {
                    e.style.display = "block";
                })
            }

        })
    }
    var anaulPrice = document.querySelectorAll(".price-anual")
    var monthlyPrice = document.querySelectorAll(".price-month")


    anaulPrice.forEach((element) => {
        element.addEventListener("click", () => {
            if (!element.classList.contains('price-active')) {
                element.classList.add('price-active')

                monthlyPrice.forEach((ele) => {
                    ele.classList.remove('price-active')
                })
            }
        })
    })

    monthlyPrice.forEach((element) => {
        element.addEventListener("click", () => {
            if (!element.classList.contains('price-active')) {
                element.classList.add('price-active')

                anaulPrice.forEach((ele) => {
                    ele.classList.remove('price-active')
                })
            }
        })
    })


    //Mixitup
    $('.work-mixi').mixItUp();

    // Counter
    $('.counter').counterUp({
        delay: 10,
        time: 1000
    });


    // Magnific Popup video
    $('.popup-youtube').magnificPopup({
        disableOn: 700,
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,

        fixedContentPos: false
    });



    // Slick slide about us

    $('.mission-slide-img-one').slick({
        slidesToScroll: 1,
        slidesToShow: 1,
        dots: true,
        fade: true,
        arrows: false,
        prevArrow: "<i class='bx bxs-chevron-left'></i>",
        nextArrow: "<i class='bx bxs-chevron-right' ></i>"
    });






    // Owl Carousel Service
    $('.service-slide-wrap').owlCarousel({
        items: 3,
        loop: true,
        smartSpeed: 1500,
        autoplay: false,
        dots: false,
        margin: 24,
        nav: true,
        navText: ["<i class='fas fa-chevron-left'></i>", "<i class='fas fa-chevron-right'></i>"],
        responsive: {
            0: {
                items: 1
            },
            480: {
                items: 1
            },

            768: {
                items: 2
            },
            992: {
                items: 2
            },
            1200: {
                items: 3
            },
            1400: {
                items: 3
            }

        }
    });


    // Owl Carousel Team
    $('.team-slide-wrap').owlCarousel({
        items: 3,
        loop: true,
        smartSpeed: 1500,
        autoplay: false,
        dots: false,
        margin: 24,
        nav: true,
        navText: ["<i class='fas fa-chevron-left'></i>", "<i class='fas fa-chevron-right'></i>"],
        responsive: {
            0: {
                items: 1
            },
            480: {
                items: 1
            },

            768: {
                items: 2
            },
            992: {
                items: 2
            },
            1200: {
                items: 3
            },
            1400: {
                items: 3
            }

        }
    });



    // Contact Form

    // Get the form.
    var form = $('#contact-form');

    // Get the messages div.
    var formMessages = $('.form-message');

    // Set up an event listener for the contact form.
    $(form).on('submit', function(e) {
        // Stop the browser from submitting the form.
        e.preventDefault();

        // Serialize the form data.
        var formData = $(form).serialize();

        // Submit the form using AJAX.
        $.ajax({
                type: 'POST',
                url: $(form).attr('action'),
                data: formData
            })
            .done(function(response) {
                // Make sure that the formMessages div has the 'success' class.
                $(formMessages).removeClass('error');
                $(formMessages).addClass('success');

                // Set the message text.
                $(formMessages).text(response);

                // Clear the form.
                $('#contact-form input,#contact-form textarea').val('');
            })
            .fail(function(data) {
                // Make sure that the formMessages div has the 'error' class.
                $(formMessages).removeClass('success');
                $(formMessages).addClass('error');

                // Set the message text.
                if (data.responseText !== '') {
                    $(formMessages).text(data.responseText);
                } else {
                    $(formMessages).text('Oops! An error occured. Message could not be sent.');
                }
            });
    });


    // Bottom To Top
    $(window).on('scroll', function() {
        if ($(this).scrollTop() > 100) {
            $('#scroll-top').fadeIn();
        } else {
            $('#scroll-top').fadeOut();
        }
    });
    $('#scroll-top').on('click', function() {
        $("html, body").animate({
            scrollTop: 0
        }, 600);
        return false;
    });



    // Coming Soon Countdown 

    function timeConverter(UNIX_timestamp) {
        var a = new Date(UNIX_timestamp * 1000);
        var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        var year = a.getFullYear();
        var month = months[a.getMonth()];
        var date = a.getDate();
        var hour = a.getHours();
        var min = a.getMinutes();
        var sec = a.getSeconds();
        var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec;
        // return time;
        console.log(date);

        $("#timer #days").html(date);
        $("#timer #hours").html(hour);
        $("#timer #minutes").html(min);
        $("#timer #seconds").html(sec);
    }

    function makeTimer() {

        var endTime = new Date("September 01, 2022 00:00:00");
        var endTime = (Date.parse(endTime)) / 1000; //replace these two lines with the unix timestamp from the server

        var now = new Date();
        var now = (Date.parse(now) / 1000);

        var timeLeft = endTime - now;

        var days = Math.floor(timeLeft / 86400);
        var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
        var Xmas95 = new Date('December 25, 1995 23:15:30');
        // console.log(Xmas95);
        // console.log(Date.parse(timeLeft * 1000));
        var hour = Xmas95.getHours();
        // console.log(hour);

        var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600)) / 60);
        var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));

        if (hours < "10") {
            hours = "0" + hours;
        }
        if (minutes < "10") {
            minutes = "0" + minutes;
        }
        if (seconds < "10") {
            seconds = "0" + seconds;
        }

        $("#timer #days").html(days);
        $("#timer #hours").html(hours);
        $("#timer #minutes").html(minutes);
        $("#timer #seconds").html(seconds);

    }

    setInterval(function() {
        makeTimer();
    }, 1000);

    // Coming Soon Countdown end


    jQuery(window).on('load', function() {

        //wow Animation
        new WOW().init();
        window.wow = new WOW({
            boxClass: 'wow', // default
            animateClass: 'animated', // default
            offset: 0, // default
            mobile: true, // default
            live: true, // default
            offset: 100
        })
        window.wow.init();
    });


}(jQuery));