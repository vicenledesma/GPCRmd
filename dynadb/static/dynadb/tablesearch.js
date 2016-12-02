function ShowResults(data, restype,is_apoform){
    var tablestr='';
    if (restype=='complex' &&  data.result.length>0 ){
        var cl=data.result;
        for(i=0; i<cl.length; i++){
            tablestr=tablestr+"<tr><td> <a target='_blank' class='btn btn-info' role='button' href=/dynadb/complex/id/"+cl[i][0]+"> Complex with ID "+cl[i][0]+"</a> </td><td>  Receptor: <kbd>"+cl[i][1]+"</kbd> Ligand: <kbd>"+ cl[i][2]+"</kbd>. </td></tr>";
        }
    }//endif

    //Results are models
    if ( restype=='model'  && data.model.length>0){
        var rl=data.model
        for(i=0; i<rl.length; i++){ //rl[i].length>2
            if (rl[i].length>2 && (is_apoform=='com'||is_apoform=='both') ){
                tablestr=tablestr+"<tr><td>"+ "<a target='_blank' class='btn btn-info' role='button' href=/dynadb/model/id/"+rl[i][0]+"> Complex Structure ID:"+rl[i][0] +"</a> </td><td> Receptor: <kbd>"+rl[i][1]+"</kbd> Ligand: <kbd>"+rl[i][2]+"</kbd> </td></tr>";
            }if (rl[i].length==2 && (is_apoform=='apo'||is_apoform=='both')) {
                tablestr=tablestr+"<tr><td>"+ "<a target='_blank' class='btn btn-info' role='button' href=/dynadb/model/id/"+rl[i][0]+"> Apoform Complex Structure ID:"+rl[i][0]+"</a> </td><td> Protein: <kbd>"+rl[i][1]+"</kbd> </td></tr>";
            }
        }
    }//endif


    if (restype=='dynamics' && data.dynlist.length>0  ){
        var dl=data.dynlist;
        for(i=0; i<dl.length; i++){
            if (dl[i].length>2 && (is_apoform=='com'||is_apoform=='both')){ //dl[i].length>2
                tablestr=tablestr+"<tr><td>"+ "<a target='_blank' class='btn btn-info' role='button' href=/dynadb/dynamics/id/"+dl[i][0]+"> Dynamics ID:"+dl[i][0]+" </a></td><td> Receptor: <kbd>"+dl[i][1]+ "</kbd> Ligand:<kbd>"+ dl[i][2]+"</kbd></td></tr>";
            }if (dl[i].length==2 && (is_apoform=='apo'||is_apoform=='both')) {
                tablestr=tablestr+"<tr><td>"+ "<a target='_blank' class='btn btn-info' role='button' href=/dynadb/dynamics/id/"+dl[i][0]+"> Dynamics ID:"+dl[i][0]+" </a></td><td> Receptor:<kbd> "+dl[i][1]+"</kbd></td></tr>";
            }
        }
    } //endif

    return tablestr;

}//end of function definition

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function CreateTable(){
    if ( $.fn.dataTable.isDataTable( '#ajaxresults22' ) ) {
        table = $('#ajaxresults22').DataTable();
    }
    else {
        table = $('#ajaxresults22').DataTable( {
            "sPaginationType" : "full_numbers",
            "lengthMenu": [[5, 25, 50, -1], [5, 25, 50, "All"]],
            "oLanguage": {
                "oPaginate": {
                    "sPrevious": "<",
                    "sNext": ">",
                    "sFirst": "<<",
                    "sLast": ">>",
                 }
            }
        } );
    }   
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

$("#tablesearch").click(function() {
    $('#ajaxresults22').DataTable().clear().draw();
    var exactboo=$('#exactmatch').prop('checked');
    var bigarray=[];
    var openpar=[];
    var closingpar=[]
    var flag=0; //means no errors
    $("#tablesearch").prop("disabled",true);


    //pick information of advanced search, parenthesis
    if ($('#gotoadvsearch').html().length==19){
        var typeofsearch='advanced';
        $("#myTable tr").each(function () {
            var postarray=[];
            var counter=0;
            $('td', this).each(function () {
                if (counter==0){
                    var drop=$(this).find(":selected").text();
                    postarray.push(drop);

                }else if (counter==1) {
                    var drop=$(this).find(":selected").text();
                    postarray.push(drop);
                    openpar.push(drop);

                }else{
                    if (counter==4){
                        if (postarray[2]=='protein') {
                            var isligrec=$(this).find('[type=checkbox]').prop('checked');
                            postarray.push(isligrec);
                        }else{
                            var drop=$(this).find(":selected").val();
                            postarray.push(drop);  
                        }
                    }else if (counter==5) {
                        var drop=$(this).find(":selected").text();
                        postarray.push(drop);
                        closingpar.push(drop);
                    } else {
                        var value = $(this).text(); //var value = $(this).text();
                        postarray.push(value);
                    }
                }
                counter=counter+1;
            })
            bigarray.push(postarray);
        })

    }else{
        //pick simple search information
        var typeofsearch='simple';
        $("#myTable tr").each(function () {
            var postarray=[];
            var counter=0;
            $('td', this).each(function () {
                if (counter==0){
                    var drop=$(this).find(":selected").text();
                    postarray.push(drop);
                } else {
                    if (counter==3){
                        if(postarray[1]=='protein'){
                            var isligrec=$(this).find('[type=checkbox]').prop('checked');
                            postarray.push(isligrec);    
                        }else{
                            var drop=$(this).find(":selected").val();
                            postarray.push(drop); 
                        }

                    } else {
                        var value = $(this).text(); //var value = $(this).text();
                        postarray.push(value);
                    }
                }
                counter=counter+1;
            })
            bigarray.push(postarray);
        })
    } //else ends

    for (i=0;i<openpar.length;i++){
        if (openpar[i]=='(' && openpar[i+1]=='('){
            flag=2;
            flagsms='nested parenthesis is not allowed.';
        }
    }

    for (i=0;i<closingpar.length;i++){
        if (closingpar[i]==')' && closingpar[i+1]==')'){
            flag=2;
            flagsms='nested parenthesis is not allowed.';
        }
    }
    status='off';
    for (i=0;i<closingpar.length;i++){
        if ( closingpar[i]==')' && openpar[i]=='(' ) {
            flag=3;
            flagsms='inline parenthesis is not allowed.';
        }
        if (openpar[i]=='(') {
            if (status=='on'){
                flag=4;
                flagsms='Mismatching parenthesis!';
            }else{
                status='on';
            }

        }
        if (closingpar[i]==')'){
            if (status=='off'){
                flag=4;
                flagsms='Mismatching parenthesis!';
            }else{
                status='off';
            }
        }

    }

    if (status=='on'){
        flag=4;
        flagsms='Mismatching parenthesis!';
    }

    var restype=$('#result_type').val();
    var ff=$('#fftype').val();
    var tstep=$('#tstep').val();
    var sof=$('#soft').val();
    var mem=$('#memtype').val();
    var method=$('#method').val();
    var sol=$('#soltype').val();
    if (restype=='model'){
        var is_apoform=$('#search_type').find(":selected").val();
    }
    if (restype=='dynamics'){
        var is_apoform=$('#search_type_dyn').find(":selected").val();
    }

    if (flag!=0){
        alert(flagsms);
        return false;
    }

    ///////////////////////////////////////////EMPTY SEARCH //////////////////////////////////////////////////////////

    if(bigarray.length==1 && (restype=='model' || restype=='dynamics') ){ //empty
        $.ajax({
            type: "POST",
            data: {'restype':restype,'ff':ff,'tstep':tstep,'sol':sol,'mem':mem,'method':method,'sof':sof,'is_apo':is_apoform},
            headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            },
            url: "/dynadb/empty_search/",
            dataType: "json",
            success: function(data) {
                $("#tablesearch").prop("disabled",false);
                if (data.message==''){
                    $('#ajaxresults22 tbody').empty();
                    tablestr=ShowResults(data, restype,is_apoform);
                    $('#ajaxresults22').DataTable().destroy()
                    setTimeout(function() {
                        $('#ajaxresults22 tbody').append(tablestr);
                        CreateTable();
                    }, 500);


                }else{
                    alert(data.message);
                }
            },

            error: function(XMLHttpRequest, textStatus, errorThrown) {
                $("#tablesearch").prop("disabled",false);
                alert("Something unexpected happen.");
            }
        }); //end of ajax call
        return true;
    }

    if (bigarray.length==1 && restype=='complex'){
        alert('Complex search does not work if there is not any protein or molecule.You have to add proteins, molecules or compounds from the left to search for complexes.');
        $("#tablesearch").prop("disabled",false);
        return false;
    }

    /////////////////////////////////////////// SIMPLE SEARCH //////////////////////////////////////////////////////////
    if ($('#gotoadvsearch').html().length==21){


        for (i=1;i<bigarray.length;i++){
            bigarray[i].splice(1, 0, " ");
            bigarray[i].splice(5, 0, "");        


        $.ajax({
            type: "POST",
            data: {  "bigarray[]": bigarray, 'exactmatch':exactboo,'restype':restype,'ff':ff,'tstep':tstep,'sol':sol,'mem':mem,'method':method,'sof':sof,'is_apo':is_apoform,'typeofsearch':typeofsearch},
            headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            },
            url: "/dynadb/advanced_search/",//"/dynadb/complex_search/",
            dataType: "json",
            success: function(data) {
                $("#tablesearch").prop("disabled",false);
                if (data.message==''){
                    $('#ajaxresults22 tbody').empty(); //this new
                    tablestr=ShowResults(data,restype,is_apoform);
                    $('#ajaxresults22').DataTable().destroy() //this new
                    $('#ajaxresults22 tbody').append(tablestr);
                    CreateTable();

                }else{
                    alert(data.message);
                }
            },

            error: function(XMLHttpRequest, textStatus, errorThrown) {
                $("#tablesearch").prop("disabled",false);
                alert("Something unexpected happen.");
            }
        });
        return true;
    }


    ///////////////////////////////////////////ADV SEARCH //////////////////////////////////////////////////////////
    }else{
        $.ajax({
            type: "POST",
            data: {  "bigarray[]": bigarray, 'exactmatch':exactboo,'restype':restype,'ff':ff,'tstep':tstep,'sol':sol,'mem':mem,'method':method,'sof':sof,'is_apo':is_apoform,'typeofsearch':typeofsearch},
            headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            },
            url: "/dynadb/advanced_search/",
            dataType: "json",
            success: function(data) {
                $("#tablesearch").prop("disabled",false);
                if (data.message==''){
                    $('#ajaxresults22 tbody').empty(); //this new
                    tablestr=ShowResults(data,restype,is_apoform);
                    $('#ajaxresults22').DataTable().destroy() //this new
                    $('#ajaxresults22 tbody').append(tablestr);
                    CreateTable();
                }else{
                    alert(data.message);
                    $("#tablesearch").prop("disabled",false);
                }
            },

            error: function(XMLHttpRequest, textStatus, errorThrown) {
                $("#tablesearch").prop("disabled",false);
                alert("Something unexpected happen.");
            }
        });
        return true;
    }//end of the "advanced search" else.

});

    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function getCookie(name) {
    var cookieValue = null;
    var i = 0;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (i; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).on('click', '#deleterow', function(e){
  e.preventDefault();
  $(this).closest('tr').remove();
  $('#myTable').find('.tableselect:first').empty().append('<option selected="selected" value=" ">'); //</option><option value="not">NOT</option>
});
