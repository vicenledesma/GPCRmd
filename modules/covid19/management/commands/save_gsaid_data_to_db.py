#Recommended to remove the following tables before starting: CovidMutations, CovidMutatedPosMutation, CovidSequencedGene, CovidSequence , CovidIsolate - in this order
from django.core.management.base import BaseCommand, CommandError
import os
import pandas as pd
from io import StringIO
from covid19.models import *
import datetime
import re
import csv
import tqdm
import gc
import pickle
from django.conf import settings

class Command(BaseCommand):
    help = "Saves info from GSAID to the database."
    def add_arguments(self, parser):
        parser.add_argument(
            '--skip_isolates',
            action='store_true',
            dest='skip_isolates',
            default=False,
            help='Do not save isolates data.',
        )
        parser.add_argument(
            '--skip_sequences',
            action='store_true',
            dest='skip_sequences',
            default=False,
            help='Do not save sequences data.',
        )
        parser.add_argument(
            '--skip_isolates_per_prot',
            action='store_true',
            dest='skip_isolates_per_prot',
            default=False,
            help='Do not save the dictionary relating final protein obj. with isolates with mutatons in that protein.',
        )


    def handle(self, *args, **options):

        if not options["skip_isolates"] or not options["skip_sequences"]:
            self.stdout.write(self.style.NOTICE("Loading data..."))
            #data_toni:
                ##genes=pd.read_csv( os.path.join( gsaid_path, "genes.csv.xz"))
                #genes_path=os.path.join( gsaid_path, "genes.csv.xz")
                ##seq=pd.read_csv( os.path.join( gsaid_path, "seq_2.csv.xz"),index_col=0)
                #seq_path= os.path.join( gsaid_path, "seq_2.csv.xz")
                ##isolates=pd.read_csv( os.path.join( gsaid_path, "isolates.csv.xz"))
                #isolates_path=os.path.join( gsaid_path, "isolates.csv.xz")

            gsaid_path=settings.MEDIA_ROOT + "Covid19Data/Data/gisaid/tables"
            
            #genesdf=pd.read_csv( os.path.join(gsaid_path,"genes_validseq.csv"))
            with open(os.path.join(gsaid_path,"genes_validseq.data"),"rb") as fh:
                genesdict=pickle.load(fh)

            #genes_path=os.path.join( gsaid_path, "genes.csv")
            isolates_path=os.path.join( gsaid_path, "isolates.csv")


    #        if not options["skip_sequences"]:
            seq_path= os.path.join( gsaid_path, "seq_2.csv.xz")
            seq_all=pd.read_csv( os.path.join( gsaid_path, "seq_2.csv.xz"),index_col=0)
            #seq_all_iter = pd.read_csv('train_2011_2012_2013.csv', sep=';', iterator=True, chunksize=20000000, low_memory = False)
            #seq_all = pd.concat(seq_all_iter, ignore_index=True)
            seq=seq_all.loc[(seq_all["mutation_description"] != "X Too different")& (seq_all["mutation_description"] != "X Undefined AA") & (seq_all["mutation_description"] != "WT")]
            del seq_all
            gc.collect()

        #Saving all isolates

        if not options["skip_isolates"]:
            self.stdout.write(self.style.NOTICE("Saving isolates..."))
            iso_skip_rows=0
            nrow=0
            total_iso=2095134 #just for the log

            #isolates=pd.read_csv( isolates_path)
            with open(isolates_path, 'r') as read_obj:
                csv_reader = csv.reader(read_obj)
                header=False
                for row in tqdm.tqdm(csv_reader,total=total_iso):
                    if not header:
                        header=row
                    else:
                        if nrow < iso_skip_rows:
                            nrow+=1
                            continue
                        nrow+=1
                        myisolate= pd.DataFrame([row],columns=header).iloc[0]
                        isolate_id=myisolate["isolate_id"]


                        (y,m,d)=myisolate["ymd"].split("-")
                        if int(m)==0:
                            m=1
                        if int(d)==0:
                            d=1
                        isolate_date=datetime.date(int(y),int(m),int(d))

                        #In case an entry with this isolate ID altrady existed, this would get it and update the info (some fields may have changed slightly)
                        isolateobj, created_isolateobj= CovidIsolate.objects.get_or_create(
                            isolate_name = myisolate["isolate_name"],
                            isolate_date = isolate_date,
                            isolate_id = myisolate["isolate_id"],
                            history = myisolate["history"],
                            tloc = myisolate["tloc"],
                            host = myisolate["host"],
                            originating_lab = myisolate["originating_lab"],
                            submitting_lab = myisolate["submitting_lab"],
                            submitter = myisolate["submitter"],
                            location = myisolate["location"],
                            isolate_type = myisolate["type"]
                        )


        




        if not options["skip_sequences"]:
            self.stdout.write(self.style.NOTICE("Prepare isolates data..."))
            alliso=CovidIsolate.objects.all()

            queryset_iso=CovidIsolate.objects.all().iterator()
            isolates_dict={}
            for i in queryset_iso:
                isolates_dict[i.isolate_id]=i

    #        iso_vals=alliso.values("isolate_id") 
    #        iso_ids=[e['isolate_id'] for e in iso_vals]
    #        isolates_dict=dict(zip(iso_ids,alliso)) 



            #Saving all genes except those that are 'bad' and those for which the sequence was not saved (seq was 'X Too different' or 'X Undefined AA')
            self.stdout.write(self.style.NOTICE("Saving genes, sequences and mutations..."))
            total_genes=len(genesdict)
            gene_skip_rows= 6890800
            nrow=0

            #for i,mygene in tqdm.tqdm(genesdf.iterrows(),total=total_genes):
            for mygene in tqdm.tqdm(genesdict,total=total_genes):
                if nrow < gene_skip_rows:
                    nrow+=1
                    continue
                nrow+=1

                #NSx should be ORFx - change this
                genename=mygene["gene"]
                nsnum=re.match("NS(\d+[a-zA-Z]?)",  genename)
                alt_name=None
                if nsnum:
                    alt_name=genename
                    genename="ORF" + nsnum.group(1)
                    if genename=="ORF3":
                        genename="ORF3a"

                finalprotobj, created_finalprotobj=CovidFinalProtein.objects.get_or_create(name=genename)


                gene_isolate=isolates_dict[mygene["isolate_id"]]

                #gene_isolate=CovidIsolate.objects.get(isolate_id= mygene["isolate_id"])
    #            if gene_isolate_filt:
    #                gene_isolate=gene_isolate_filt[0]
    #            else:
    #                continue
                
                # Create sequence ----------------
                seq_idx=mygene["seq_idx"]
                myseq=seq.loc[seq["seq_idx"]==seq_idx]
                if myseq.empty:
                    self.stdout.write(self.style.NOTICE("Empty seq for gene row %s" % nrow))
                    continue
                myseq=myseq.iloc[0]
                mut_descr=myseq["mutation_description"]

                seqobj, created_seqobj =CovidSequence.objects.get_or_create(
                    seq = myseq["seq"],
                    is_wt = False, #I filtered out WTs
                    seq_idx_table=myseq["seq_idx"]
                )

                # Create mutations associated to the sequence ----------------
                #if created_seqobj: #If the sequence is not new, we don't need to save the mutations again
                mut_li=mut_descr.split(",")
                adj=0
                for mut in mut_li:
                    mutmatch=re.match("([A-Z])(\d+)([A-Z])",  mut)
                    if mutmatch:
                        fromres=mutmatch.group(1)
                        mutpos=int(mutmatch.group(2))
                        tores=mutmatch.group(3)
                        corrected_mutpos=mutpos+adj

                        mutposobj, created_mutposobj=CovidMutatedPos.objects.get_or_create(
                            resid =corrected_mutpos,
                            #id_sequence =seqobj
                            id_final_protein=finalprotobj,
                            resletter_from = fromres,
                            resletter_to = tores,
                            )

                        mutrelobj, created_mutrelobj=CovidSequenceMutatedPos.objects.get_or_create(
                            id_mutated_pos= mutposobj,
                            id_sequence=seqobj,

                            )

                    elif mut.startswith("del"):
                        #print("deletion found at seq %s" % myseq["seq_idx"])
                        mutmatch=re.match("del(\d+)([A-Z]+)",  mut)
                        if mutmatch:
                            mutpos=mutmatch.group(1)
                            fromres=mutmatch.group(2)
                            tores=""
                        else:
                            self.stdout.write(self.style.NOTICE("Error in mutation %s of seq %s" % (mut,myseq["seq_idx"])))
                    elif mut.startswith("ins"):
                        #print("insertion found at seq %s" % myseq["seq_idx"])
                        mutmatch=re.match("ins(\d+)([A-Z]+)",  mut)
                        if mutmatch:
                            mutpos=mutmatch.group(1)
                            fromres=""
                            tores=mutmatch.group(2)
                            adj-=len(tores)
                        else:
                            self.stdout.write(self.style.NOTICE("Error in mutation %s of seq %s" % (mut,myseq["seq_idx"])))
                    else:
                        self.stdout.write(self.style.NOTICE("Unknown mutation %s of seq %s" % (mut,myseq["seq_idx"])))

                # Create gene ------------
                seqgeneobj,created_seqgeneobj=CovidSequencedGene.objects.get_or_create(
                        id_final_protein=finalprotobj,
                        alt_name=alt_name,
                        id_isolate=gene_isolate,
                        id_sequence=seqobj
                )
        #save isolates by final_protein
        if not options["skip_isolates_per_prot"]:
            self.stdout.write(self.style.NOTICE("Saving dicitonary relating final proteins with isolates that have mutations there..."))


            out_fp_iso_path=settings.MEDIA_ROOT + "Precomputed/covid19/finprot_to_isolates"
            if not os.path.isdir(out_fp_iso_path):
                os.mkdir(out_fp_iso_path)

            finprot_li=CovidFinalProtein.objects.all().values_list("name",flat=True)
            for finprot in finprot_li:
                #print(finprot)

                iter_iso=CovidIsolate.objects.filter(covidsequencedgene__id_final_protein__name=finprot).values_list("isolate_id",flat=True).iterator()
                isolates_in_prot=set()
                for iso in iter_iso:
                    isolates_in_prot.add(iso)

                finprot_nm=finprot.lower().replace(" ","_")
                with open(os.path.join(out_fp_iso_path,"%s.data"%finprot_nm),"wb") as fh:
                    pickle.dump(isolates_in_prot,fh)

                del isolates_in_prot
                del iter_iso
                gc.collect()
        self.stdout.write(self.style.NOTICE("Done! :)"))
 
