from modules.dynadb.models import DyndbDynamics, DyndbModel, DyndbProtein
from rest_framework import serializers
import copy
from collections import OrderedDict

# search_allpdbs
class AllPdbsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DyndbModel
        fields = ['pdbid']

# search_pdbs/ & # search_uniprots/
class DynsSerializer(serializers.ModelSerializer):
    dyn_id = serializers.IntegerField(source='id') 
    class Meta:
        model = DyndbDynamics
        fields = ['dyn_id']

# search_alluniprots
class AllUniprotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DyndbProtein
        fields = ['uniprotkbac']
        # depth = 1


        

        

    
