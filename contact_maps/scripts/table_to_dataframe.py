import matplotlib# MANDATORY TO BE IN FIRST PLACE!!
matplotlib.use('Agg')# MANDATORY TO BE IN SECOND PLACE!!
from sys import argv,exit
import pandas as pd
from  numpy import array
from json import loads
from  plotly.figure_factory import create_dendrogram
from  plotly.offline import plot
import numpy as np
import os
import re
from math import pi
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, TapTool, CustomJS, BasicTicker, ColorBar, ColumnDataSource, LinearColorMapper, PrintfTickFormatter
from bokeh.transform import transform
from scipy.cluster.hierarchy import linkage, fcluster

############
## Functions
############

# Be careful with this!!! Put here only because some false-positive warnings from pandas
import warnings
warnings.filterwarnings('ignore')

def json_dict(path):
    """Converts json file to pyhton dict."""
    json_file=open(path)
    json_str = json_file.read()
    json_data = loads(json_str)
    return json_data

def improve_receptor_names(df_ts,compl_data):
    """
    Parses the dataframe to create the data source of the plot. When defining a name for each dynamics entry: if there is any other dynamics in the 
    datadrame that is created fromt he same pdb id and ligand, all these dynamics will indicate the dynamics id
    """
    recept_info={}
    recept_info_order={
        "upname":0,
        "resname":1,
        "dyn_id":2,
        "prot_id":3,
        "comp_id":4,
        "prot_lname":5,
        "pdb_id":6,
        "lig_lname":7,
        "struc_fname":8,
        "struc_f":9,
        "traj_fnames":10,
        "traj_f":11,
        "delta":12
    }
    taken_protlig={}
    index_dict={}
    dyn_gpcr_pdb={}
    for recept_id in df_ts['Id']:
        dyn_id=recept_id
        upname=compl_data[recept_id]["up_name"]
        resname=compl_data[recept_id]["lig_sname"]
        lig_lname=compl_data[recept_id]["lig_lname"]
        prot_id=compl_data[recept_id]["prot_id"]
        comp_id=compl_data[recept_id]["comp_id"]
        prot_lname=compl_data[recept_id]["prot_lname"]
        pdb_id=compl_data[recept_id]["pdb_id"]
        struc_fname=compl_data[recept_id]["struc_fname"]
        struc_f=compl_data[recept_id]["struc_f"]
        traj_fnames=compl_data[recept_id]["traj_fnames"]
        traj_f=compl_data[recept_id]["traj_f"]
        delta=compl_data[recept_id]["delta"]
        if pdb_id:
            prot_lig=(pdb_id,resname)
        else:
            prot_lig=(upname,resname)

        if prot_lig in taken_protlig:
            name_base=taken_protlig[prot_lig]["recept_name"]
            #recept_name=name_base +" (dynID:"+str(dyn_id)+")"
            recept_name = name_base

        else:
            recept_name=prot_lname+" ("+prot_lig[0]+")"

#            if bool(prot_lig[1]):
 #               recept_name = recept_name + " + "+prot_lig[1]
            taken_protlig[prot_lig]={"recept_name":recept_name,"id_added":False}
        recept_info[dyn_id]=[upname, resname,dyn_id,prot_id,comp_id,prot_lname,pdb_id,lig_lname,struc_fname,struc_f,traj_fnames,traj_f,delta]
        index_dict[recept_id]=recept_name 
        dyn_gpcr_pdb[recept_name]=compl_data[recept_id]["gpcr_pdb"]
    df_ts['Name'] = list(map(lambda x: index_dict[x], df_ts['Id']))
    return(recept_info,recept_info_order,df_ts,dyn_gpcr_pdb,index_dict)

def removing_entries(df, itypes, main_itype):
    """
    Filter same-helix and low-frequency interactions. 
    """    
    positions = dict()
    counter = 0
    dict_freqs = {}
    pos_topreserve = set()
    
    #Filtering same-helix contacts
    helixpattern = re.compile(r"""^(..)\w+\s+\1""")#For detecting same-helix contacts, the ones like 1.22x22 1.54x54
    helixfilter = df['Position'].str.contains(helixpattern)
    df = df[~helixfilter]
            
    # Preserve positions which interaction frequency for this type reach, at mean, 0.1 (or 10 if working on percentages)
    df['mean_row'] = df.mean(axis = 1, numeric_only = True)
    pos_topreserve = set(df['Position'][ (df['mean_row'] > 10) & (df['itype'] == main_itype) ])
    df.drop('mean_row', 1, inplace = True)
    df = df[df['Position'].isin(pos_topreserve)]
     
    return(df)

def stack_matrix(df, itypes):
    """
    Converts matrix in a stacked version: columns now are Position, dynid and itypes and rows all 
    frequencies by position and dyind
    """
    df_ts = 1
    for itype in itypes:
        df_type = df[df["itype"] == itype]
        df_type.drop('itype', 1, inplace = True)
        df_type.set_index('Position', inplace = True)
        df_ts_type = df_type.transpose().stack().rename(itype).reset_index()

        if type(df_ts) == int:
            df_ts = df_ts_type
        else:
            df_ts = pd.merge( df_ts, df_ts_type, how ='outer', on=["level_0", 'Position'])

    df_ts = df_ts.fillna(0.0) # Fill posible NaN in file
    df_ts.rename(columns={"level_0": "Id"}, inplace=True)
    return df_ts
    
def adapt_to_marionas(df):
    """
    This function comprises a series of operations to adapt the new tsv format to Mariona's original scripts.
    Also returns a dictionary
    """

    #Merging toghether both contacting aminoacid Ids
    df['Position'] = df.Position1.str.cat(df.Position2, sep = " ")
    df = df.drop(df.columns[[0, 1]], axis=1)

    # Passing frequencies from decimal to percentage
    nocols = (("Position1","Position2","itype","Position"))
    for colname in df:
        if colname not in nocols:
            df[colname] = df[[colname]].apply(lambda x: x*100)

    return(df)

def frequencies(df):
    """
    Creates an interaction frequency numpy matrix from 
    """

    # Transpose matrix
    df_t = df.transpose() 
    
    # Create dictionary table with position tuple as keys and interaction-by-simulation-freq array as value
    freq_table = { tuple(col.split(" ")):list(df_t[col].values) for col in df_t }
        
    # Convert previous dictionary to numpy array, and traspose it
    freq_matrix = (array([freq_table[(r1, r2)] for (r1, r2) in freq_table])).T

    # Reorder according to clustering
    return freq_matrix

def clustering(clusters, dend_matrix, labels, linkagefun):
    """
    Find the color threshold needed for the dendrogram to have "clusters" number of clusters. 
    Also define to which cluster each simulation belongs
    """
    Z = linkagefun(dend_matrix)
    color_threshold = Z[-1*clusters][2]+0.0000000001 #Cut slightly above the tree node
    
    # Defining to which cluster belongs to each simulation
    T = fcluster(Z, t=clusters, criterion='maxclust')
    clustdict = { sim : "cluster" + str(clust) for sim,clust in zip(labels,T) }

    return(color_threshold, clustdict)

def black_or_white(bgcolor):
    """
    Text with this color background should be in black or white font?
    """
    ary_bgcolors = re.findall(r"[\w']+", bgcolor)
    R = int(ary_bgcolors[1])
    G = int(ary_bgcolors[2])
    B = int(ary_bgcolors[3])
    Lumi = (sum([R,G,B])/3)

    if Lumi > 125:
        colorfont = 'rgb(0,0,0)'
    else:
        colorfont = 'rgb(255,255,255)'

    return colorfont

def hoverlabels_axis(fig, recept_info, recept_info_order, annotations = []):
    """
    Makes hover labels from figure correspond to Y-axis labels, and make Y-axis labels correspond to dendrogram
    colors.
    """
    
    def define_hoverentry(marker, text, x, y,):
        """
        Define a new trace (U-shape things that consitute dendrograms)
        """
        return dict(
            type = 'scatter',
            hoverinfo = 'text',
            marker = marker,
            text = text,
            mode = 'markers',
            x = x,
            xaxis = 'x',
            y = y,
            yaxis = 'y'
        )
    
    def define_annotation_list(y_pos, bgcolor, text, colorfont):
        """
        Create a list of annotation objects. This annotations are meant to replace the axis labels as names of simulations
        """
        return dict(
            x = -0,
            y = y_pos,
            xanchor = 'left',
            text = text,
            showarrow = False,
            bgcolor = bgcolor,
            font = { 'size' : 12, 'color' : colorfont },
            height = 14
        )

    def prepare_entry(hoverentry, fig, ypos, name_index, ligname_index, recept_info, pdb_index):
        """
        Creates xaxis-annotations and hoverlabels based on the information contained by this dendrogram branch
        """                
        dynid = dendro_leaves[int((ypos-5)/10)]
        nodyn_id = dynid.replace('dyn','')
        pdbcode = recept_info[dynid][pdb_index]
        simname = recept_info[dynid][name_index]
        ligname = recept_info[dynid][ligname_index]
        bgcolor = hoverentry['marker']['color']
        anot_text = "%s (%s)" % (simname, pdbcode)
        hovertext = str("complex with %s (dynID: %s)" % (ligname, nodyn_id)) if (ligname) else  str("apoform (dynID: %s)" % (nodyn_id))

        # Create new mini-entry reaching only branch of interest
        newhoverentry = define_hoverentry(hoverentry['marker'], hovertext, [-0]*4, [ypos] * 4)
        fig.add_trace(newhoverentry)

        # Annotation to corresponding simulation
        colorfont = black_or_white(bgcolor)
        annotations.append(define_annotation_list(ypos, bgcolor, anot_text, colorfont))

        return(fig, annotations)
    
    dendro_leaves = fig['layout']['yaxis']['ticktext']

    # Adapting hovertool to what I want from it
    name_index = recept_info_order['prot_lname']
    pdb_index = recept_info_order['pdb_id']
    ligname_index = recept_info_order['resname']
    for hoverentry in fig['data']:

        # Silenciate all default hover entries. 
        hoverentry['hoverinfo'] = 'none'
        
        # If entry reaches end of plot (not intermediate node)
        if (hoverentry['x'][0] == -0) and (int(hoverentry['y'][0])%10 == 5):
            (fig, annotations) = prepare_entry(hoverentry, fig, hoverentry['y'][0], name_index, ligname_index, recept_info, pdb_index)
                
            #If this entry reaches two labels at the same time (terminal U node), create yet another entry
            if (hoverentry['x'][3] == -0) and (int(hoverentry['y'][3])%10 == 5): 
                (fig, annotations) = prepare_entry(hoverentry, fig, hoverentry['y'][3], name_index, ligname_index, recept_info, pdb_index)

    fig['layout']['annotations'] = annotations
                
    return fig

def annotate_clusters(fig, default_color = ""):
    """
    Put an annotation the nodes on top of clusters
    """
    prevcolor = ""
    min_x = 0
    clustcount = -1
    clustcoords = []
    xcords = []
    annotations = []
    for entry in fig['data']:

        currentcolor = entry['marker']['color']
        # If new entry is higher (inside the tree) than previous, select as candidate for cluster node
        current_min_x = min(entry['x'])
        current_max_x = max(entry['x'])
        if (currentcolor == default_color) and (max(entry['x']) != -0.0):
            continue

        # If there has been a color change, then a new cluster the iteration has entered
        if prevcolor != currentcolor:
            clustcount += 1
            xcords.append("")
            min_x = 0
            clustcoords.append({})
        
        if current_min_x <= min_x:
            min_x = current_min_x
            clustcoords[clustcount]['clusnode_x'] = entry['x'][1]
            xcords[clustcount] = (clustcoords[clustcount]['clusnode_x'])
            clustcoords[clustcount]['clusnode_y'] = (entry['y'][1] + entry['y'][2])/2
            clustcoords[clustcount]['clustnumber'] = clustcount
            clustcoords[clustcount]['color'] = currentcolor
            clustcoords[clustcount]['xanchor'] = 'right'
            
            if (currentcolor == default_color) and (current_max_x == -0): #For single-branch clusters
                index_x = np.where(entry['x'] == current_max_x) 
                clustcoords[clustcount]['clusnode_y'] = entry['y'][index_x][0]
                clustcoords[clustcount]['xanchor'] = 'center' # In those cases is prettier this way
                
        prevcolor = currentcolor

    for clust in clustcoords:
        colorfont = black_or_white(clust['color'])
        annotations.append(dict(
            x = clust['clusnode_x'],
            y = clust['clusnode_y'],
            xanchor = clust['xanchor'],
            text = "cluster " + str(clust['clustnumber']+1),
            showarrow = False,
            bgcolor = clust['color'],
            font = { 'size' : 12, 'color' : colorfont },
            height = 14
        ))

    return annotations

def dendrogram_clustering(dend_matrix, labels, height, width, filename, clusters, recept_info, recept_info_order): 

    # Define linkage function (we'll be using the default one for plotly). 
    linkagefun=lambda x: linkage(x, 'complete')
    (thres,clustdict) = clustering(clusters, dend_matrix, labels, linkagefun)

    # Create color scale from the "category20" color scale. Not working because color_scale plotly option is inoperative
    colors_category20 = ['rgb(31, 119, 180)', 'rgb(174, 199, 232)', 'rgb(255, 127, 14)', 'rgb(255, 187, 120)', 'rgb(44, 160, 44)', 'rgb(152, 223, 138)', 'rgb(214, 39, 40)', 'rgb(255, 152, 150)', 'rgb(148, 103, 189)', 'rgb(197, 176, 213)', 'rgb(140, 86, 75)', 'rgb(196, 156, 148)', 'rgb(227, 119, 194)', 'rgb(247, 182, 210)', 'rgb(127, 127, 127)', 'rgb(199, 199, 199)', 'rgb(188, 189, 34)', 'rgb(219, 219, 141)', 'rgb(23, 190, 207)', 'rgb(158, 218, 229)']
    colors = colors_category20[0:clusters]

    # Setting figures
    fig = create_dendrogram(
        dend_matrix,
        orientation='right',
        labels=labels,
        linkagefun=linkagefun,
        color_threshold = thres,
        hovertext = labels,
    )

    fig['layout'].update({
        'width':width, 
        'height':height,
        'autosize' : False,
        'hoverdistance' : 10,
        })

    fig['layout']['margin'].update({
        'r' : 300,
        'l' : 20,
        't' : 0,
        'b' : 0,
        'pad' : 0
        })

    fig['layout']['xaxis'].update({
        'showline': False,
        'showticklabels': False,
        'ticks' : '',
        'fixedrange' : True,
        })

    fig['layout']['yaxis'].update({
        'side' : 'right',
        'showline': False,
        'ticks' : '',
        'tickfont' : {
            'size' : 15,
            'color' : 'white'
            },
        'fixedrange' : True,
        })
   
    #Annotating cluster nodes
    annotations = annotate_clusters(fig, 'rgb(0,116,217)') # Default color for tree
    
    # Correcting hoverlabels
    fig = hoverlabels_axis(fig, recept_info, recept_info_order, annotations)
    
    # Taking order for plot rows
    dendro_leaves = fig['layout']['yaxis']['ticktext']

    # Writing dendrogram on file
    plot(fig, filename=filename, auto_open=False, config={
        "displayModeBar": "hover",
        "showAxisDragHandles": False,
        "showAxisRangeEntryBoxes": False,
        "scrollZoom": False,
        "showTips" : False,
        "modeBarButtons": [["toImage"]]
    })
    return (list(dendro_leaves),clustdict)

def sort_simulations(df_ts, dyn_dend_order):
    """
    Sorts the simulations in the dataframe according to the order in the list dyn_dend_order
    """

    # Create a dictionary with the order of each simulation row in the plot 
    dyn_dend_order_dict = { dyn_name : dyn_dend_order.index(dyn_name) for dyn_name in dyn_dend_order }

    # Adding column based in new order recieved from clustering
    df_ts['clust_order'] =  df_ts['Id'].apply(lambda x: dyn_dend_order_dict[x])

    #Sorting by ballesteros Id's (helixloop column) and clustering order
    df_ts['helixloop'] = df_ts['Position'].apply(lambda x: re.sub(r'^(\d)x',r'\g<1>0x',x)) 
    df_ts = df_ts.sort_values(["helixloop",'clust_order'])

    #Drop sort columns once used
    df_ts.drop(['helixloop','clust_order'], axis = 1, inplace = True)

    return df_ts

def reverse_positions(df):
    """
    Appends a copy of the dataframe with the Position pair of the interaction being reversed (5x43-7x89 for 7x89-5x43)
    """
    df_rev = df.copy(deep = True)
    df_rev['Position'] = df_rev['Position'].replace({r'(\w+)\s+(\w+)' : r'\2 \1'}, regex=True)
    df_double = pd.concat([df, df_rev])
    return df_double    

def create_hovertool(itype, itypes_order, hb_itypes, typelist):
    """
    Creates a list in hovertool format from the two dictionaries above
    """

    #Creating hovertool list
    hoverlist = [('Name', '@Name'), ('PDB id', '@pdb_id'), ('Position', '@Position')]
    if itype == "all":
        for group,type_tuple in itypes_order:
            for itype_code,itype_name in type_tuple:
                hoverlist.append((itype_name, "@{" + itype_code + '}{0.00}%'))
                if itype_code == "hb":
                    for hb_code,hb_name in hb_itypes.items():
                        hoverlist.append((hb_name, "@{" + hb_code + '}{0.00}%'))
    else:
        hoverlist.append((typelist[itype], "@{" + itype + '}{0.00}%'))
    hoverlist.append(('Total interaction frequency', '@{all}{0.00}%'))

    #Hover tool:
    hover = HoverTool(
        tooltips=hoverlist
    )

    return hover


def define_figure(width, height, tool_list, dataframe, hover, itype):
    """
    Prepare bokeh figure heatmap as intended
    """

    # Mapper
    colors = ['#FF0000','#FF0800','#FF1000','#FF1800','#FF2000','#FF2800','#FF3000','#FF3800','#FF4000','#FF4800','#FF5000','#FF5900','#FF6100','#FF6900','#FF7100','#FF7900','#FF8100','#FF8900','#FF9100','#FF9900','#FFA100','#FFAA00','#FFB200','#FFBA00','#FFC200','#FFCA00','#FFD200','#FFDA00','#FFE200','#FFEA00','#FFF200','#FFFA00','#FAFF00','#F2FF00','#EAFF00','#E2FF00','#DAFF00','#D2FF00','#CAFF00','#C2FF00','#BAFF00','#B2FF00','#AAFF00','#A1FF00','#99FF00','#91FF00','#89FF00','#81FF00','#79FF00','#71FF00','#69FF00','#61FF00','#59FF00','#50FF00','#48FF00','#40FF00','#38FF00','#30FF00','#28FF00','#20FF00','#18FF00','#10FF00','#08FF00','#00FF00']
    colors.reverse()
    mapper = LinearColorMapper(palette=colors, low=0, high=100)

    p = figure(
        plot_width= width, 
        plot_height=height,
        #title="Example freq",
        y_range=list(dataframe.Id.drop_duplicates()),
        x_range=list(dataframe.Position.drop_duplicates()),
        tools=tool_list, 
        x_axis_location="above",
        active_drag=None,
        toolbar_location="right",
        toolbar_sticky = False,
        min_border_top = round(height * 0.047), # The proportion of margin to be left on top of matrix to align with dendrogram
        min_border_bottom = 0
    )

    # Rotate angle of x-axis labels
    p.xaxis.major_label_orientation = pi/3

    # Create rectangle for heatmap
    mysource = ColumnDataSource(dataframe)
    p.rect(
        y="Id", 
        x="Position", 
        width=1, 
        height=1, 
        source=mysource,
        line_color="white", 
        fill_color=transform(itype, mapper),

        # set visual properties for selected glyphs
        selection_line_color="black",
        selection_fill_color=transform(itype, mapper),
        # set visual properties for non-selected glyphs
        nonselection_fill_color=transform(itype, mapper),
        nonselection_fill_alpha=1,
        nonselection_line_alpha=1,
        nonselection_line_color="white"
        )

    # Add legend
    color_bar = ColorBar(
        color_mapper=mapper,
        location=(0, 0),
        label_standoff = 12,
        ticker=BasicTicker(desired_num_ticks=2),
        formatter=PrintfTickFormatter(format="%d%%"),
        major_label_text_font_size="11pt"
        )
    p.add_layout(color_bar, 'left')

    # Setting axis
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.xaxis.major_label_text_font_size = "10pt"
    p.yaxis.major_label_text_font_size = "10pt"
    p.yaxis.visible = False
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = 1#"vertical"

    # Adding hover
    p.add_tools(hover)

    # Needed later
    return(mysource,p)

def select_tool_callback(recept_info, recept_info_order, dyn_gpcr_pdb, itype, typelist, mysource):
    """
    Prepares the javascript script necessary for the side-window
    """
    
    #Create data source
    df_ri=pd.DataFrame(recept_info)
    ri_source=ColumnDataSource(df_ri)
    df_rio=pd.DataFrame(recept_info_order, index=[0])
    rio_source=ColumnDataSource(df_rio)
    df_gnum=pd.DataFrame(dyn_gpcr_pdb)
    gnum_source=ColumnDataSource(df_gnum)

    #Select tool and callback: (SIMPLIFIED)
    mysource.callback = CustomJS(
        args={"r_info":ri_source,"ro_info":rio_source,"gnum_info":gnum_source,"itype":itype, "typelist" : typelist},
        code="""
            var sel_ind = cb_obj.selected["1d"].indices;
            var plot_bclass=$("#retracting_parts").attr("class");
            if (sel_ind.length != 0){
                var data = cb_obj.data;
                var ri_data=r_info.data;
                var rio_data=ro_info.data;
                var gnum_data=gnum_info.data;
                var recept_name=data["Name"][sel_ind];
                var recept_id=data["Id"][sel_ind];
                var pos=data["Position"][sel_ind];
                var freq_total=data["all"][sel_ind];
                var freq_type=data[itype][sel_ind];
                var pos_array = pos.split(" ");
                var pos_string = pos_array.join("_")
                var pos_ind_array = pos_array.map(value => { return gnum_data['index'].indexOf(value); });
                var pdb_pos_array = pos_ind_array.map(value => { return gnum_data[recept_name][value]; });
                var lig=ri_data[recept_id][rio_data['resname']];
                var lig_lname=ri_data[recept_id][rio_data['lig_lname']];
                var recept=ri_data[recept_id][rio_data['upname']];
                var dyn_id_pre=ri_data[recept_id][rio_data['dyn_id']];
                var dyn_id=dyn_id_pre.match(/\d*$/)[0];
                var prot_id=ri_data[recept_id][rio_data['prot_id']];
                var prot_lname=ri_data[recept_id][rio_data['prot_lname']];
                var comp_id=ri_data[recept_id][rio_data['comp_id']];
                var struc_fname=ri_data[recept_id][rio_data['struc_fname']];
                var struc_file=ri_data[recept_id][rio_data['struc_f']];
                var traj_fnames=ri_data[recept_id][rio_data['traj_fnames']];
                var traj_f=ri_data[recept_id][rio_data['traj_f']];
                var pdb_id=ri_data[recept_id][rio_data['pdb_id']];
                var pdb_id_nochain = pdb_id.split(".")[0];
                var delta=ri_data[recept_id][rio_data['delta']];
                $('#ngl_iframe')[0].contentWindow.$('body').trigger('createNewRef', [struc_file, traj_fnames, traj_f ,lig, delta, pos, pdb_pos_array]);
                
                if (plot_bclass != "col-xs-9"){
                    $("#retracting_parts").attr("class","col-xs-9");
                    $("#second_col").attr("class","col-xs-5");
                    $("#info").css({"visibility":"visible","position":"relative","z-index":"auto"});
                }

                //Setting type specific frequencies
                if (itype == "all") {
                    for (my_type in typelist) {
                        if (my_type == "all"){ // Total frequency shall not be displayed twice
                            continue;
                        }
                        var freq_type = data[my_type][sel_ind];
                        $( "#freq_" + my_type).html(freq_type.toFixed(2) + "%");
                    }
                }
                else {
                    $( "#freq_" + itype).html(freq_type.toFixed(2) + "%");
                }

                $("#freqtotal_val").html(freq_total.toFixed(2) + "%");
                $("#recept_val").html(prot_lname + " ("+recept+")");
                $("#pos_val").html(pos);
                $("#pdb_id").html(pdb_id);
                $("#pdb_link").attr("href","https://www.rcsb.org/structure/" + pdb_id_nochain)
                if (Boolean(lig)) {
                    $("#lig_val").html(lig_lname + " ("+lig+")");
                    $("#lig_link").show();
                    $("#lig_link").attr("href","../../../dynadb/compound/id/"+comp_id);
                }
                else {
                    $("#lig_val").html("None");
                    $("#lig_link").hide();
                }
                $("#viewer_link").attr("href","../../../view/"+dyn_id+"/"+pos_string);
                $("#recept_link").attr("href","../../../dynadb/protein/id/"+prot_id);
            } else {
                if (plot_bclass != "col-xs-12"){
                    $("#retracting_parts").attr("class","col-xs-12");
                    $("#info").css({"visibility":"hidden","position":"absolute","z-index":"-1"});
                } 
            }           
        """)

    return mysource

############
## Variables
############

#itype sets
itypes = set(("wb", "wb2", "sb","hp","pc","ps","ts","vdw", "hb", "hbbb","hbsb","hbss","hbls","hblb","all"))
nolg_itypes = set(("sb","pc","ts","ps","hbbb","hbsb","hbss","hp"))
noprt_itypes = set(("hbls","hblb"))
ipartners = set(("lg","prt","prt_lg"))

# Basepath for files
basepath = "/protwis/sites/files/Precomputed/get_contacts_files/"

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
    "hb" : 'hydrogen bonds',
    'all' : 'all types',
}
hb_itypes = {
    "hbbb" : 'backbone to backbone',
    "hbsb" : 'sidechain to backbone',
    "hbss" : 'sidechain to sidechain',
    "hbls" : 'ligand to sidechain',
    "hblb" : 'ligand to backbone',
}
other_itypes = {
    'hp' : 'hydrophobic',
    'sb' : 'salt bridge',
    "pc" : 'pi-cation',
    "ps" : 'pi-stacking',
    'ts' : 't-stacking',
    "vdw" : 'van der waals',
    "wb" : 'water bridge',
    "wb2" : 'extended water bridge',

}

itypes_order = [
    ("Non-polar", 
        (
            ("vdw","van der waals"),
            ('hp', "hydrophobic")
        )
    ),
    ("Polar/Electrostatic", 
        (
            ("hb", "hydrogen bond"),
            ("wb", "water bridge"),
            ("wb2", "extended water bridge"),
            ('sb', "salt bridge"),
            ("pc", "pi-cation")
        )
    ),
    ("Stacking",
        (
            ("ps", "pi-stacking"),
            ('ts', "t-stacking")
        )
    )
]

###############
# Main function 
###############

def get_contacts_plots(itype, ligandonly):

    """
    Create and save dataframe, dendrogram, and other data necessary for computing get_contacts online plots
        - itype: any of the codes from below typelist.
        - ligandonly: lg (only residue-ligand contacts), prt (only intraprotein contacts), all 
    """    

    print(str("computing dataframe and dendrogram for %s-%s") % (itype, ligandonly))

    # Creating set_itypes, with all in case it is not still in it
    if itype == "all":
        set_itypes =  set(("sb", "pc", "ps", "ts", "vdw", "hp", "hb", "hbbb", "hbsb", "hbss", "wb", "wb2", "hbls", "hblb", "all"))
    else: 
        set_itypes = set(itype.split("_"))
        set_itypes.add('all')

    #Creating itypes dictionary for selected types
    selected_itypes = { x:typelist[x] for x in set_itypes }

    #Loading files
    df_raw = pd.read_csv(str(basepath + "contact_tables/compare_all.tsv"), sep="\s+")
    for itype_df in set_itypes:
        if itype_df == "all": 
            continue
        df_raw_itype = pd.read_csv(str(basepath + "contact_tables/compare_" + itype_df + ".tsv"), sep="\s+")
        df_raw = pd.concat([df_raw, df_raw_itype])
    compl_data = json_dict(str(basepath + "compl_info.json"))

    

    # Adapting to Mariona's format
    df = adapt_to_marionas(df_raw)

    # Filtering out non-ligand interactions if option ligandonly is True
    if ligandonly == "lg":
        ligandfilter = df['Position'].str.contains('Ligand')
        df = df[ligandfilter]
    elif ligandonly == "prt":
        ligandfilter = ~df['Position'].str.contains('Ligand')
        df = df[ligandfilter]


    #Removing helix-to-helix, low-frequency pairs and merging same residue-pair interaction frequencies
    df = removing_entries(df, set_itypes, itype)

    # Stack matrix (one row for each interaction pair and dynamic. Colnames are position, dynid and itypes)
    df_ts = stack_matrix(df, set_itypes)

    #Dropping away non main-type interaction rows.
    df = df[df['itype'] == itype]

    #Dropping away interaction type colum
    df.drop('itype', 1, inplace = True)

    # If there are no interactions with this ligandonly-itype combination
    if df.empty:
        print("No interactions avalible for this molecular partners and interaction type: %s and %s" % (ligandonly, itype) )
        return

    # Set position as row index of the dataframe
    df = df.set_index('Position')        

    #Computing frequency matrix
    dend_matrix = frequencies(df)
    
    #Changing ID names by simulation names
    (recept_info,recept_info_order,df_t,dyn_gpcr_pdb,index_dict)=improve_receptor_names(df_ts,compl_data)

    # Apending column with PDB ids
    pdb_id = recept_info_order['pdb_id']
    df_ts['pdb_id'] = df_ts['Id'].apply(lambda x: recept_info[x][pdb_id])

    # Labels for dendogram
    dendlabels_dyns = [ dyn for dyn in df ]

    #Creating dendrogram for each cluster number
    dendfolder = basepath + "view_input_dataframe/" + itype + "_" + ligandonly + "_dendrograms" 
    if not os.path.exists(dendfolder):
        os.makedirs(dendfolder)
    dend_height = int( int(df.shape[1]) * 16 + 20)
    dend_width = 500
    for cluster in range(2,21):
        print("\tcomputing dendrogram: " + str(cluster) + " clusters" )
        dendfile = ("%s/%s_%s_%s_dendrogram_figure.html" % (dendfolder, itype, str(cluster), ligandonly))
        (dyn_dend_order, clustdict) = dendrogram_clustering(dend_matrix, dendlabels_dyns, dend_height, dend_width, dendfile, cluster, recept_info, recept_info_order)

    for rev in ["rev", "norev"]:

        # If rev option is setted to rev, duplicate all lines with the reversed-position version (4x32-2x54 duplicates to 2x54-4x32)
        if rev == "rev":
            df_ts_rev = reverse_positions(df_ts)
        else:
            df_ts_rev = df_ts

        df_ts_rev = sort_simulations(df_ts_rev, dyn_dend_order)
        
        
        # Defining height and width of the future figure from columns (simulations) and rows (positions) of the df dataframe
        # I use df instead of df_ts because of its structure. I know it's kind of strange
        h=dend_height
        if rev == "rev":
            w=16300 if int(df.shape[0]*20 + 130) > 16300 else int(df.shape[0]*20*2 + 130)
        else: 
            w=16300 if int(df.shape[0]*20 + 130) > 16300 else int(df.shape[0]*20 + 130)    

        # Save dataframe in csv (without row indexes)
        csvfile =  basepath + "view_input_dataframe" + "/" + itype + "_" + ligandonly + "_" + rev + "_dataframe.csv"
        df_ts_rev.to_csv(path_or_buf = csvfile, index = False)

        # Define a figure
        hover = create_hovertool(itype, itypes_order, hb_itypes, typelist)
        mytools = ["hover","tap","save","reset","wheel_zoom"]
        mysource,p = define_figure(w, h, mytools, df_ts_rev, hover, itype)

        # Creating javascript for side-window
        mysource = select_tool_callback(recept_info, recept_info_order, dyn_gpcr_pdb, itype, typelist, mysource)

        # Find path to files 
        plotdiv_w= w + 275
        script, div = components(p)
        
        # Creating directory if it doesn't exist
        if not os.path.exists(basepath + "view_input_dataframe"):
            os.makedirs(basepath + "view_input_dataframe")

        # Write heatmap on file
        with open(basepath + "view_input_dataframe" + "/" + itype + "_" + ligandonly + "_" + rev + "_heatmap.html", 'w') as heatmap:
            heatmap.write(script)

        # Write div and plotdiv as python variables in a python file
        with open(basepath + "view_input_dataframe" + "/" + itype + "_" + ligandonly + "_" + rev + "_variables.py", 'w') as varfile:
            varfile.write("div = \'%s\'\n" % div.lstrip())
            varfile.write("plotdiv_w = " + str(plotdiv_w))

###################
## Calling function
###################

if len(argv) == 1:
    print(exit("""

##############table_to_dataframe.py#####################

This script creates dataframes, dendrogram and other
auxiliary files which serve as main inputs for contact_maps
application.

table_to_dataframe.py <INTERACTION_TYPE> <INTERACTION_PARTNERS>
table_to_dataframe.py --all

    - INTERACTION TYPE: any of the interaction types avalible for the web 
    - INTERACTION PARTNERS: lg, prt or prt_lg 

    --all: all combinations of itype and interaction partners are computed
"""))

if argv[1] == "--all":
    for itype in itypes:
        for ipartner in ipartners:
            if (itype in nolg_itypes) and (ipartner == "lg"):
                continue
            if (itype in noprt_itypes) and (ipartner == "prt"):
                continue
            get_contacts_plots(itype, ipartner)
else:
    get_contacts_plots(argv[1], argv[2])
