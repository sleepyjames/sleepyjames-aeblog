;(function(){

    $(document).ready(function(){
        
        var topnav = $("#topnav"), 
            mobile_nav = $("<select />").attr('id', 'topnav-mobile');

        mobile_nav.append($('<option>Goto..</option>'));
        topnav.find('a').each(function(){

            var el = $(this), option = $('<option />');
            option.html(el.html()).val(el.attr('href'));
            mobile_nav.append(option);

        });
        mobile_nav.change(function(){
            if(this.value) 
                window.location.href = this.value;
        });
        topnav.after(mobile_nav);

        $('#messages .close').click(function(){
            $(this).closest('li').slideUp();            
            return false;
        });

    });

})()
