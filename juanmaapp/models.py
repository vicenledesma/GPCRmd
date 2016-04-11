
import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

# Create your models here.

@python_2_unicode_compatible
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

@python_2_unicode_compatible
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

@python_2_unicode_compatible
class Formup(models.Model):
    UNIPROTid=models.CharField(max_length=20)
    iso=models.CharField(max_length=100)
    MUT=models.CharField(max_length=4)
    Nam=models.CharField(max_length=30)
    ORGAN=models.CharField(max_length=200)
    
    DescMOL=models.TextField()
    NETc=models.IntegerField()
    INCHI=models.TextField()
    inchik=models.CharField(max_length=27)
    SMI=models.TextField()
    resnamMOL=models.CharField(max_length=5)
    numMOL=models.IntegerField()

    MAINprot=models.TextField()
    MAINlig=models.TextField()

    IONresn=models.CharField(max_length=5)
    IONnum=models.IntegerField()

    COMtyp=models.CharField(max_length=50)
    idproT= models.CharField(max_length=50)
    idcoM=models.CharField(max_length=50)
    Msour=models.CharField(max_length=50)
    PDB=models.CharField(max_length=4)
    desc=models.TextField()
    mTEMP=models.TextField()
    
    METH=models.CharField(max_length=50)
    SOFT=models.CharField(max_length=50) 
    SOFTver=models.CharField(max_length=50) 
    ffield=models.CharField(max_length=50) 
    MEMB=models.CharField(max_length=50) 
    Solv=models.CharField(max_length=50) 
    PDBcoor=models.CharField(max_length=50) 
    PSF=models.CharField(max_length=50) 
    topPSF=models.CharField(max_length=50) 
    par=models.CharField(max_length=50) 
    DCD=models.CharField(max_length=50) 
   
@python_2_unicode_compatible
class DyndbAssayTypes(models.Model):
    type_name = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'dyndb_assay_types'

     

