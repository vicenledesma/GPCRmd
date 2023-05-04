# DJANGO REST-API DATABASE TOOLS ########################################################################################################################################

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics

from modules.api.serializers import *
from modules.dynadb.models import DyndbModel, DyndbProtein

class SearchAllPdbs(generics.ListAPIView):
    """
    Retrieve a list with all Pdbs codes in GPCRmd database. 
    """

    queryset = DyndbModel.objects.filter(is_published=True).values("pdbid").distinct().order_by("pdbid")
    serializer_class = AllPdbsSerializer
    
class SearchAllUniprots(generics.ListAPIView):
    """
    Retrieve a list with all Uniprot ids in GPCRmd database. 
    """

    queryset = DyndbProtein.objects.filter(is_published=True).values("uniprotkbac").distinct().order_by("uniprotkbac")
    serializer_class = AllUniprotsSerializer

# NOT API TOOLS ###############################################################################################################################################################

import os
from os.path import join
import shutil
import mimetypes
import json

from wsgiref.util import FileWrapper

from django.conf import settings
from django.http import StreamingHttpResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone

from modules.dynadb.models import DyndbFiles, DyndbFilesDynamics
from modules.api.models import AllDownloads

class AllDownloader:
    def __init__(self, dyns):
        """
        __init__ function to start and define parameters used on class Downloader. 

        Params: 
            > dyns --> List of dynamic ids. 
            > outfile --> Name of the directory. 
            > l_dyns --> List python type of dyns parameter.
            > tmp --> Path of the main temporary folder.
            > tmpdir --> Path of the temporary folder that will contain all the files.
            > dic_files --> Dictionary that contains dyn ids as keys and list of file ids as value.
            > dyn_path --> Path of the temporary folder that will contain the files of one dynamic.
        """
        self.dyns = dyns
        try:
            id = AllDownloads.objects.latest('id').id
        except:
            id = 0
        self.outfile = f"download_all_{id}"

    def prepare_file(self, *args, **kwargs):
        #Modify list of values
        dyns = self.dyns.replace(" ","") # Clean whitespaces e.g. 36
        self.l_dyns = dyns.split(",") # Create list

        #Create directory to store 
        self.tmp = settings.DOWNLOAD_FILES
        self.tmpdir = join(self.tmp,self.outfile) # .../tmp/GPCRmd_downloads/download_all_0
        os.makedirs(self.tmpdir, mode=0o777, exist_ok=True)

        # Seach the files
        self.dic_files = {}
        for dyn in self.l_dyns:
            self.dic_files[f"dyn_{dyn}"] = list(DyndbFilesDynamics.objects.filter(id_dynamics = dyn).values_list("id_files", flat=True)) #[10394, 10395, 10396, 10397, 10398, 10399, 10400]     10395_dyn_36.psf  |  NOT 10398_trj_36_xtc_bonds 

        # Get the files 
        for dyn_key in self.dic_files:
            dyn_path = join(self.tmpdir,dyn_key)
            os.makedirs(dyn_path, mode=0o777, exist_ok=True)
            file_ids = self.dic_files[dyn_key]
            for f_id in file_ids:
                file_path = list(DyndbFiles.objects.filter(id = f_id).values_list("filepath", flat=True))[0]
                file_name = list(DyndbFiles.objects.filter(id = f_id).values_list("filename", flat=True))[0]
                in_file = settings.MEDIA_ROOT[:-1] + file_path
                out_file = dyn_path + "/" + file_name
                print(in_file, out_file)
        # Copy the files 
                try:
                    shutil.copyfile(in_file, out_file)
                except:
                    print(f"        > File {in_file} not found")
                    continue

        # Zip them
        self.zip = f"{self.outfile}.zip"
        shutil.make_archive(self.tmpdir, 'zip', self.tmp, self.outfile)
        
        # Remove tmp directory
        shutil.rmtree(self.tmpdir)

        downfileobj=AllDownloads(
            tmpname = self.zip,
            dyn_ids = self.dyns,
            creation_timestamp = timezone.now(),
            created_by_dbengine = settings.DB_ENGINE,
            filepath = self.tmpdir + ".zip",
        )
        downfileobj.save()

    def download_file(self, *args, **kwargs):
        the_file = self.tmpdir + ".zip"
        filename = os.path.basename(the_file)
        chunk_size = 8192
        response = StreamingHttpResponse(
            FileWrapper(
                open(the_file, "rb"),
                chunk_size,
            ),
            content_type=mimetypes.guess_type(the_file)[0],
        )
        response["Content-Length"] = os.path.getsize(the_file)
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response

@csrf_protect
def download_all(request): 
    l_dyns = AllDownloader(request.GET['dyn_ids'])
    # try:
    l_dyns.prepare_file()
    data = dict()
    data["url"] = l_dyns.zip # CHANGE URL 
    return HttpResponse(json.dumps(data))
    # l_dyns.download_file()
    # except:
    #     return None

