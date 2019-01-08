$(document).ready(function(){
    $('.menu-mob').click(function(){
        $('.middle-page-in .aside-l .nav-l').slideToggle(500);
        $(this).toggleClass('active');
    });

    $('.user-data-mob').click(function(){
        $('.middle-page-in .content-page .user-data-wrap').slideToggle(500);
        $(this).toggleClass('active');
    });
});
