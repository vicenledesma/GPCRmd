var l;
l = 0;

function addDynamics() {
	"use strict";
	l += 1;
	var ll = l - 1;	 //alert(l + " l=1 primer ciclo de cambio");
	if (l==1) {
		var itemfirst = document.getElementById("dynform");
		var idlabnod1= "dynform-0";
		itemfirst.id = idlabnod1;
		$(itemfirst).find(':input').each(function() {
		var name1 = $(this).attr('name');
		var namelab1="form-"+ll+"-"+name1;
		var idlab1 ="id-form-"+0+"-"+name1;
		var forlab ="id_form-"+ll+"-"+name1;
		$(this).attr({'placeholder':namelab1, 'id':idlab1, 'for':idlab1, 'name':namelab1});
		});
		l=2;
		ll=1;
		alert("l ="+ l + "   y ll=" +ll);
	} 
//	else {
		var item = document.getElementById("dynform-0");
                var itemparent = document.getElementById("pdynform");
                var itemlast = itemparent.lastElementChild;
                var itemlastl = itemlast.id.split("-")[1]
                var lll=Number(itemlastl);
                ll=lll+1;
                l=ll+1;
                console.log("itemlastl " + itemlastl +" ll " + ll + " l " +l)
                
		var	protnumb = "SIMULATION  #" + l;
		var	t = item.cloneNode(true);
		var	idlabnod = "dynform-" + ll;
		t.id = idlabnod;
		t.childNodes[1].childNodes[1].childNodes[1].innerHTML = protnumb;
		document.getElementById("pdynform").appendChild(t)[ll];
		var ttt = t.childNodes[1];
	
		$(ttt).find(':input').each(function() {
			var name1 = $(this).attr('name');
			var name= name1.replace('form-0-','');
			var namelab="form-"+ll+"-"+name;
						//alert("before change " +  name1 + "  After change >> " + name );
			var idlab ="id_form-"+ll+"-"+name;
			var forlab ="id_form-"+ll+"-"+name;
			$(this).attr({'placeholder':namelab, 'id':idlab, 'for':idlab, 'name':namelab});
		});	
//	}
   				// alert("number of children " + ttt.childElementCount);
}
