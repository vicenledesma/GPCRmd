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
import mimetypes
import json

from wsgiref.util import FileWrapper

from django.conf import settings
from django.http import StreamingHttpResponse, HttpResponse

from modules.dynadb.models import DyndbFilesDynamics

class Downloader:
    def __init__(self, dyns):
        """
        __init__ function to start and define parameters used on class Downloader. 

        Params: 
            > dyns --> List of dynamic ids. 
            > outfile --> Name of the output file. 
        """
        self.dyns = dyns
        self.outfile = ""

    def prepare_file(self, *args, **kwargs):
        #Modify list of values
        dyns = self.dyns.replace(" ","") # Clean whitespaces e.g. 36
        l_dyns = dyns.split(",") # Create list

        #Create directory to store 
        l_id_files = list(DyndbFilesDynamics.objects.filter(id_dynamics__in=l_dyns).values_list("id_files", flat=True)) #[10394, 10395, 10396, 10397, 10398, 10399, 10400]     10395_dyn_36.psf  |  NOT 10398_trj_36_xtc_bonds 

        # Seach the files

        # Remove the files that we do not want 

        # Get the files 
        
        #Copy the files 

        #Zip them
        int("s")
        self.outfile = settings.MEDIA_ROOT

    def download_file(self, *args, **kwargs):
        the_file = self.outfile
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

def download_all(request): 
    l_dyns = Downloader(request.GET['dyn_ids'])
    print(l_dyns)
    print(l_dyns.dyns)
    print(l_dyns.outfile)
    # try:
    l_dyns.prepare_file()


    # url = settings.MEDIA_ROOT
    #OUTDATA
    # data = dict()
    # data["url"] = url
    # return HttpResponse(json.dumps(data))
    #    
    l_dyns.download_file()
    # except:
    #     return None

