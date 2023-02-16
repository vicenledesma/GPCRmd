$(document).ready( function () {

    $('[data-toggle="tooltip"]').tooltip(); 
    $('#table_id').DataTable(
        {
         "order": [],
        //"scrollY": 100,
        //"scrollX": true,
           "columnDefs": [ 
                        { "orderable": false, "searchable": false, "targets": 0 },   //Don't give option to sort or search by column 0
                        ],
          dom:"<'myfilter'f><'mylength'l>rtip",
          
        }
    );
    $('#loading', window.parent.document).css("display","none");
    $('#table_id').css("display","table");

    
    $(".links a").click(function(){
        $("body").css("cursor","progress");
        $('*', window.parent.document).css("cursor","progress");
    }) ;


    // If '#...' in URL (searched from homepage) write the input in the searchbar
    // var path_list = window.location.href.split("/");
    // var path_list = document.referrer.split("/");
    var path_list = window.top.location.href.toString().split("/");
    console.log(path_list[5])
    if (path_list[5].indexOf('#') > -1)
    {
        var inputElement = path_list[5].replace('#','')
        // if spaces in url
        if (inputElement.indexOf('%20') > -1){
            inputElement=inputElement.replaceAll('%20',' ')
        }
        $('#table_id').DataTable().search(inputElement).draw();
    }
       
} );


