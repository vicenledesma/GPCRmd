
     $.fn.protein_init_config = function(){
        $(document).find("[id|=protform]").each(function(){
            var protform=$(this)
            var is_mutated= $(protform).find("[id='id_is_mutated'],[id|=id_form][id$='is_mutated']");
            var mutations = $(protform).find("[id='id_mutations_id'],[id|=id_form][id$='mutations_id']");
            var use_isoform= $(protform).find("[id='id_use_isoform'],[id|=id_form][id$='use_isoform']");
            if ($(is_mutated).is(":checked")){
                $(mutations).show();
                console.log("f1");
                $(mutations).find('textarea,:button').each(function(){
                    $(this).prop('disabled',false);
                console.log("f2");
                });
            }else{
                $(mutations).hide();
                console.log("f1");
                $(mutations).find('textarea,:button').each(function(){
                    $(this).prop('disabled',true);
                console.log("f2");
                });
           
            };
    
            if ($(use_isoform).is(":checked")){
                console.log("f1");
                $(protform).find("[id|=id_form][id$='-isoform']").show().prop('disabled',false);
                console.log("f2");
            }else{
                $(protform).find("[id|=id_form][id$='-isoform']").hide().prop('disabled',true);
            };
          
        });
    };

       $(document).on('click',"[id='id_is_mutated'],[id|=id_form][id$='-is_mutated']",function(){

           if ($(document).find("[id|=id_form][id$='is_mutated']input:checked").length > 0){
               $("#mutations_id").show();
           } else {
               $("#mutations_id").hide();
           }
           var self=$(this);
           self.prop('disabled',true);
           var mut_block=$(this).parents("[id|=protform]").find("[id|=id_form][id$='mutations_id']");
           if ($(this).is(':checked')){
               $(mut_block).show();  
           }else{
               $(mut_block).hide();  
               $(mut_block).css("display","none");  
           }
           self.prop('disabled',false);
       });

       $(document).on('click',"[id='id_use_isoform'],[id|=id_form][id$='-use_isoform']",function(){

           var self=$(this);
           self.prop('disabled',true);
           var mut_iso=$(this).parents("[id|=protform]").find("[id|=id_form][id$='-isoform']");
           if ($(this).is(':checked')){
               $(mut_iso).show();  
           }else{
               $(mut_iso).hide();  
              // $(mut_iso).css("display","none");  
           }
           self.prop('disabled',false);
       });


$(document).ready(function(){
    $(document).protein_init_config()
    $.fn.exists = function () {
      return this.length !== 0;
    };
});
