# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm, Textarea



class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DyndbAssayTypes(models.Model):
    type_name = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'dyndb_assay_types'


class DyndbBinding(models.Model):
    id = models.ForeignKey('DyndbExpInteractionData', models.DO_NOTHING, db_column='id', primary_key=True)
    rvalue = models.FloatField()
    units = models.CharField(max_length=10)
    description = models.CharField(max_length=900, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'dyndb_binding'


class DyndbCannonicalProteins(models.Model):
    id_protein = models.ForeignKey('DyndbProtein', models.DO_NOTHING, db_column='id_protein', primary_key=True)

    class Meta:
        managed = False
        db_table = 'dyndb_cannonical_proteins'


class DyndbComplexCompound(models.Model):
    COMPOUND_TYPE=(
        (0,'Orthosteric ligand'),
        (1,'Allosteric ligand')
    )
    id_complex_exp=models.ForeignKey('DyndbComplexExp', models.DO_NOTHING, db_column='id_complex_exp', null=True)#
    #id_complex_exp_id =models.IntegerField(blank=True, null=True)
    id_compound = models.ForeignKey('DyndbCompound',models.DO_NOTHING, db_column='id_compound',null=True)  
    #id_compound_id = models.IntegerField(blank=True, null=True)
    type = models.SmallIntegerField(choices=COMPOUND_TYPE, default=0)#modified by juanma 
 
    class Meta:
        managed = True
        db_table = 'dyndb_complex_compound'
        unique_together = (('id_complex_exp', 'id_compound'))
 

class DyndbComplexExp(models.Model):
    update_timestamp = models.DateTimeField()
    creation_timestamp = models.DateTimeField()
    created_by_dbengine = models.CharField(max_length=40)
    last_update_by_dbengine = models.CharField(max_length=40)
    created_by = models.IntegerField(blank=True, null=True)
    last_update_by = models.IntegerField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        managed = True #this used to be False
        db_table = 'dyndb_complex_exp'


class DyndbComplexMolecule(models.Model):
#   COMPOUND_TYPE=(
#       (0,'Orthosteric ligand'),
#       (1,'Allosteric ligand'),
#       (2,'Crystallographic waters'),
#       (3,'Other')
#   )
    #type = models.SmallIntegerField(choices=COMPOUND_TYPE, default=0)#modified by juanma 
    id_complex_exp = models.ForeignKey(DyndbComplexExp, models.DO_NOTHING, db_column='id_complex_exp')
    update_timestamp = models.DateTimeField()
    creation_timestamp = models.DateTimeField()
    created_by_dbengine = models.CharField(max_length=40)
    last_update_by_dbengine = models.CharField(max_length=40)
    created_by = models.IntegerField(blank=True, null=True)
    last_update_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'dyndb_complex_molecule'


class DyndbComplexMoleculeMolecule(models.Model):
    COMPOUND_TYPE=(
        (0,'Orthosteric ligand'),
        (1,'Allosteric ligand')
    )
    type = models.SmallIntegerField(choices=COMPOUND_TYPE, default=0)#modified by juanma 
    id_complex_molecule = models.ForeignKey(DyndbComplexMolecule, models.DO_NOTHING, db_column='id_complex_molecule',null=False)
    id_molecule = models.ForeignKey('DyndbMolecule', models.DO_NOTHING, db_column='id_molecule',null=False)


    class Meta:
        managed = True
        db_table = 'dyndb_complex_molecule_molecule'
        unique_together = (('id_complex_molecule', 'id_molecule'),)


class DyndbComplexProtein(models.Model):
    id_protein = models.ForeignKey('DyndbProtein', models.DO_NOTHING, db_column='id_protein', null=True)
    id_complex_exp = models.ForeignKey(DyndbComplexExp, models.DO_NOTHING, db_column='id_complex_exp', null=True)

    class Meta:
        managed = True
        db_table = 'dyndb_complex_protein'
        unique_together = (('id_protein', 'id_complex_exp'),)


class DyndbCompound(models.Model):
    name = models.CharField(unique=True, max_length=60)
    iupac_name = models.CharField(max_length=500)
    pubchem_cid = models.IntegerField(unique=True, blank=True, null=True)
    chemblid = models.IntegerField(unique=True, blank=True, null=True)
    sinchi = models.TextField(null=True)
#    sinchikey = models.CharField(max_length=27, db_index=True,null=True)
    sinchikey = models.CharField(max_length=27, null=True)
    std_id_molecule = models.ForeignKey('DyndbMolecule', models.DO_NOTHING, db_column='std_id_molecule', blank=True, null=True)
    update_timestamp = models.DateTimeField()
    creation_timestamp = models.DateTimeField()
    created_by_dbengine = models.CharField(max_length=40)
    last_update_by_dbengine = models.CharField(max_length=40)
    created_by = models.IntegerField(blank=True, null=True)
    last_update_by = models.IntegerField(blank=True, null=True)
    id_ligand = models.ForeignKey('Ligand', models.DO_NOTHING, db_column='id_ligand', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        managed = True
        db_table = 'dyndb_compound'

class DyndbSubmission(models.Model):
    user_id=models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'dyndb_submission'



class DyndbSubmissionProtein(models.Model):
    submission_id = models.ForeignKey('DyndbSubmission',models.DO_NOTHING, db_column='submission_id',  blank=True, null=True) 
    protein_id = models.ForeignKey('DyndbProtein', models.DO_NOTHING, db_column='protein_id', blank=True, null=True)  
    int_id=models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'dyndb_submission_protein'
        unique_together = (('submission_id', 'protein_id'),('submission_id', 'int_id'),)

class DyndbSubmissionMolecule(models.Model):
    COMPOUND_TYPE=(
        (0,'Orthosteric ligand'),
        (1,'Allosteric ligand'),
        (2,'Crystallographic ions'),
        (3,'Crystallographic lipids'),
        (4,'Crystallographic waters'),
        (5,'Other co-crystalized item'),
        (6,'Bulk waters'),
        (7,'Bulk lipids'),
        (8,'Bulk ions'),
        (9,'Other bulk component'),
    )
    type = models.SmallIntegerField(choices=COMPOUND_TYPE, default=0, null=True, blank=True)#modified by juanma 
    submission_id = models.ForeignKey('DyndbSubmission', models.DO_NOTHING, db_column='submission_id', blank=True, null=True)
    molecule_id = models.ForeignKey('DyndbMolecule', models.DO_NOTHING, db_column='molecule_id', blank=True, null=True)
    not_in_model=models.NullBooleanField()
    int_id=models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'dyndb_submission_molecule'
        unique_together = (('submission_id', 'molecule_id'),('submission_id', 'int_id'),)

smol_to_dyncomp_type={0:1, 1:1, 2:0, 3:2, 4:3, 5:4, 6:3, 7:2, 8:0, 9:4} #dictionary from submission_molecule_type to Dynamics components type and Modeled components type (from 0 to 5)

class DyndbSubmissionModel(models.Model):
    submission_id = models.ForeignKey('DyndbSubmission', models.DO_NOTHING, db_column='submission_id', blank=True, null=True, unique=True)
    model_id=models.ForeignKey('DyndbModel', models.DO_NOTHING, db_column='model_id', blank=True, null=True) 

    class Meta:
        managed =True 
        db_table = 'dyndb_submission_model'

class DyndbDynamics(models.Model):
    id_model = models.ForeignKey('DyndbModel', models.DO_NOTHING, db_column='id_model', blank=True, null=True)
    id_dynamics_methods = models.ForeignKey('DyndbDynamicsMethods', models.DO_NOTHING, db_column='id_dynamics_methods', blank=True, null=True)
    software = models.CharField(max_length=30, blank=True, null=True)
    sversion = models.CharField(max_length=15, blank=True, null=True)
    ff = models.CharField(max_length=20, blank=True, null=True)
    ffversion = models.CharField(max_length=15, blank=True, null=True)
    id_assay_types = models.ForeignKey(DyndbAssayTypes, models.DO_NOTHING, db_column='id_assay_types', blank=True, null=True)
    description = models.CharField(max_length=150, blank=True, null=True)
    id_dynamics_membrane_types = models.ForeignKey('DyndbDynamicsMembraneTypes', models.DO_NOTHING, db_column='id_dynamics_membrane_types', blank=True, null=True)
    id_dynamics_solvent_types = models.ForeignKey('DyndbDynamicsSolventTypes', models.DO_NOTHING, db_column='id_dynamics_solvent_types', blank=True, null=True)
    solvent_num = models.IntegerField(blank=True, null=True)
    atom_num = models.IntegerField(blank=True, null=True)
    timestep = models.FloatField(blank=False, null=False)
    delta = models.FloatField(blank=False, null=False)
    update_timestamp = models.DateTimeField()
    creation_timestamp = models.DateTimeField()
    created_by_dbengine = models.CharField(max_length=40)
    last_update_by_dbengine = models.CharField(max_length=40)
    created_by = models.IntegerField(blank=True, null=True)
    last_update_by = models.IntegerField(blank=True, null=True)
    submission_id = models.ForeignKey(DyndbSubmission, models.DO_NOTHING, db_column='submission_id', blank=True, null=True) 
    is_published = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'dyndb_dynamics'

class DyndbDynamicsComponents(models.Model):
    MOLECULE_TYPE=(
        (0,'Ions'),
        (1,'Ligand'),
        (2,'Lipid'),
        (3,'Water'),
        (4,'Other')
    )    
    id_molecule = models.ForeignKey('DyndbMolecule', models.DO_NOTHING, db_column='id_molecule', null=True)
    id_dynamics = models.ForeignKey('DyndbDynamics', models.DO_NOTHING, db_column='id_dynamics', null=True)
    resname = models.CharField(max_length=4)
    numberofmol = models.PositiveSmallIntegerField(blank=True, null=True)
    type = models.SmallIntegerField( choices=MOLECULE_TYPE, default=0)

    class Meta:
        managed = True
        db_table = 'dyndb_dynamics_components'
        unique_together = (('id_dynamics', 'id_molecule', 'resname'),)

class DyndbModelComponents(models.Model):
    MOLECULE_TYPE=DyndbDynamicsComponents.MOLECULE_TYPE 

    id_molecule = models.ForeignKey('DyndbMolecule', models.DO_NOTHING, db_column='id_molecule',null=True)
    id_model = models.ForeignKey('DyndbModel', models.DO_NOTHING, db_column='id_model',null=True)
    resname = models.CharField(max_length=4)
    numberofmol = models.PositiveSmallIntegerField(blank=True, null=True)
    type = models.SmallIntegerField(choices=MOLECULE_TYPE, null=True, default=0)
  
    class Meta:
        managed = True
        db_table = 'dyndb_model_components'
        unique_together = (('id_model', 'id_molecule', 'resname'),)


class Model2DynamicsMoleculeType:
    def __init__(self):
        model_type_2_num = dict()
        for num,name in DyndbModelComponents.MOLECULE_TYPE:
            model_type_2_num[name] = num
        self.__dynamics_type_2_name = dict()
        for num,name in DyndbDynamicsComponents.MOLECULE_TYPE:
            self.__dynamics_type_2_name[num] = name
        self.__translation_dict = dict()
        for num,name in DyndbDynamicsComponents.MOLECULE_TYPE:
            self.__translation_dict[model_type_2_num[name]] = num 
    def translate(self,num,as_text=False):
        val = None
        if num in self.__translation_dict:
            val = self.__translation_dict[num]
            if as_text:
                val = self.__dynamics_type_2_name[val]     
        return val


class DyndbDynamicsMembraneTypes(models.Model):
    type_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'dyndb_dynamics_membrane_types'


class DyndbDynamicsMethods(models.Model):
    type_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'dyndb_dynamics_methods'


class DyndbDynamicsSolventTypes(models.Model):
    type_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'dyndb_dynamics_solvent_types'


class DyndbDynamicsTags(models.Model):
    id_dynamics_tag = models.ForeignKey('DyndbDynamicsTagsList', models.DO_NOTHING, db_column='id_dynamics_tag')
    id_dynamics = models.ForeignKey(DyndbDynamics, models.DO_NOTHING, db_column='id_dynamics')

    class Meta:
        managed = False
        db_table = 'dyndb_dynamics_tags'
        unique_together = (('id_dynamics_tag', 'id_dynamics'),)


class DyndbDynamicsTagsList(models.Model):
    name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'dyndb_dynamics_tags_list'


class DyndbEfficacy(models.Model):
    EFFICACY_TYPE=(
        (0,'Full Agonist'),
        (1,'Partial Agonist'),
        (2,'Antagonist'),
        (3, 'Inverse Agonist'),
        (4,'Other')
    )
    id = models.ForeignKey('DyndbExpInteractionData', models.DO_NOTHING, db_column='id', primary_key=True)
    rvalue = models.FloatField()
    units = models.CharField(max_length=10)
    description = models.CharField(max_length=900,blank=True, null=True)
    type = models.SmallIntegerField( choices=EFFICACY_TYPE, default=0)
    reference_id_compound = models.ForeignKey(DyndbCompound, models.DO_NOTHING, db_column='reference_id_compound',null=True)   
    id_functional = models.ForeignKey('DyndbFunctional', models.DO_NOTHING, blank=True, db_column='id_functional', null=True) 

    class Meta:
        managed = True
        db_table = 'dyndb_efficacy'


class DyndbExpInteractionData(models.Model):
    INTERACTION_TYPE=(
        (0, 'Functional'),
        (1, 'Binding'),
        (2, 'Efficacy')
    )
    id_complex_exp = models.ForeignKey(DyndbComplexExp, models.DO_NOTHING, db_column='id_complex_exp',null=True)
    type = models.SmallIntegerField( choices=INTERACTION_TYPE, default=0)
    protein1 = models.ForeignKey('DyndbProtein',  models.DO_NOTHING, db_column='protein1', related_name='DyndbExpInteractionData_protein1_fky', null=True)
    protein2 = models.ForeignKey('DyndbProtein', models.DO_NOTHING, db_column='protein2', blank=True, null=True, related_name='DyndbExpInteractionData_protein2_fky' )
    ligand1 = models.ForeignKey(DyndbCompound, models.DO_NOTHING, db_column='ligand1', blank=True, null=True, related_name='DyndbExpInteractionData_ligand1_fky')
    ligand2 = models.ForeignKey(DyndbCompound, models.DO_NOTHING,db_column='ligand2',   blank=True, null=True, related_name='DyndbExpInteractionData_ligand2_fky') 
    update_timestamp = models.DateTimeField()
    creation_timestamp = models.DateTimeField()
    created_by_dbengine = models.CharField(max_length=40)
    last_update_by_dbengine = models.CharField(max_length=40)
    created_by = models.IntegerField(blank=True, null=True)
    last_update_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True 
        db_table = 'dyndb_exp_interaction_data'


class DyndbExpProteinData(models.Model):
    EXP_PROTEIN_TYPES=(
        (0,'Activity'),
        (1, 'Others')
    )
    id_protein = models.ForeignKey('DyndbProtein', models.DO_NOTHING, db_column='id_protein', null=True)
    type = models.SmallIntegerField(choices=EXP_PROTEIN_TYPES, default=0)
    update_timestamp = models.DateTimeField()
    creation_timestamp = models.DateTimeField()
    created_by_dbengine = models.CharField(max_length=40)
    last_update_by_dbengine = models.CharField(max_length=40)
    created_by = models.IntegerField(blank=True, null=True)
    last_update_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'dyndb_exp_protein_data'


class DyndbFileTypes(models.Model):
    type_name = models.CharField(max_length=40, blank=True, null=True)
    extension = models.CharField(max_length=10, blank=True, null=True)
    is_coordinates = models.NullBooleanField()
    is_topology = models.NullBooleanField()
    is_trajectory = models.NullBooleanField()
    is_parameter = models.NullBooleanField()
    is_anytype = models.NullBooleanField()
    is_image = models.NullBooleanField()
    is_molecule = models.NullBooleanField()
    is_model = models.NullBooleanField()
    is_accepted = models.NullBooleanField()

    class Meta:
        managed = True
        db_table = 'dyndb_file_types'
        unique_together = (('type_name', 'extension'),)


class DyndbFiles(models.Model):
    filename = models.CharField(unique=True, max_length=80)
    id_file_types = models.ForeignKey(DyndbFileTypes,  models.DO_NOTHING, db_column='id_file_types', null=True ) 
    description = models.CharField(max_length=40, blank=True, null=True)
    update_timestamp = models.DateTimeField()
    creation_timestamp = models.DateTimeField()
    created_by_dbengine = models.CharField(max_length=40)
    last_update_by_dbengine = models.CharField(max_length=40)
    created_by = models.IntegerField(blank=True, null=True)
    last_update_by = models.IntegerField(blank=True, null=True)
    filepath = models.CharField(max_length=520, blank=True, null=True)
    url = models.CharField(max_length=520, blank=True, null=True)
    

    class Meta:
        managed = True
        db_table = 'dyndb_files'

class DyndbFilesDynamics(models.Model):
    file_types=(
        (0, 'Input coordinates'),
        (1, 'Input topology'),
        (2, 'Trajectory'),
        (3, 'Parameters'),
        (4, 'Others'),
    )
    id_dynamics = models.ForeignKey('DyndbDynamics', models.DO_NOTHING, db_column='id_dynamics',   null=True) 
    id_files = models.ForeignKey('DyndbFiles', models.DO_NOTHING,   db_column='id_files',  null=True)
    type = models.SmallIntegerField( choices=file_types, default=0)


    class Meta:
        managed = True
        db_table = 'dyndb_files_dynamics'
        unique_together = (('id_dynamics', 'id_files','type'),)

class DyndbSubmissionDynamicsFiles(models.Model):
    file_types = DyndbFilesDynamics.file_types
    submission_id = models.ForeignKey('DyndbSubmission',models.DO_NOTHING, db_column='submission_id',  blank=False, null=False)
    type = models.SmallIntegerField(choices=file_types,default=0,null=False)
    filename = models.CharField(unique=True, max_length=80)
    filepath = models.CharField(max_length=520, blank=False, null=False)
    url = models.CharField(max_length=520, blank=False, null=True)
    filenum = models.PositiveSmallIntegerField(null=False,default=0)
    framenum = models.PositiveIntegerField(null=True,default=None)
    class Meta:
        managed = True
        db_table = 'dyndb_submission_dynamics_files'
        unique_together = (('submission_id', 'filepath'),('submission_id','type','filenum'))

class DyndbFilesModel(models.Model):
    id_model = models.ForeignKey('DyndbModel', models.DO_NOTHING, db_column='id_model',unique=True)
    id_files = models.ForeignKey('DyndbFiles', models.DO_NOTHING, db_column='id_files',unique=True)

    class Meta:
        managed = True
        db_table = 'dyndb_files_model'


class DyndbFilesMolecule(models.Model):
    filemolec_types=(
        (0,'Molecule'),
        (1,'Image 100px'),
        (2,'Image 300px'),
        
    )
    id_molecule = models.ForeignKey('DyndbMolecule', models.DO_NOTHING, db_column='id_molecule', null=True)
    id_files = models.ForeignKey('DyndbFiles', models.DO_NOTHING, db_column='id_files', unique=True,null=True) 
    type = models.SmallIntegerField(choices=filemolec_types, default=0)
    

    class Meta:
        managed = True
        db_table = 'dyndb_files_molecule'
        unique_together = (('id_molecule', 'id_files'),('id_molecule','id_files','type'))


class DyndbFunctional(models.Model):
    id = models.ForeignKey(DyndbExpInteractionData, models.DO_NOTHING, db_column='id', primary_key=True)
    description = models.CharField(max_length=60)
    go_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dyndb_functional'


#      class DyndbIonicComponents(models.Model):
#          id_molecule = models.ForeignKey('DyndbMolecule', models.DO_NOTHING, db_column='id_molecule')
#          id_dynamics = models.ForeignKey(DyndbDynamics, models.DO_NOTHING, db_column='id_dynamics')
#          resname = models.CharField(max_length=4)
#          number = models.IntegerField(blank=True, null=True)
#      
#          class Meta:
#              managed = True
#              db_table = 'dyndb_ionic_components'
#              unique_together = (('id_dynamics', 'id_molecule'),)
#      

#  class DyndbMembraneComponents(models.Model):
#      id_molecule = models.ForeignKey('DyndbMolecule', models.DO_NOTHING, db_column='id_molecule')
#      id_dynamics = models.ForeignKey(DyndbDynamics, models.DO_NOTHING, db_column='id_dynamics')
#      resname = models.CharField(max_length=4)
#      number = models.IntegerField(blank=True, null=True)
#  
#      class Meta:
#          managed = True
#          db_table = 'dyndb_membrane_components'
#          unique_together = (('id_dynamics', 'id_molecule'),)
#  
   
class DyndbModel(models.Model):
    MODEL_TYPE=(
        (0,'Apoform (one single protein monomer)'),
        (1,'Complex')
    )
    SOURCE_TYPE=(
        (0,'X-ray'),
        (1,'NMR'),
        (2,'Docking'),
        (3,'MD'),
        (4,'Other')
    )

    name =  models.TextField(max_length=100,null=False,blank=False) 
    type = models.SmallIntegerField(choices=MODEL_TYPE, default=0) 
    id_protein = models.ForeignKey('DyndbProtein', models.DO_NOTHING,  db_column='id_protein',blank=True, null=True) 
    id_complex_molecule = models.ForeignKey(DyndbComplexMolecule, models.DO_NOTHING, db_column='id_complex_molecule',blank=True, null=True) 
    source_type = models.SmallIntegerField(choices=SOURCE_TYPE, default=0) 
    pdbid = models.CharField(max_length=6, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    model_creation_submission_id=models.ForeignKey('DyndbSubmission', models.DO_NOTHING, db_column='model_creation_submission_id', blank=True, null=True, unique=True)
    template_id_model = models.ForeignKey('self', models.DO_NOTHING, db_column='template_id_model', blank=True, null=True)
    update_timestamp = models.DateTimeField()
    creation_timestamp = models.DateTimeField()
    created_by_dbengine = models.CharField(max_length=40)
    last_update_by_dbengine = models.CharField(max_length=40)
    created_by = models.IntegerField(blank=True, null=True)
    last_update_by = models.IntegerField(blank=True, null=True)
    id_structure_model = models.ForeignKey('StructureModel', models.DO_NOTHING,db_column='id_structure_model',  blank=True, null=True) 
    is_published = models.BooleanField(default=False)
    
    class Meta:
        managed = True
        db_table = 'dyndb_model'

class DyndbModeledResidues(models.Model):
    SOURCE_TYPE=(
        (0,'X-ray'),
        (1,'NMR'),
        (2,'Ab-initio'),
        (3,'Homology'),
        (4,'Threading'),
        (5,'MD'),
        (6,'Other Computational Methods')
    )
    id_protein = models.ForeignKey('DyndbProtein',  models.DO_NOTHING, db_column='id_protein', null=True)
    id_model = models.ForeignKey('DyndbModel',  models.DO_NOTHING, db_column='id_model', null=True) 
    chain = models.CharField(max_length=1,blank=True, null=False,default='')
    segid = models.CharField(max_length=4,blank=True, null=False,default='')
    resid_from = models.SmallIntegerField()
    resid_to = models.SmallIntegerField()
    seq_resid_from = models.SmallIntegerField()
    seq_resid_to = models.SmallIntegerField()
    bonded_to_id_modeled_residues = models.ForeignKey('self', models.DO_NOTHING, db_column='bond_to_id_modeled_residues', blank=True, null=True, related_name='dyndbmodeledresidues_bond_to_id_modeled_residues')#!!!!
    pdbid = models.CharField(max_length=6, blank=True, null=True)
    source_type = models.SmallIntegerField(choices=SOURCE_TYPE, default=0)
    template_id_model = models.ForeignKey(DyndbModel, models.DO_NOTHING, db_column='template_id_model', blank=True, null=True, related_name='dyndbmodeledresidues_template_id_protein')

    class Meta:
        managed = True
        db_table = 'dyndb_modeled_residues'



class DyndbMolecule(models.Model):

    molecule_creation_submission_id = models.ForeignKey('DyndbSubmission', models.DO_NOTHING, db_column='molecule_creation_submission_id', blank=True, null=True)
    id_compound = models.ForeignKey(DyndbCompound, models.DO_NOTHING, db_column='id_compound' ) 
    description = models.CharField(max_length=80, blank=True, null=True)
    net_charge = models.SmallIntegerField(blank=True, null=True)
    inchi = models.TextField()
#    inchikey = models.CharField(max_length=27,db_index=True)
    inchikey = models.CharField(max_length=27,null=True)
    inchicol = models.SmallIntegerField()
    smiles = models.TextField(blank=True, null=True)
    update_timestamp = models.DateTimeField(blank=True, null=True)
    creation_timestamp = models.DateTimeField()
    created_by_dbengine = models.CharField(max_length=40)
    last_update_by_dbengine = models.CharField(max_length=40)
    created_by = models.IntegerField(blank=True, null=True)
    last_update_by = models.IntegerField(blank=True, null=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'dyndb_molecule'
        unique_together = (('inchikey', 'inchicol'),)
         

class DyndbOtherCompoundNames(models.Model):
    other_names = models.CharField(max_length=200)
    id_compound = models.ForeignKey(DyndbCompound, models.DO_NOTHING, db_column='id_compound')

    class Meta:
        managed = False
        db_table = 'dyndb_other_compound_names'
        unique_together = (('other_names', 'id_compound'),)


class DyndbOtherProteinNames(models.Model):
    other_names = models.CharField(max_length=100)
    id_protein = models.ForeignKey('DyndbProtein', models.DO_NOTHING, db_column='id_protein')

    class Meta:
        managed = False
        db_table = 'dyndb_other_protein_names'
        unique_together = (('other_names', 'id_protein'),)

class DyndbUniprotSpecies(models.Model):
    code = models.CharField(max_length=5,db_index=True,null=True,blank=False)
    kingdom = models.CharField(max_length=1,null=False)
    taxon_node = models.IntegerField(null=True)
    scientific_name = models.TextField(max_length=200,db_index=True,null=False,blank=False)
    class Meta:
      db_table = 'dyndb_uniprot_species'
    
class DyndbUniprotSpeciesAliases(models.Model):
    NAME_TYPE=(
        ('C','Common name'),
        ('S','Synonym'),
    )
    id_uniprot_species = models.ForeignKey(DyndbUniprotSpecies, on_delete=models.CASCADE, db_column='id_uniprot_species',null=False)
    name = models.TextField(max_length=200,db_index=True,null=False,blank=False)
    name_type = models.CharField(max_length=1,choices=NAME_TYPE,null=False)
    class Meta:
      db_table = 'dyndb_uniprot_species_aliases'
      unique_together = ("name", "id_uniprot_species")

class DyndbProtein(models.Model):
    uniprotkbac = models.CharField(max_length=10, blank=True, null=True)
    protein_creation_submission_id = models.ForeignKey('DyndbSubmission',models.DO_NOTHING, db_column='protein_creation_submission_id',  blank=True, null=True) 
    isoform = models.SmallIntegerField()
    is_mutated = models.BooleanField()
    name = models.TextField()
    update_timestamp = models.DateTimeField(null=True)
    creation_timestamp = models.DateTimeField()
    created_by_dbengine = models.CharField(max_length=40)
    last_update_by_dbengine = models.CharField(max_length=40)
    created_by = models.IntegerField(blank=True, null=True)
    last_update_by = models.IntegerField(blank=True, null=True)
    receptor_id_protein = models.ForeignKey('Protein', on_delete=models.DO_NOTHING, db_column='receptor_id_protein', blank=True, null=True)
    id_uniprot_species = models.ForeignKey(DyndbUniprotSpecies, on_delete=models.DO_NOTHING, db_column='id_uniprot_species',null=False)
    is_published = models.BooleanField(default=False)
    class Meta:
        managed = True
        db_table = 'dyndb_protein'


class DyndbProteinActivity(models.Model):
    id = models.ForeignKey(DyndbExpProteinData, models.DO_NOTHING, db_column='id', primary_key=True)
    rvalue = models.FloatField()
    units = models.CharField(max_length=10)
    description = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'dyndb_protein_activity'


class DyndbProteinCannonicalProtein(models.Model):
    id_protein = models.ForeignKey(DyndbProtein, models.DO_NOTHING, db_column='id_protein')
    id_cannonical_proteins = models.ForeignKey(DyndbCannonicalProteins, models.DO_NOTHING, db_column='id_cannonical_proteins')

    class Meta:
        managed = False
        db_table = 'dyndb_protein_cannonical_protein'
        unique_together = (('id_protein', 'id_cannonical_proteins'),)


class DyndbProteinMutations(models.Model):
    id_protein = models.ForeignKey(DyndbProtein, models.DO_NOTHING, db_column='id_protein', null=True)
    resid = models.SmallIntegerField(null=True)
    resletter_from = models.CharField(max_length=1, null=True)
    resletter_to = models.CharField(max_length=1, null=True)

    class Meta:
        managed = True
        db_table = 'dyndb_protein_mutations'
        unique_together = (('id_protein', 'resid', 'resletter_from', 'resletter_to'),)


class DyndbProteinSequence(models.Model):
    id_protein = models.ForeignKey(DyndbProtein, models.DO_NOTHING, db_column='id_protein', primary_key=True)
    sequence = models.TextField()
    length = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'dyndb_protein_sequence'


class DyndbReferences(models.Model):
    doi = models.CharField("DOI", help_text="Digital object identifier.", unique=True, max_length=80, blank=True, null=True)
    authors = models.CharField("Authors", help_text="List of the authors separated by semicolon.", max_length=600, blank=True, null=True)
    title = models.CharField("Title",help_text="Title of the paper.", max_length=900, blank=True, null=True)
             #institution = models.CharField(max_length=100, blank=True, null=True)
    pmid = models.IntegerField("PMID", help_text="PubMed identifier or PubMed unique identifier", unique=True, blank=True, null=True)
    journal_press = models.CharField("Journal or Press", help_text="Name of the Journal or Press in case of a book.", max_length=200, blank=True, null=True)
    issue = models.CharField("Issue", help_text="Issue number.",max_length=10, blank=True, null=True)
    volume = models.CharField("Volume", help_text="Volume number.", max_length=10, blank=True, null=True)
    pages = models.CharField("Pages", help_text="Initial and final pages of the publication separated by dash." ,max_length=16, blank=True, null=True)
    pub_year = models.SmallIntegerField("Publication year", help_text="Year of publication",blank=True, null=True)
    dbname = models.CharField(max_length=30, blank=True, null=True)
    url = models.URLField("URL", help_text="Uniform Resource Locator to the publication resource", max_length=250,  blank=True, null=True)
    update_timestamp = models.DateTimeField()
    creation_timestamp = models.DateTimeField()
    created_by_dbengine = models.CharField(max_length=40)
    last_update_by_dbengine = models.CharField(max_length=40)
    created_by = models.IntegerField(blank=True, null=True)
    last_update_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'dyndb_references'


class DyndbReferencesCompound(models.Model):
    id_compound = models.ForeignKey(DyndbCompound, models.DO_NOTHING, db_column='id_compound')
    id_references = models.ForeignKey(DyndbReferences, models.DO_NOTHING, db_column='id_references')

    class Meta:
        managed = False
        db_table = 'dyndb_references_compound'
        unique_together = (('id_compound', 'id_references'),)


class DyndbReferencesDynamics(models.Model):
    id_dynamics = models.ForeignKey(DyndbDynamics, models.DO_NOTHING, db_column='id_dynamics')
    id_references = models.ForeignKey(DyndbReferences, models.DO_NOTHING, db_column='id_references')

    class Meta:
        managed = False
        db_table = 'dyndb_references_dynamics'
        unique_together = (('id_dynamics', 'id_references'),)


class DyndbReferencesExpInteractionData(models.Model):
    id_exp_interaction_data = models.ForeignKey(DyndbExpInteractionData, models.DO_NOTHING, db_column='id_exp_interaction_data')
    id_references = models.ForeignKey(DyndbReferences, models.DO_NOTHING, db_column='id_references')

    class Meta:
        managed = False
        db_table = 'dyndb_references_exp_interaction_data'
        unique_together = (('id_exp_interaction_data', 'id_references'),)


class DyndbReferencesExpProteinData(models.Model):
    id_exp_protein_data = models.ForeignKey(DyndbExpProteinData, models.DO_NOTHING, db_column='id_exp_protein_data')
    id_references = models.ForeignKey(DyndbReferences, models.DO_NOTHING, db_column='id_references')

    class Meta:
        managed = False
        db_table = 'dyndb_references_exp_protein_data'
        unique_together = (('id_exp_protein_data', 'id_references'),)


class DyndbReferencesModel(models.Model):
    id_model = models.ForeignKey(DyndbModel, models.DO_NOTHING, db_column='id_model')
    id_references = models.ForeignKey(DyndbReferences, models.DO_NOTHING, db_column='id_references')

    class Meta:
        managed = False
        db_table = 'dyndb_references_model'
        unique_together = (('id_model', 'id_references'),)


class DyndbReferencesMolecule(models.Model):
    id_molecule = models.ForeignKey(DyndbMolecule, models.DO_NOTHING, db_column='id_molecule')
    id_references = models.ForeignKey(DyndbReferences, models.DO_NOTHING, db_column='id_references')

    class Meta:
        managed = False
        db_table = 'dyndb_references_molecule'
        unique_together = (('id_molecule', 'id_references'),)


class DyndbReferencesProtein(models.Model):
    id_protein = models.ForeignKey(DyndbProtein, models.DO_NOTHING, db_column='id_protein')
    id_references = models.ForeignKey(DyndbReferences, models.DO_NOTHING, db_column='id_references')

    class Meta:
        managed = False
        db_table = 'dyndb_references_protein'
        unique_together = (('id_protein', 'id_references'),)


class DyndbRelatedDynamics(models.Model):
    id_dynamics = models.ForeignKey(DyndbDynamics, models.DO_NOTHING, db_column='id_dynamics', primary_key=True)

    class Meta:
        managed = False
        db_table = 'dyndb_related_dynamics'


class DyndbRelatedDynamicsDynamics(models.Model):
    id_dynamics = models.ForeignKey(DyndbDynamics, models.DO_NOTHING, db_column='id_dynamics')
    id_related_dynamics = models.ForeignKey(DyndbRelatedDynamics, models.DO_NOTHING, db_column='id_related_dynamics')

    class Meta:
        managed = False
        db_table = 'dyndb_related_dynamics_dynamics'
        unique_together = (('id_dynamics', 'id_related_dynamics'),)
        



class Protein(models.Model):
    entry_name = models.CharField(unique=True, max_length=100)
    accession = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=200)
    sequence = models.TextField()
    family = models.ForeignKey('ProteinFamily', models.DO_NOTHING)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    residue_numbering_scheme = models.ForeignKey('ResidueGenericNumberingScheme', models.DO_NOTHING)
    sequence_type = models.ForeignKey('ProteinSequenceType', models.DO_NOTHING)
    source = models.ForeignKey('ProteinSource', models.DO_NOTHING)
    species = models.ForeignKey('Species', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'protein'


class ProteinAlias(models.Model):
    name = models.CharField(max_length=200)
    position = models.SmallIntegerField()
    protein = models.ForeignKey(Protein, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'protein_alias'


class ProteinAnomaly(models.Model):
    anomaly_type = models.ForeignKey('ProteinAnomalyType', models.DO_NOTHING)
    generic_number = models.ForeignKey('ResidueGenericNumber', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'protein_anomaly'
        unique_together = (('anomaly_type', 'generic_number'),)


class ProteinAnomalyRule(models.Model):
    amino_acid = models.CharField(max_length=1)
    negative = models.BooleanField()
    generic_number = models.ForeignKey('ResidueGenericNumber', models.DO_NOTHING)
    rule_set = models.ForeignKey('ProteinAnomalyRuleSet', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'protein_anomaly_rule'


class ProteinAnomalyRuleSet(models.Model):
    exclusive = models.BooleanField()
    protein_anomaly = models.ForeignKey(ProteinAnomaly, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'protein_anomaly_rule_set'


class ProteinAnomalyType(models.Model):
    slug = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'protein_anomaly_type'


class ProteinConformation(models.Model):
    protein = models.ForeignKey(Protein, models.DO_NOTHING)
    state = models.ForeignKey('ProteinState', models.DO_NOTHING)
    template_structure = models.ForeignKey('Structure', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'protein_conformation'


class ProteinConformationProteinAnomalies(models.Model):
    proteinconformation = models.ForeignKey(ProteinConformation, models.DO_NOTHING)
    proteinanomaly = models.ForeignKey(ProteinAnomaly, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'protein_conformation_protein_anomalies'
        unique_together = (('proteinconformation', 'proteinanomaly'),)


class ProteinConformationTemplateStructure(models.Model):
    protein_conformation = models.ForeignKey(ProteinConformation, models.DO_NOTHING)
    protein_segment = models.ForeignKey('ProteinSegment', models.DO_NOTHING)
    structure = models.ForeignKey('Structure', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'protein_conformation_template_structure'


class ProteinEndogenousLigands(models.Model):
    protein = models.ForeignKey(Protein, models.DO_NOTHING)
    ligand = models.ForeignKey(Ligand, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'protein_endogenous_ligands'
        unique_together = (('protein', 'ligand'),)


class ProteinFamily(models.Model):
    slug = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'protein_family'


class ProteinFusion(models.Model):
    name = models.CharField(unique=True, max_length=100)
    sequence = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'protein_fusion'


class ProteinFusionProtein(models.Model):
    protein = models.ForeignKey(Protein, models.DO_NOTHING)
    protein_fusion = models.ForeignKey(ProteinFusion, models.DO_NOTHING)
    segment_after = models.ForeignKey('ProteinSegment',   models.DO_NOTHING,  related_name='ProteinFusionProtein_segment_after_fky')
    segment_before = models.ForeignKey('ProteinSegment',   models.DO_NOTHING, related_name='ProteinFusionProtein_segment_before_fky')

    class Meta:
        managed = False
        db_table = 'protein_fusion_protein'


class ProteinSegment(models.Model):
    slug = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    fully_aligned = models.BooleanField()
    partial = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'protein_segment'


class ProteinSequenceType(models.Model):
    slug = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'protein_sequence_type'


class ProteinSet(models.Model):
    name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'protein_set'


class ProteinSetProteins(models.Model):
    proteinset = models.ForeignKey(ProteinSet, models.DO_NOTHING)
    protein = models.ForeignKey(Protein, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'protein_set_proteins'
        unique_together = (('proteinset', 'protein'),)


class ProteinSource(models.Model):
    name = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'protein_source'


class ProteinState(models.Model):
    slug = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'protein_state'


class ProteinWebLinks(models.Model):
    protein = models.ForeignKey(Protein, models.DO_NOTHING)
    weblink = models.ForeignKey('WebLink', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'protein_web_links'
        unique_together = (('protein', 'weblink'),)


class Publication(models.Model):
    title = models.TextField()
    authors = models.TextField()
    year = models.IntegerField()
    reference = models.TextField()
    journal = models.ForeignKey('PublicationJournal', models.DO_NOTHING)
    web_link = models.ForeignKey('WebLink', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'publication'


class PublicationJournal(models.Model):
    slug = models.CharField(max_length=200, blank=True, null=True)
    name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'publication_journal'


class ReleaseNotes(models.Model):
    date = models.DateField()
    html = models.TextField()

    class Meta:
        managed = False
        db_table = 'release_notes'


class ReleaseStatistics(models.Model):
    value = models.IntegerField()
    release = models.ForeignKey(ReleaseNotes, models.DO_NOTHING)
    statistics_type = models.ForeignKey('ReleaseStatisticsType', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'release_statistics'


class ReleaseStatisticsType(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'release_statistics_type'


class Residue(models.Model):
    sequence_number = models.SmallIntegerField()
    amino_acid = models.CharField(max_length=1)
    display_generic_number = models.ForeignKey('ResidueGenericNumber', models.DO_NOTHING, blank=True, null=True, related_name='Residue_display_generic_number_fky' )
    generic_number = models.ForeignKey('ResidueGenericNumber', models.DO_NOTHING, blank=True, null=True, related_name='Residue_generic_number_fky')
    protein_conformation = models.ForeignKey(ProteinConformation, models.DO_NOTHING)
    protein_segment = models.ForeignKey(ProteinSegment, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'residue'


class ResidueAlternativeGenericNumbers(models.Model):
    residue = models.ForeignKey(Residue, models.DO_NOTHING)
    residuegenericnumber = models.ForeignKey('ResidueGenericNumber', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'residue_alternative_generic_numbers'
        unique_together = (('residue', 'residuegenericnumber'),)


class ResidueGenericNumber(models.Model):
    label = models.CharField(max_length=10)
    protein_segment = models.ForeignKey(ProteinSegment, models.DO_NOTHING, blank=True, null=True)
    scheme = models.ForeignKey('ResidueGenericNumberingScheme', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'residue_generic_number'
        unique_together = (('scheme', 'label'),)


class ResidueGenericNumberEquivalent(models.Model):
    label = models.CharField(max_length=10)
    default_generic_number = models.ForeignKey(ResidueGenericNumber, models.DO_NOTHING)
    scheme = models.ForeignKey('ResidueGenericNumberingScheme', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'residue_generic_number_equivalent'
        unique_together = (('scheme', 'label'),)


class ResidueGenericNumberingScheme(models.Model):
    slug = models.CharField(max_length=20)
    short_name = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'residue_generic_numbering_scheme'


class ResidueSet(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'residue_set'


class ResidueSetResidue(models.Model):
    residueset = models.ForeignKey(ResidueSet, models.DO_NOTHING)
    residue = models.ForeignKey(Residue, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'residue_set_residue'
        unique_together = (('residueset', 'residue'),)


class Species(models.Model):
    latin_name = models.CharField(unique=True, max_length=100)
    common_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'species'


class Structure(models.Model):
    preferred_chain = models.CharField(max_length=20)
    resolution = models.DecimalField(max_digits=5, decimal_places=3)
    publication_date = models.DateField()
    representative = models.BooleanField()
    pdb_code = models.ForeignKey('WebLink', models.DO_NOTHING)
    pdb_data = models.ForeignKey('StructurePdbData', models.DO_NOTHING, blank=True, null=True)
    protein_conformation = models.ForeignKey(ProteinConformation, models.DO_NOTHING)
    publication = models.ForeignKey(Publication, models.DO_NOTHING, blank=True, null=True)
    state = models.ForeignKey(ProteinState, models.DO_NOTHING)
    structure_type = models.ForeignKey('StructureType', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'structure'


class StructureCoordinates(models.Model):
    description = models.ForeignKey('StructureCoordinatesDescription', models.DO_NOTHING)
    protein_segment = models.ForeignKey(ProteinSegment, models.DO_NOTHING)
    structure = models.ForeignKey(Structure, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'structure_coordinates'


class StructureCoordinatesDescription(models.Model):
    text = models.CharField(unique=True, max_length=200)

    class Meta:
        managed = False
        db_table = 'structure_coordinates_description'


class StructureEngineering(models.Model):
    description = models.ForeignKey('StructureEngineeringDescription', models.DO_NOTHING)
    protein_segment = models.ForeignKey(ProteinSegment, models.DO_NOTHING)
    structure = models.ForeignKey(Structure, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'structure_engineering'


class StructureEngineeringDescription(models.Model):
    text = models.CharField(unique=True, max_length=200)

    class Meta:
        managed = False
        db_table = 'structure_engineering_description'


class StructureFragment(models.Model):
    ligand = models.ForeignKey(Ligand, models.DO_NOTHING)
    pdbdata = models.ForeignKey('StructurePdbData', models.DO_NOTHING)
    residue = models.ForeignKey(Residue, models.DO_NOTHING)
    structure = models.ForeignKey(Structure, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'structure_fragment'


class StructureModel(models.Model):
    pdb = models.TextField()
    main_template = models.ForeignKey(Structure, models.DO_NOTHING)
    protein = models.ForeignKey(Protein, models.DO_NOTHING)
    state = models.ForeignKey(ProteinState, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'structure_model'


class StructureModelAnomalies(models.Model):
    reference = models.CharField(max_length=1)
    anomaly = models.ForeignKey(ProteinAnomaly, models.DO_NOTHING)
    homology_model = models.ForeignKey(StructureModel, models.DO_NOTHING)
    template = models.ForeignKey(Structure, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'structure_model_anomalies'


class StructureModelLoopTemplates(models.Model):
    homology_model = models.ForeignKey(StructureModel, models.DO_NOTHING)
    segment = models.ForeignKey(ProteinSegment, models.DO_NOTHING)
    template = models.ForeignKey(Structure, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'structure_model_loop_templates'


class StructureModelResidues(models.Model):
    sequence_number = models.IntegerField()
    origin = models.CharField(max_length=15)
    homology_model = models.ForeignKey(StructureModel, models.DO_NOTHING)
    residue = models.ForeignKey(Residue, models.DO_NOTHING)
    rotamer = models.ForeignKey('StructureRotamer', models.DO_NOTHING, blank=True, null=True)
    segment = models.ForeignKey(ProteinSegment, models.DO_NOTHING)
    template = models.ForeignKey(Structure, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'structure_model_residues'


class StructurePdbData(models.Model):
    pdb = models.TextField()

    class Meta:
        managed = False
        db_table = 'structure_pdb_data'


class StructureProteinAnomalies(models.Model):
    structure = models.ForeignKey(Structure, models.DO_NOTHING)
    proteinanomaly = models.ForeignKey(ProteinAnomaly, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'structure_protein_anomalies'
        unique_together = (('structure', 'proteinanomaly'),)


class StructureRotamer(models.Model):
    pdbdata = models.ForeignKey(StructurePdbData, models.DO_NOTHING)
    residue = models.ForeignKey(Residue, models.DO_NOTHING)
    structure = models.ForeignKey(Structure, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'structure_rotamer'


class StructureSegment(models.Model):
    start = models.IntegerField()
    end = models.IntegerField()
    protein_segment = models.ForeignKey(ProteinSegment, models.DO_NOTHING)
    structure = models.ForeignKey(Structure, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'structure_segment'


class StructureSegmentModeling(models.Model):
    start = models.IntegerField()
    end = models.IntegerField()
    protein_segment = models.ForeignKey(ProteinSegment, models.DO_NOTHING)
    structure = models.ForeignKey(Structure, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'structure_segment_modeling'


class StructureStabilizingAgent(models.Model):
    slug = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'structure_stabilizing_agent'


class StructureStabilizingAgents(models.Model):
    structure = models.ForeignKey(Structure, models.DO_NOTHING)
    structurestabilizingagent = models.ForeignKey(StructureStabilizingAgent, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'structure_stabilizing_agents'
        unique_together = (('structure', 'structurestabilizingagent'),)


class StructureType(models.Model):
    slug = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'structure_type'


class WebLink(models.Model):
    index = models.TextField()
    web_resource = models.ForeignKey('WebResource', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'web_link'
        unique_together = (('web_resource', 'index'),)


class WebResource(models.Model):
    slug = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    url = models.TextField()

    class Meta:
        managed = False
        db_table = 'web_resource'

