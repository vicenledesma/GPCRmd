var l;
l = 0;

function addModeledelement2() {
	"use strict";
	l += 1;
	var ll = l - 1;	 //alert(l + " l=1 primer ciclo de cambio");
	if (l==1) {
		var itemfirst = document.getElementById("Element2");
		var idlabnod1= "Element2_0";
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
//		alert("l ="+ l + "   y ll=" +ll);
	} 
//	else {
		var item = document.getElementById("Element2_0");
//		var	protnumb = "PROTEIN  #" + l;
		//alert("Mira   "+ item.id)
		var	t = item.cloneNode(true);
		var	idlabnod = "Element2_" + ll;
		t.id = idlabnod;
//		t.childNodes[1].childNodes[1].childNodes[1].innerHTML = protnumb;
		document.getElementById("pElement2").appendChild(t)[ll];
		var ttt = t;
	
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
