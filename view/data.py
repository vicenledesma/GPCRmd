

change_lig_name={7:{"resname":"CHL1 and 59",
                    "longname":"Cholesterol 59",
                    "orig_resname":"CHL1",
                    "add_twice":"Lipid"},
                10:{"resname":"CAU",
                    "longname":"Carazolol",
                    "orig_resname":"CAU",
                    "add_twice":False}
                }

cons_classA=[["N1.50", "Allosteric sodium binding site (98%)",""], ["D2.50", "90%",""], ["R3.50", "95%",""],["W4.50", "97%",""],["P5.50", "78%",""], ["P6.50", "99%",""], ["P7.50", "88%",""]]
mol_swA=[["D3.32","",""],["I3.40","",""],["D3.49","",""],["E6.30","",""],["F6.44","",""],["W6.48","",""],["Y7.53","",""]]
cons_classB=[["S1.50", "",""], ["H2.50", "",""], ["E3.50", "",""],["W4.50", "",""],["N5.50", "",""], ["G6.50", "",""], ["G7.50", "",""]]
cons_classC=[["G1.50", "",""], ["Y2.50", "",""], ["K3.50", "",""],["L4.50", "",""],["L5.50", "",""], ["W6.50", "",""], ["P7.50", "",""]]
cons_classF=[["T1.50", "",""], ["F2.50", "",""], ["W3.50", "",""],["W4.50", "",""],["P5.50", "",""], ["H6.50", "",""], ["I7.50", "",""]]

cons_pos_dict={"A":[cons_classA,mol_swA],"B":[cons_classB],"C":[cons_classC],"F":[cons_classF]}

motifs=[["PIF","P5.50",False,"",""],["PIF","I3.40",False,"",""],["PIF","F6.44",False,"",""],["DRY","D3.49",False,"",""],["DRY","R3.50",False,"",""],["DRY","Y3.51",False,"",""],["NPxxY","N7.49",False,"",""],["NPxxY","P7.50",False,"",""],["NPxxY","x7.51",False,"",""],["NPxxY","x7.52",False,"",""],["NPxxY","Y7.53",False,"",""]]
motname_li=["PIF","DRY","NPxxY",]

motifs_dict={"A":[motifs,motname_li],"B":[],"C":[],"F":[]}

motifs_all_info={"A":[["PIF","P5.50 , I3.40 , F6.44",""],["DRY","D3.49 , R3.50 , Y3.51",""],["NPxxY","N7.49 , P7.50 , x7.51 , x7.52 , Y7.53",""]],"B":[],"C":[],"F":[]}

active_class={"A":["",""],"B":["",""],"C":["",""],"F":["",""]}

