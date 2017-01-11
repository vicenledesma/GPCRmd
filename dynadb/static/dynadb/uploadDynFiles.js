$(document).ready(function() {
    $.fn.exists = function () {
      return this.length !== 0;
    };
    $("[id^=id_][id$=_upload]").click(function(event) {
        var self = $(this);
        event.preventDefault();
        var file_type = self.attr('id').split('_')[1]
        var dynform = $(this).parents("#upload_dynform");
        var download_file = dynform.find("[id|='id_"+file_type+"_download_url']");
        var no_js = dynform.find("input[name='no_js']");
        no_js.val(0);
        var link_div = dynform.find("#id_"+file_type+"_download_url_div");
        var link_div_parent = link_div.parent();
        
        link_div.hide();
        
        self.prop('disabled',true);
        if (file_type == "traj") {
            var maxsize = "2 GB";
        } else {
            var maxsize = "50 GB";
        }
        
        $(dynform).ajaxSubmit({
            url: "./",
            type: 'POST',
            dataType:'json',
            success: function(data) {
                alert(data.msg);
                var i = 0;
                var download_url_file = data.download_url_file;
                $("[id^=id_"+file_type+"_download_url_div-]").remove();
                if (download_url_file.length == 1) {
                    download_url_file = download_url_file[0]
                }
                if (typeof download_url_file === 'string') {
                    download_file.attr('href',download_url_file);
                    download_file.show();
                    link_div.show();
                } else {
                    $(download_url_file).each(function() {
                        var link_div_new = link_div.clone();
                        link_div_new.attr('id',link_div_new.attr('id')+"-"+i.toString());
                        var download_file_new = link_div_new.find("[id|='id_"+file_type+"_download_url']");
                        download_file_new.attr('id',download_file.attr('id')+"-"+i.toString());
                        download_file_new.attr('href',this);
                        download_file_new.text(download_file_new.text().replace("file","file "+(i+1).toString()));
                        download_file_new.show();
                        link_div_new.show();
                        link_div_parent.append(link_div_new);
                        i++;
                    });
                    
                    

                    
                    
                    

                }
               
                
            },
            error: function(xhr,status,msg){
                if (xhr.readyState == 4) {
                    alert(status.substr(0,1).toUpperCase()+status.substr(1)+":\nStatus: " + xhr.status+". "+msg+".\n"+xhr.responseText);
                    $("[id^=id_"+file_type+"_download_url_div-]").remove();
                    download_file.hide();
                    if (xhr.status == 432) {
                        $("[id^=id_"+file_type+"_download_url_div-]").remove();
                    }
                }
                else if (xhr.readyState == 0) {
                    alert("Connection error. Please, try later and check that your file is not larger than "+maxsize+".");
                }
                else {
                    alert("Unknown error");
                    $("[id^=id_"+file_type+"_download_url_div-]").remove();
                    download_file.hide();
                }
            },
            complete: function(xhr,status,msg){
                self.prop('disabled',false);
                //if compatible or non-cross origin 
                if ( window.parent.document != null) {
                    var current_iframe = $(window.parent.document).find("#id_"+file_type+"_iframe");
                    if (current_iframe.exists()) {
                        var body_height = self.parents("body").height();
                        current_iframe.height(body_height);
                        
                    }
                }

            }
        });
    });   
});