from modules.dynadb.models import DyndbModel, DyndbProtein
from rest_framework import serializers

class AllPdbsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DyndbModel
        fields = ['pdbid']

class AllUniprotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DyndbProtein
        fields = ['uniprotkbac']
        # depth = 1



        

    
