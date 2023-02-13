# -*- coding: utf-8 -*-

from django.urls import re_path, include
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings

from . import views

from haystack.query import SearchQuerySet
from haystack.views import SearchView
from .forms import MainSearchForm

from config.settings import TEMP_ROOT

sqs = SearchQuerySet().all()

app_name= 'dynadb'
urlpatterns = [
    re_path(r'^reset/$', views.reset_permissions, name="reset_permissions"),
    re_path(r'^testsub/$', views.testsub, name="testsub"),
    re_path(r'^testpng/$', views.testpng, name="testpng"),
    #re_path(r'^prueba_varios/$', TemplateView.as_view(template_name='dynadb/pruebamult_template.html'), name="prueba_varios"),
    #re_path(r'^profile_setting/$', views.profile_setting, name='profile_setting'),
    #re_path(r'^sub_sim/$', views.sub_sim, name='sub_sim'),
    #re_path(r'^name/$', views.get_name, name='name'),
#    re_path(r'^dyndbfiles/$', views.get_DyndbFiles, name='dyndbfiles'),
    re_path(r'^db_inputform/(?P<submission_id>[0-9]+)?/?$', views.db_inputformMAIN, name='db_inputform'),
    re_path(r'^before_db_inputform_prev_moddb_inputform/(?P<submission_id>[0-9]+)?/?$', views.db_inputformMAIN, name='before_db_inputform_prev_mod'),
#    re_path(r'^db_author_information/$', views.get_Author_Information, name='db_author_information'),
#    re_path(r'^db_dynamics/$', views.get_Dynamics, name='db_dynamics'),
#    re_path(r'^db_files/$', views.get_FilesCOMPLETE, name='db_files'),
#    re_path(r'^db_protein/$', views.get_ProteinForm, name='db_protein'),
#    re_path(r'^db_molecule/$', views.get_Molecule, name='db_molecule'),
#    re_path(r'^db_molecule/$', views.get_Molecule, name='db_molecule'),
#    re_path(r'^db_component/$', views.get_Component, name='db_component'),
#    re_path(r'^db_model/$', views.get_Model, name='db_model'),
#    re_path(r'^db_compoundform/$', views.get_CompoundForm, name='db_compoundform'),
#    re_path(r'^your_name/$', views.get_name, name='your_name'),
#    re_path(r'^thanks/$', views.get_name, name='thanks'),
#    re_path(r'^admin/', admin.site.urls),
    re_path(r'^protein/(?P<submission_id>[0-9]+)/$', views.PROTEINview, name='protein'),
    re_path(r'^protein/(?P<submission_id>[0-9]+)/delete/$', views.delete_protein, name='delete_protein'),
    re_path(r'^protein/get_data_upkb/?([A-Z0-9-]+)?$', views.protein_get_data_upkb, name='protein_get_data_upkb'),
    re_path(r'^protein/download_specieslist/$', views.download_specieslist, name='protein_download_specieslist'),
    re_path(r'^protein/get_specieslist/$', views.get_specieslist, name='protein_get_specieslist'),
    re_path(r'^protein/get_mutations/$', views.get_mutations_view, name='protein_get_mutations'),
    re_path(r'^protein/(?P<alignment_key>[0-9]+)/alignment/$', views.show_alig, name='show_alig'),
    re_path(r'^protein/id/(?P<protein_id>[0-9]+)/$',views.query_protein, name='query_protein'),
    re_path(r'^protein/id/(?P<protein_id>[0-9]+)/fasta$',views.query_protein_fasta, name='query_protein_fasta'),
    re_path(r'^molecule/id/(?P<molecule_id>[0-9]+)/$',views.query_molecule, name='query_molecule'),
    re_path(r'^molecule/id/(?P<molecule_id>[0-9]+)/sdf$',views.query_molecule_sdf,name='query_molecule_sdf'),
    re_path(r'^compound/id/(?P<compound_id>[0-9]+)/$',views.query_compound, name='query_compound'),
    re_path(r'^model/id/(?P<model_id>[0-9]+)/$',views.query_model, name='query_model'),
    re_path(r'^dynamics/id/(?P<dynamics_id>[0-9]+)/$',views.query_dynamics, name='query_dynamics'),
    re_path(r'^complex/id/(?P<complex_id>[0-9]+)/$',views.query_complex, name='query_complex'),
    re_path(r'^references/$', views.REFERENCEview, name='references'),
    re_path(r'^REFERENCEfilled/(?P<submission_id>[0-9]+)/$', views.REFERENCEview, name='REFERENCEfilled'),
    re_path(r'^PROTEINfilled/(?P<submission_id>[0-9]+)/$', views.PROTEINview, name='PROTEINfilled'),
    re_path(r'^submission_summary/(?P<submission_id>[0-9]+)/$', views.submission_summaryiew, name='submission_summary'),
    re_path(r'^protein_summary/(?P<submission_id>[0-9]+)/$', views.protein_summaryiew, name='protein_summary'),
    re_path(r'^molecule_summary/(?P<submission_id>[0-9]+)/$', views.molecule_summaryiew, name='molecule_summary'),
    re_path(r'^model_summary/(?P<submission_id>[0-9]+)/$', views.model_summaryiew, name='model_summary'),
    re_path(r'^molecule/(?P<submission_id>[0-9]+)/$', views.SMALL_MOLECULEview, name='molecule'),
    re_path(r'^molecule/(?P<submission_id>[0-9]+)/delete/$', views.delete_molecule, name='delete_molecule'),
    re_path(r'^moleculereuse/(?P<submission_id>[0-9]+)/(?P<model_id>[0-9]+)/$', views.SMALL_MOLECULEreuseview, name='moleculereuse'),
    re_path(r'^moleculereuse/(?P<submission_id>[0-9]+)/(?:[0-9]+/)?generate_properties/$', views.generate_molecule_properties, name='generate_molecule_properties_reuse'),
    re_path(r'^moleculereuse/(?P<submission_id>[0-9]+)/(?:[0-9]+/)?delete/$', views.delete_molecule, name='delete_molecule_reuse'),
    re_path(r'^moleculereuse/(?P<submission_id>[0-9]+)/(?:[0-9]+/)?get_compound_info_pubchem/$', views.get_compound_info_pubchem, name='get_compound_info_pubchem_reuse'),
    re_path(r'^moleculereuse/(?P<submission_id>[0-9]+)/(?:[0-9]+/)?get_compound_info_chembl/$', views.get_compound_info_chembl, name='get_compound_info_chembl_reuse'),
    re_path(r'^moleculereuse/(?P<submission_id>[0-9]+)/(?:[0-9]+/)?submitpost/$', views.submitpost_view, name='submitpost_reuse'),
    #re_path(r'^moleculereuse/open_pubchem/$', views.open_pubchem, name='molecule_open_pubchem_reuse'),
    #re_path(r'^moleculereuse/open_chembl/$', views.open_chembl, name='molecule_open_chembl_reuse'),
    re_path(r'^moleculereuse/(?:[0-9]+/)open_pubchem/$', views.open_pubchem, name='molecule_open_pubchem_reuse'),
    re_path(r'^moleculereuse/(?:[0-9]+/)open_chembl/$', views.open_chembl, name='molecule_open_chembl_reuse'),
    re_path(r'^molecule/(?P<submission_id>[0-9]+)/submitpost/$', views.submitpost_view, name='submitpost'),
    re_path(r'^molecule/(?P<submission_id>[0-9]+)/generate_properties/$', views.generate_molecule_properties, name='generate_molecule_properties'),
    re_path(r'^molecule/(?P<submission_id>[0-9]+)/get_compound_info_pubchem/$', views.get_compound_info_pubchem, name='get_compound_info_pubchem'),
    re_path(r'^molecule/(?P<submission_id>[0-9]+)/get_compound_info_chembl/$', views.get_compound_info_chembl, name='get_compound_info_chembl'),
    re_path(r'^molecule/open_pubchem/$', views.open_pubchem, name='molecule_open_pubchem'),
    re_path(r'^molecule/open_chembl/$', views.open_chembl, name='molecule_open_chembl'),
    re_path(r'^molecule2/(?P<submission_id>[0-9]+)/$', views.SMALL_MOLECULEview2, name='molecule2'),
    re_path(r'^MOLECULEfilled/(?P<submission_id>[0-9]+)/$', views.SMALL_MOLECULEview, name='MOLECULEfilled'),
    re_path(r'^MOLECULEfilled2/$', views.SMALL_MOLECULEview2, name='MOLECULEfilled2'),
    re_path(r'^model/(?P<submission_id>[0-9]+)/$', views.MODELview, name='model'),
    re_path(r'^(?P<form_type>model|dynamics)/(?P<submission_id>[0-9]+)/check_pdb_molecules/$', views.pdbcheck_molecule, name='pdbcheck_molecule'),
    re_path(r'^(?P<form_type>dynamics)reuse/(?P<submission_id>[0-9]+)/(?:[0-9]+/)?check_pdb_molecules/$', views.pdbcheck_molecule, name='pdbcheck_molecule'), #######
    re_path(r'^(?P<form_type>model|dynamics)/(?P<submission_id>[0-9]+)/get_submission_molecule_info/$', views.get_submission_molecule_info, name='get_submission_molecule_info'),
    re_path(r'^model/(?P<submission_id>[0-9]+)/ajax_pdbchecker/$', views.pdbcheck, name='pdbcheck'),
    re_path(r'^model/(?P<submission_id>[0-9]+)/search_top/$',views.search_top,name='search_top'), #keep this one in a merge
    re_path(r'^model/(?P<submission_id>[0-9]+)/upload_model_pdb/$', views.upload_model_pdb, name='upload_model_pdb'),
    re_path(r'^modelreuse/(?P<submission_id>-?[0-9]+)/(?:[0-9]+/)?$', views.MODELreuseview, name='modelreuse'),
    re_path(r'^proteinreuse/(?P<submission_id>[0-9]+)/(?:[0-9]+/)?$', views.PROTEINreuseview, name='proteinreuse'),
#    re_path(r'^moleculereuse/(?P<submission_id>[0-9]+)/(?P<model_id>[0-9]+)/$', views.SMALL_MOLECULEreuseview, name='moleculereuse'),
#    re_path(r'^modelrow/$', views.MODELrowview, name='modelrow'),
    re_path(r'^modelreuserequest/(?P<model_id>[0-9]+)/$', views.MODELreuseREQUESTview, name='modelreuserequest'),
    re_path(r'^MODELfilled/(?P<submission_id>[0-9]+)/$', views.MODELview, name='MODELfilled'),
    #re_path(r'^ajax_pdbchecker/(?P<submission_id>[0-9]+)/$', views.pdbcheck, name='pdbcheck'), 
    re_path(r'^search/$', SearchView(template=f'{TEMP_ROOT}/dynadb/search/search.html', searchqueryset=sqs, form_class=MainSearchForm),name='haystack_search'),
    re_path(r'^ajaxsearch/',views.ajaxsearcher,name='ajaxsearcher'),
    re_path(r'^empty_search/',views.emptysearcher,name='emptysearcher'),
    re_path(r'^autocomplete/',views.autocomplete,name='autocomplete'),
    re_path(r'^advanced_search/$', views.NiceSearcher,name='NiceSearcher'),
    #re_path(r'^search_top/(?P<submission_id>[0-9]+)/$',views.search_top,name='search_top'),
    re_path(r'^dynamics/(?P<submission_id>[0-9]+)/$', views.DYNAMICSview, name='dynamics'),
    re_path(r'^dynamics/(?P<submission_id>[0-9]+)/(?:[0-9]+/)?upload_files/((?P<trajectory>traj)/)?$', views.upload_dynamics_files, name='dynamics_upload_files'),
    re_path(r'^dynamicsreuse/(?P<submission_id>[0-9]+)/(?:[0-9]+/)?upload_files/((?P<trajectory>traj)/)?$', views.upload_dynamics_files, name='dynamics_upload_files'),
    re_path(r'^dynamics/(?P<submission_id>[0-9]+)/check_trajectories/$', views.check_trajectories, name='dynamics_check_trajectories'),
    re_path(r'^dynamics/do_analysis/$', views.do_analysis, name='do_analysis'),
#    re_path(r'^dynamicsreuse/(?P<submission_id>[0-9]+)/(?P<model_id>[0-9]+)/$', views.DYNAMICSreuseview, name='dynamicsreuse'),
    re_path(r'^dynamicsreuse/(?P<submission_id>[0-9]+)/(?P<model_id>[0-9]+)/$', views.DYNAMICSview, name='dynamicsreuse'),
    re_path(r'^DYNAMICSfilled/(?P<submission_id>[0-9]+)/$', views.DYNAMICSview, name='DYNAMICSfilled'),
    #re_path(r'^form/$', views.get_formup, name='form'),
    re_path(r'^model/carousel/(?P<model_id>[0-9]+)/$', views.carousel_model_components, name='carousel_model_components'),
    re_path(r'^dynamics/carousel/(?P<dynamics_id>[0-9]+)/$', views.carousel_dynamics_components, name='carousel_dynamics_components'),
    #re_path(r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}), #this line shouldnt be here
    re_path(r'^submitted/(?P<submission_id>[0-9]+)/$', views.SUBMITTEDview, name='submitted'),
    re_path(r'^close_submission/(?P<submission_id>[0-9]+)/$', views.close_submission, name='close_submission'),
    re_path(r'^datasets/$', views.datasets, name='datasets'),
    re_path(r'^table/$', views.table, name='table'),
    re_path(r'^blank/$', TemplateView.as_view(template_name="dynadb/blank.html"), name='blank'),
    re_path(r'^step0/$', views.step0, name='step0'),
    re_path(r'^step1/(?P<submission_id>[0-9]+)/$', views.step1, name='step1'),
    re_path(r'^step2/(?P<submission_id>[0-9]+)/$', views.step2, name='step2'),
    re_path(r'^step3/(?P<submission_id>[0-9]+)/$', views.step3, name='step3'),
    re_path(r'^step4/(?P<submission_id>[0-9]+)/$', views.step4, name='step3'),
    re_path(r'^step5/(?P<submission_id>[0-9]+)/$', views.step5, name='step5'),
    re_path(r'^step1_submit/(?P<submission_id>[0-9]+)/$', views.step1_submit, name='step1_submit'),
    re_path(r'^step2_submit/(?P<submission_id>[0-9]+)/$', views.step2_submit, name='step2_submit'),
    re_path(r'^step3_submit/(?P<submission_id>[0-9]+)/$', views.step3_submit, name='step3_submit'),
    re_path(r'^step4_submit/(?P<submission_id>[0-9]+)/$', views.step4_submit, name='step4_submit'),
    re_path(r'^step5_submit/(?P<submission_id>[0-9]+)/$', views.step5_submit, name='step5_submit'),
    re_path(r'^submission_summary/(?P<submission_id>[0-9]+)/$', views.submission_summaryiew, name='submission_summary'),
    re_path(r'^find_smalmols/(?P<submission_id>[0-9]+)/$', views.find_smalmols, name='find_smalmols'),
    re_path(r'^find_prots/(?P<submission_id>[0-9]+)/$', views.find_prots, name='find_prots'),
    re_path(r'^delete_submission/(?P<submission_id>[0-9]+)/$', views.delete_submission, name='delete_submission'),
    re_path(r'^close__submission/(?P<submission_id>[0-9]+)/$', views.close__submission, name='close__submission'),
    re_path(r'^smalmol_info/', views.smalmol_info_url, name='smalmol_info'),
    re_path(r'^prot_info/', views.prot_info, name='prot_info'),
    re_path(r'^get_alignment/', views.get_alignment_URL, name='get_alignment_URL'),
    re_path(r'^publications/(?P<ref_id>[0-9]+)/$', views.dyns_in_ref, name='dyns_in_ref'),
    #re_path(r'^step2/(?P<submission_id>[0-9]+)/$', views.step2, name='step2'),
    ]

#    re_path(r'^some_temp/$', views.some_view, name='some_temp')
#    re_path(r'^prueba_varios/$', views.profile_setting, name='PRUEBA_varios'),

""" if settings.DEBUG:
    urlpatterns += ('',
        re_path(r'^files/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        re_path(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    )
else:
    if settings.FILES_NO_LOGIN:
        serve_files_func = views.serve_submission_files_no_login
    else:
        serve_files_func = views.serve_submission_files
    urlpatterns += ('',
        re_path(r'^files/(?P<obj_folder>[^/\\]+)/(?P<submission_folder>[^/\\]+)/(?P<path>.*)$', serve_files_func, name='serve_submission_files'),
    )
 """
