//Get path arguments (if any)
var args, itype, ligandonly, cluster, rev;
args = window.location.pathname.match(/\/(\w+)&(\w+)&(\w+)&(\w+)/);
if(args){
    itype = args[1];
    clusters = args[2];
    ligandonly = args[3];
    rev = args[4];
}
else {
    itype = 'all';
    clusters = '3';
    ligandonly = 'prt_lg';
    rev = 'norev';        
}

$(document).ready(function(){
    
    //I don't know what this line does, but Mariona told me to add it and I trust her wisdom
    document.domain=document.domain;

	////////////
	// Functions
	////////////

    function createFlareplotCustom(fpsize, jsonData, fpdiv, showContacts = false){
        var fpjson=jsonData;
        if (fpjson.edges[0].helixpos != undefined) {
            //$("#fpShowResSetBtns").css("display","inline-block");
            if(showContacts!= "all"){
                var edges=fpjson.edges;
                var newedges=[];
                for (eN=0; eN < edges.length ; eN++ ){
                    var edge = edges[eN];
                    if (edge.helixpos == showContacts){
                        newedges.push(edge);
                    }
                }
                fpjson.edges=newedges;
            }
        }

        plot=createFlareplot(fpsize, fpjson, fpdiv);

        //Wider lines
        $("path.link").css('stroke-width', 6); 
        //Thicker lines
        $("path.link").css('stroke-opacity', 0.5);         

        return(plot);
    }

    function setFpNglSize(applyMinSize, flare_container){
	    var screen_h=screen.height;
	    var min_size=300;
	    var fpcont_w_str=$(flare_container).css("width");
	    var fpcont_w=Number(fpcont_w_str.match(/^\d*/g)[0]);
	    var final_size = fpcont_w;
	    if (screen_h){
	        var max_h=screen_h*0.5;
	        var maxR_h=Math.round(max_h);
	        if (fpcont_w > maxR_h){
	            final_size = maxR_h;
	        }
	    } 
	    
	    if (applyMinSize){
	        if (final_size < min_size){
	            final_size = min_size;
	        }
	    }
	    return (final_size)
	}

    function emptyFPsels(flare_container, plot){
        //Clear all selected positions from both NGL and flareplots
        $(flare_container).find("g.node.toggledNode").each(function(){
            if (plot){
                var nodename = $(this).attr("id");
                var nodenum=nodename.split("-")[1];
                plot.toggleNode(nodenum)
                fpSelInt={};
            }
        });
        //Trigger click on random position to activate embed_contmaps_bottom set_positions function
        $(flare_container+" #node-5x42 text").trigger("click");        
    }

    function show_in_structure(flare_container, fp_display){
        if($(fp_display).hasClass("active")){
            $(fp_display).removeClass("active");            
        }
        else{
            $(fp_display).addClass("active");            
        }
        //Trigger click on random position to activate embed_contmaps_bottom set_positions function
        $(flare_container+" #node-5x42 text").trigger("click");
    }

    function colorsHoverActiveInactive(myselector,activeclass,colorhov,colorNohobAct, colorNohobInact){
        $(myselector).hover(function(){
            $(this).css("background-color",colorhov);
        },
        function(){
            var selected=$(this).hasClass(activeclass);
            if (selected){
                $(this).css("background-color",colorNohobAct);
            } else {
                $(this).css("background-color",colorNohobInact);
            }
        });
    };

    function change_display_sim_option(to_activate,to_inactivate){
        $(to_activate).addClass("is_active");
        $(to_activate).css("background-color","#bfbfbf");
        
        $(to_inactivate).removeClass("is_active");
        $(to_inactivate).css("background-color","#FFFFFF");
    }

    function updateFPInt(plot, flare_container){
        //Updates the fpSelInt dict depending on the nodes that are clicked
        allEdges= plot.getEdges()
        var updFpSelInt={}
        $(flare_container).find("g.node.toggledNode").each(function(){
            var nodename=$(this).attr("id");
            if (nodename.indexOf("node-") !== -1){        
                var nodenum=nodename.split("-")[1];
                var nodepos=fpgpcrdb_dict[nodenum].join(":"); 
                
                var edges=[];
                allEdges.forEach(function(e){
                    if (e.edge.name1==nodenum){
                        var othernum=e.edge.name2;
                        edges.push(fpgpcrdb_dict[othernum].join(":"));
                    } else if (e.edge.name2==nodenum){
                        var othernum=e.edge.name1;
                        edges.push(fpgpcrdb_dict[othernum].join(":"));
                    }
                });
                if (edges.length > 0){
                    updFpSelInt[nodepos]=edges;
                }
            }
        })
        fpSelInt = updFpSelInt;
    }

	 function changeContactsInFplot(id, fpdir, plots){
        //create new FP but saving the selected contacts
        
        flare_container = "#flare-container" + id;
        fpdiv = "#fpdiv" + id;
        showContacts=$(fpdiv).find(".fp_display_element.is_active").data("tag");

        //Update display button
        $("#clusterbutton" + id).html("Cluster " + showContacts + ' <span class="caret"></span>');

        //pg_framenum=new_fnum //?
        var pre_resSelected=[];
        $(flare_container).find("g.node.toggledNode").each(function(){
            var nodename=$(this).attr("id");
            var nodenum=nodename.split("-")[1];
            pre_resSelected.push(nodenum);
        })
        var fpfile_now="cluster" + showContacts + ".json";
        d3.json(fpdir+fpfile_now, function(jsonData){
            $(flare_container).html("");
            var fpsize=setFpNglSize(true, flare_container); // Or just use the size used before?
            plots[id] = createFlareplotCustom(fpsize, jsonData, flare_container, showContacts, plots[id]);
            allEdges= plots[id].getEdges();
            numfr = plots[id].getNumFrames();
            
            if ($("#fp_display_summary").hasClass("is_active")){
                plots[id].framesSum(0, numfr);
            }
            
            for (nN=0;nN<pre_resSelected.length;nN++){//Select at plot the residues selected before
                plots[id].toggleNode(pre_resSelected[nN]);
            }

            //updateFPInt(plot, flare_container)//I'm going to skip this for the moment. fpgpcrdb_dict is hard to obtain. //Update fpSelInt depending on what is in the fplot.
            $("#selectionDiv").trigger("click");

            //Add hoverlabels
            hoverlabels(id)

        });
    }

    function hoverlabels(id){
        var pos, source_pos, target_pos;
        var source_pos_pat = /source-(\w+)/;
        var target_pos_pat = /target-(\w+)/;
        //Put hoverlabels (tooltips) in flareplots position rectangles
        $('#flare-container'+id+' .trackElement path').each(function(){
            $(this).tooltip({
              html: true,
              placement: 'top',
              container: 'body'
            });
        });

        //Put hoverlabels (tooltips) in flareplot position texts
        $('#flare-container'+id+' .node text').each(function(){
            pos = $(this).html();
            $(this).tooltip({
              title: pos,
              html: true,
              placement: 'top',
              container: 'body'
            });
        });

        //Put hoverlabels on interaction lines
        $('#flare-container'+id+' .link').each(function(){
            source_pos = $(this).attr('class').match(source_pos_pat)[1];
            target_pos = $(this).attr('class').match(target_pos_pat)[1];
            $(this).tooltip({
              title: source_pos+"-"+target_pos,
              html: true,
              placement: 'auto',
              container: 'body'
            });
        });
    };

	////////////////////
	//Flare plots time!!
	////////////////////
    //Make sure NGL viewers are ok before 
    $('body').on('iframeSet',function(){
        $('#ngl_iframe0')[0].contentWindow.$('body').trigger('iframeSetOk');
        $('#ngl_iframe1')[0].contentWindow.$('body').trigger('iframeSetOk');
        var fpdir = $("#flare_col").data("fpdir");

    	//Create initial flareplots
    	if (fpdir) {
    		var plots = [];
            var fpsize=setFpNglSize(true, "#flare-container0");

            d3.json(fpdir+"cluster1.json", function(jsonData){
    	        plots[0] = createFlareplotCustom(fpsize, jsonData, "#flare-container0", "Inter");
               	$('#loading_flare0').css('display', 'none');
                
                //Paint flareplots legend once they are loaded
                var id_element,color_element;
                parent.$(".Legend-element").each(function(){
                    id_element = $(this).attr('id');
                    color_element = parent.$("g[id^='"+id_element+"'] path").css('fill');
                    $(this).css('background-color',color_element);
                })

                //Put hoverlabels to flareplot
                hoverlabels(0)
            });
            d3.json(fpdir+"cluster2.json", function(jsonData){
    	        plots[1] = createFlareplotCustom(fpsize, jsonData, "#flare-container1", "Inter");
    	        $('#loading_flare1').css('display', 'none');

                //Put hoverlabels to flareplot
                hoverlabels(1)
            });

    	}

    	//clear buttons
    	$("#FPclearSel0").click(function(){
    		emptyFPsels("#flare-container0", plots[0]);
    	});
    	$("#FPclearSel1").click(function(){
    		emptyFPsels("#flare-container1", plots[1]);
    	});

        //"Show in structure buttons"
        $("#FPdisplay0").click(function(){
            show_in_structure("#flare-container0", "#FPdisplay0");
        });
        $("#FPdisplay1").click(function(){
            show_in_structure("#flare-container1", "#FPdisplay1");
        });

    	//Hover in "cluster" dropups
        colorsHoverActiveInactive(".fp_display_element","is_active","#f2f2f2","#bfbfbf","#FFFFFF");	

        //On click of cluster dropups
        $("#fpdiv0 .clusters_dropup-ul li").click(function(){
        	var to_activate =$(this).attr('id');
        	var to_inactivate = $("#fpdiv0 .clusters_dropup-ul .is_active").attr('id');
        	if (to_activate != to_inactivate){
    	    	change_display_sim_option("#" + to_activate, "#" + to_inactivate);
        		changeContactsInFplot("0", fpdir, plots);

                //Set new dyn list for dropdown in NGL viewer
                var new_clust = "cluster"+$(this).attr('data-tag')
        	}
        });
        $("#fpdiv1 .clusters_dropup-ul li").click(function(){
        	var to_activate =$(this).attr('id');
        	var to_inactivate = $("#fpdiv1 .clusters_dropup-ul .is_active").attr('id');
        	if (to_activate != to_inactivate){
    	    	change_display_sim_option("#" + to_activate, "#" + to_inactivate);
    	    	changeContactsInFplot("1", fpdir, plots);

                //Set new dyn list for dropdown in NGL viewer
                var new_clust = "cluster"+$(this).attr('data-tag')
    	    }
        });

        //Load needed Json files and execute NGL bottom viewers
        var clustdict_file, compl_data_file;
        clustdict_file = "/dynadb/files/Precomputed/get_contacts_files/view_input_dataframe/"+itype+"_"+ligandonly+"_jsons/"+clusters+"clusters/clustdict.json";
        compl_data_file = window.location.origin + "/dynadb/files/Precomputed/get_contacts_files/compl_info.json"; 
        $.getJSON(clustdict_file, function(clustdict){  
            $.getJSON(compl_data_file, function(compl_data){
                //Trigger the NGL viewers
                $('#ngl_iframe0')[0].contentWindow.$('body').trigger('createNGL0', [clustdict, compl_data]);
                $('#ngl_iframe1')[0].contentWindow.$('body').trigger('createNGL1', [clustdict, compl_data]);
            });
        });
    });
});