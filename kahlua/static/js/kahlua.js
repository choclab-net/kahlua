$(function(){
    "use strict";
    var sect = $( window.location.hash ),
        portfolio = $('.portfolio-items');
    if(sect.length == 1){
        $('.section.active').removeClass('active');
        sect.addClass('active');
        if( sect.hasClass('border-d') ){
            $('body').addClass('border-dark');
        }
    }
    /*=========================================================================
        Magnific Popup (Project Popup initialization)
    =========================================================================*/
    $('.view-project').magnificPopup({
        type: 'inline',
        fixedContentPos: false,
        fixedBgPos: true,
        overflowY: 'auto',
        closeBtnInside: true,
        preloader: false,
        midClick: true,
        removalDelay: 300,
        mainClass: 'my-mfp-zoom-in'
    });
    $(window).on('load', function(){
        $('body').addClass('loaded');
        /*=========================================================================
            Portfolio Grid
        =========================================================================*/
        portfolio.shuffle();
        $('.portfolio-filters > li > a').on('click', function (e) {
            e.preventDefault();
            var groupName = $(this).attr('data-group');
            $('.portfolio-filters > li > a').removeClass('active');
            $(this).addClass('active');
            portfolio.shuffle('shuffle', groupName );
        });
        $('li.blog-post-item div.rich-text').each(function(idx, item){
            $(item).prepend($(item).find('img').remove())
        });
    });
    /*=========================================================================
        Main tabbar
    =========================================================================*/
    $('ul.tabs li').click(function(){
        var tab_id = $(this).attr('data-tab');

        $('ul.tabs li').removeClass('current');
        $('.tab-content').removeClass('current');

        $(this).addClass('current');
        $("#"+tab_id).addClass('current');
    });
    /*=========================================================================
        Navigation Functions
    =========================================================================*/
    $('.section-toggle').on('click', function(){
        var $this = $(this),
            sect = $( '#' + $this.data('section') ),
            current_sect = $('.section.active');
        if(sect.length == 1){
            if( sect.hasClass('active') == false && $('body').hasClass('section-switching') == false ){
                $('body').addClass('section-switching');
                if( sect.index() < current_sect.index() ){
                    $('body').addClass('up');
                }else{
                    $('body').addClass('down');
                }
                setTimeout(function(){
                    $('body').removeClass('section-switching up down');
                }, 2500);
                setTimeout(function(){
                    current_sect.removeClass('active');
                    sect.addClass('active');
                }, 1250);
                if( sect.hasClass('border-d') ){
                    $('body').addClass('border-dark');
                }else{
                    $('body').removeClass('border-dark');
                }
            }
        }

        setTimeout(function(){
            $(sect.find('ul.tabs').find('>:first')[0]).click()
        }, 1250);
    });
    /*=========================================================================
        Testimonials Slider
    =========================================================================*/
    $('.testimonials-slider').owlCarousel({
        items: 2,
        responsive:{
            992: {
                items: 2
            },
            0: {
                items: 1
            }
        }
    });
});
