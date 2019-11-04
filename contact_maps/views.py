import matplotlib# MANDATORY TO BE IN FIRST PLACE!!
matplotlib.use('Agg')# MANDATORY TO BE IN SECOND PLACE!!
from os.path import exists 
from django.shortcuts import render
from importlib.machinery import SourceFileLoader
from django.http import HttpResponse
import pandas as pd
from view.views import obtain_domain_url
from json import loads
from wsgiref.util import FileWrapper


def json_dict(path):
	"""Converts json file to pyhton dict."""
	json_file=open(path)
	json_str = json_file.read()
	json_data = loads(json_str)
	return json_data

def get_contacts_plots(request, itype = "all", ligandonly = "prt_lg", cluster = 3, rev = "norev"):
	"""
	Main view of contact plots
	"""
	mdsrv_url=obtain_domain_url(request)

	#Declaring dictionaries with types
	typelist =  {
		'sb' : 'salt bridge',
		"pc" : 'pi-cation',
		"ps" : 'pi-stacking',
		'ts' : 't-stacking',
		"vdw" : 'van der waals',
		'hp' : 'hydrophobic',
		"hbbb" : 'backbone to backbone HB',
		"hbsb" : 'sidechain to backbone HB',
		"hbss" : 'sidechain to sidechain HB',
		"hbls" : 'ligand to sidechain HB',
		"hblb" : 'ligand to backbone HB',
		"wb" : 'water bridge',
		"wb2" : 'extended water bridge',
		"hb" : 'hydrogen bond',
		'all' : 'total frequency',
	}
	hb_itypes = [
		("hbbb", 'backbone to backbone HB'),
		("hbsb" , 'sidechain to backbone HB'),
		("hbss" , 'sidechain to sidechain HB'),
		("hbls" , 'ligand to sidechain HB'),
		("hblb" , 'ligand to backbone HB'),
	]

	itypes_order = [
		("Polar/Electrostatic", 
			(
				("hb", "hydrogen bond"),
				("wb", "water bridge"),
				("wb2", "extended water bridge"),
				('sb', "salt bridge"),
				("pc", "pi-cation")
			)
		),
		("Non-polar", 
			(
				("vdw","van der waals"),
				('hp', "hydrophobic")
	   		)
	   	),
		("Stacking",
			(
				("ps", "pi-stacking"),
				('ts', "T-stacking")
			)
		)
	]

	basedir = "/protwis/sites/files/Precomputed/get_contacts_files/view_input_dataframe/"

	# Creating set_itypes, with all in case it is not still in it
	if not itype == "all":
		set_itypes = set(itype.split("_"))
	else: 
		set_itypes =  (("sb", "pc", "ps", "ts", "vdw", "hp", "hb", "hbbb", "hbsb", "hbss", "wb", "wb2", "hbls", "hblb"))

	#Creating itypes dictionary for selected types
	selected_itypes = { x:typelist[x] for x in set_itypes }

	# Loading variables
	variablesmod = SourceFileLoader("module.name", basedir + itype + "_" + ligandonly + "_" + rev + "_variables.py").load_module()
	number_heatmaps_list = variablesmod.number_heatmaps_list
	divwidth_list = variablesmod.divwidth_list
	div_list = variablesmod.div_list
	filenames_list = variablesmod.heatmap_filename_list

	#Path to json
	fpdir = "/dynadb/files/Precomputed/get_contacts_files/view_input_dataframe/%s_%s_jsons/%sclusters/" %  (itype, ligandonly, cluster)

	# Loading heatmap script if it exists. If not, load "no interactions" template instead
	if exists(filenames_list[0]):
		script_list = []
		for filename in filenames_list:
			with open(filename, 'r') as scriptfile:
				script = scriptfile.read()
			script_list.append(script)
	else:
		context = {
			'fpdir' : fpdir,
			'itype_code' : itype,
			'itype_name' : typelist[itype],
			'hb_itypes' : hb_itypes,
			'itypes_order' : itypes_order,
			'clusrange_all': list(range(2,21)),
			'selected_itypes' : selected_itypes,
			'itype_code' : itype,
			'ligandonly' : ligandonly,
			'rev' : rev,
			'itype_name' : typelist[itype],
			'cluster' : int(cluster),
		}
		return render(request, 'contact_maps/index_nodata.html', context)

	#Loading dynamics-cluster dictionary
	clustdict = json_dict(str("%s%s_%s_jsons/%sclusters/clustdict.json" % (basedir, itype, ligandonly, cluster)))

	# Loading dendrogram
	dendfile = ("%s%s_%s_dendrograms/%s_%s_%s_dendrogram_figure.html" % (basedir, itype, ligandonly, itype, str(cluster), ligandonly))
	dendr_figure = open(dendfile, 'r').read()

	first_sim = clustdict['cluster1'][0]

	# Send request 
	context={
		'clustdict' : clustdict,
		'fpdir' : fpdir,
		'itypes_order' : itypes_order,
		'itypes_dict' : typelist,
		'itype_code' : itype,
		'ligandonly' : ligandonly,
		'itype_name' : typelist[itype],
		'dendrogram' : dendr_figure,
		'hb_itypes' : hb_itypes,
		'script_list' : script_list, 
		'rev' : rev,
		'number_heatmaps_list' : number_heatmaps_list,
		'numbered_divs' : zip(number_heatmaps_list, div_list),
		'numbered_divwidths':zip(number_heatmaps_list, divwidth_list), 
		'clusrange_all': list(range(2,21)),
		'clusrange': list(range(1,int(cluster)+1)),
		'cluster' : int(cluster),
		'mdsrv_url':mdsrv_url
	}
	return render(request, 'contact_maps/index_h.html', context)

def get_csv_file(request, itype, ligandonly, rev):
	"""
	Processing informatino from get_contact plots to create and download a csv file
	"""

	basedir = "/protwis/sites/files/Precomputed/get_contacts_files/view_input_dataframe/"
	csv_name = basedir + itype + "_" + ligandonly + "_dataframe.csv"

	#Creating and downloading CSV file from df
	csvfile = FileWrapper(open(csv_name, "r"))
	response = HttpResponse(csvfile, content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename={0}'.format("ContactMaps-%s-%s.csv" % (itype, ligandonly))
	return response

def get_itype_help(request, foo):
	return render(request, 'contact_maps/itype_help.html')