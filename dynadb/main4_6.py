from Bio import pairwise2
from Bio.pairwise2 import format_alignment
import re

#The pipeline: get sequence from pdb (checkpdb function) -> compare sequence from pdb to the fasta sequence (matchpdbfa) -> modify pdb to make it match the fasta numbering (repairpdb). 

#The way to detect which format is used is to check if the residue after resid 9999 is 2710. if after 9999 there is a 2710 then all coming numbers are hexadecimal. If after 9999 comes 10000 they are using the insertion code. 

d={'CYSF': 'C', 'OLS': 'S', 'HE6': 'H', 'HEX': 'H', 'CCY0': 'C', 'TRP': 'W', 'TYR': 'Y', 'HEJ': 'H', 'CCY1': 'C', 'CM2L': 'K', 'HDY': 'H', 'HEB': 'H', 'CYSL': 'C', 'NCY4': 'C', 'ASN1': 'N', 'DAB': 'X', 'CCY6': 'C', 'HE4': 'H', 'CYX': 'C', 'CH2E': 'H', 'ARGN': 'R', 'CSEP': 'S', 'HES': 'H', 'ASPH': 'D', 'LYSH': 'K', 'HEG': 'H', 'CCYM': 'C', 'NASH': 'D', 'HDQ': 'H', 'GLYM': 'G', 'OLP': 'P', 'HD9': 'H', 'HS2': 'H', 'HSE': 'H', 'NCY8': 'C', 'HEL': 'H', 'HID': 'H', 'CY0': 'C', 'PTR': 'T', 'HEI': 'H', 'HEY': 'H', 'HD3': 'H', 'M2L': 'K', 'Y1P': 'Y', 'NPTR': 'T', 'HSC': 'H', 'HDT': 'H', 'NY1P': 'Y', 'MELE': 'L', 'NCY6': 'C', 'NCCS': 'C', 'CY7': 'C', 'LYS': 'K', 'ILE': 'I', 'HEC': 'H', 'CHYP': 'P', 'HEH': 'H', 'CT2P': 'T', 'KCX': 'K', 'NCY1': 'C', 'CH2D': 'H', 'NM3L': 'K', 'CACK': 'K', 'CM3L': 'K', 'ACK': 'K', 'HISA': 'H', 'HEU': 'H', 'CCY4': 'C', 'ALY': 'K', 'CASH': 'D', 'HDK': 'H', 'CCME': 'C', 'NH1E': 'H', 'HDH': 'H', 'HIS2': 'H', 'ASP': 'D', 'NCY3': 'C', 'LSN': 'K', 'HD7': 'H', 'CNLN': 'N', 'HISE': 'H', 'CS1P': 'S', 'CY8': 'C', 'NOLP': 'P', 'HSD': 'H', 'SEP': 'S', 'COLT': 'T', 'HD8': 'H', 'CSRM': 'R', 'NM2L': 'K', 'CS2P': 'S', 'HDD': 'H', 'COLS': 'S', 'HEZ': 'H', 'NCYX': 'C', 'GLUP': 'E', 'HDE': 'H', 'NTPO': 'T', 'HDS': 'H', 'NS2P': 'S', 'CCS': 'C', 'NLE': 'L', 'CY2P': 'Y', 'CY3': 'C', 'HIN': 'H', 'ASP1': 'A', 'H2E': 'H', 'HISH': 'H', 'NCY9': 'C', 'MGY': 'G', 'CH1D': 'H', 'NSRM': 'R', 'CCY9': 'C', 'NDAB': 'X', 'NNLN': 'N', 'CY6': 'C', 'CYSG': 'C', 'CHIP': 'H', 'SER': 'S', 'CDRM': 'R', 'OLT': 'T', 'LYN': 'K', 'GLY': 'G', 'NH2D': 'H', 'PHEU': 'F', 'ASN': 'N', 'HET': 'H', 'HDO': 'H', 'HD4': 'H', 'HEE': 'H', 'HE7': 'H', 'DHSE': 'H', 'HE3': 'H', 'CDAB': 'X', 'MLYS': 'K', 'NLN': 'N', 'HEP': 'H', 'MLEU': 'L', 'Y2P': 'Y', 'CGUP': 'E', 'NT2P': 'T', 'CY9': 'C', 'T1P': 'T', 'HIS1': 'H', 'HDV': 'H', 'HDB': 'H', 'HIS': 'H', 'HEM': 'H', 'HDX': 'H', 'M3L': 'K', 'HDW': 'H', 'HDZ': 'H', 'GLUH': 'E', 'GLH': 'E', 'MEVA': 'V', 'SERD': 'S', 'CHID': 'H', 'DRM': 'R', 'HEO': 'H', 'CKCX': 'K', 'NCY0': 'C', 'HEF': 'H', 'CCY5': 'C', 'NCY7': 'C', 'NHYP': 'P', 'NY2P': 'Y', 'HE0': 'H', 'CMLY': 'K', 'MVAL': 'V', 'H2D': 'H', 'SRM': 'R', 'HDC': 'H', 'NT1P': 'T', 'NHID': 'H', 'CARM': 'R', 'HE5': 'H', 'TPO': 'T', 'HDU': 'H', 'LEU': 'L', 'GLU': 'E', 'CTPO': 'T', 'HEK': 'H', 'HE2': 'H', 'MEL': 'L', 'S2P': 'S', 'HDN': 'H', 'CGU': 'E', 'HD5': 'H', 'HD6': 'H', 'AP1': 'D', 'S1P': 'S', 'DHSP': 'H', 'NACK': 'K', 'GLN': 'Q', 'NARM': 'R', 'NCY2': 'C', 'CYS': 'C', 'ARG': 'R', 'HYP': 'P', 'CY1': 'C', 'NHIN': 'H', 'CYSH': 'C', 'HD0': 'H', 'NLYN': 'K', 'NHIP': 'H', 'CY5': 'C', 'CH1E': 'H', 'HDL': 'H', 'HEA': 'H', 'NDRM': 'R', 'NCME': 'C', 'NCYM': 'C', 'CY2': 'C', 'CHIN': 'H', 'HDR': 'H', 'COLP': 'P', 'CCYX': 'C', 'CGLH': 'E', 'MEV': 'V', 'CYS2': 'C', 'HER': 'H', 'HEW': 'H', 'HEQ': 'H', 'HED': 'H', 'ZAFF': 'D', 'HISP': 'H', 'HISD': 'H', 'NGLH': 'E', 'HEV': 'H', 'HDJ': 'H', 'CY1P': 'Y', 'HDM': 'H', 'CY4': 'C', 'THR': 'T', 'NMLY': 'K', 'HDI': 'H', 'MLY': 'K', 'HEN': 'H', 'NSEP': 'S', 'H1D': 'H', 'MET': 'M', 'HIE': 'H', 'NKCX': 'K', 'HD1': 'H', 'NOLT': 'T', 'T2P': 'T', 'ALA': 'A', 'HD2': 'H', 'DHSD': 'H', 'HDP': 'H', 'CYM': 'C', 'HDF': 'H', 'HDA': 'H', 'NS1P': 'S', 'CHIE': 'H', 'CLYN': 'K', 'HISB': 'H', 'ARM': 'R', 'CT1P': 'T', 'CPTR': 'T', 'HSP': 'H', 'CME': 'C', 'HE1': 'H', 'CYSD': 'C', 'PHE': 'F', 'NH2E': 'H', 'CCY3': 'C', 'NH1D': 'H', 'NCY5': 'C', 'PRO': 'P', 'HIP': 'H', 'NHIE': 'H', 'ASPP': 'D', 'CCCS': 'C', 'HE8': 'H', 'VAL': 'V', 'HE9': 'H', 'CYSP': 'C', 'NOLS': 'S', 'CCY2': 'C', 'CCY7': 'C', 'ASH': 'D', 'TRPU': 'W', 'CCY8': 'C', 'HDG': 'H', 'H1E': 'H','CYS':'C', 'ASP':'D', 'SER':'S', 'GLN':'Q', 'LYS':'K', 'ILE':'I', 'PRO':'P', 'THR':'T', 'PHE':'F', 'ASN':'N', 'GLY':'G', 'HIS':'H', 'LEU':'L', 'ARG':'R', 'TRP':'W', 'ALA':'A', 'VAL':'V', 'GLU':'E', 'TYR':'Y', 'MET':'M', 'DCYS':'C', 'DASP':'D', 'DSER':'S', 'DGLN':'Q', 'DLYS':'K', 'DILE':'I', 'DPRO':'P', 'DTHR':'T', 'DPHE':'F', 'DASN':'N', 'DGLY':'G', 'DHIS':'H', 'DLEU':'L', 'DARG':'R', 'DTRP':'W', 'DALA':'A', 'DVAL':'V', 'DGLU':'E', 'DTYR':'Y', 'DMET':'M', 'CCYS':'C', 'CASP':'D', 'CSER':'S', 'CGLN':'Q', 'CLYS':'K', 'CILE':'I', 'CPRO':'P', 'CTHR':'T', 'CPHE':'F', 'CASN':'N', 'CGLY':'G', 'CHIS':'H', 'CLEU':'L', 'CARG':'R', 'CTRP':'W', 'CALA':'A', 'CVAL':'V', 'CGLU':'E', 'CTYR':'Y', 'CMET':'M', 'NCYS':'C', 'NASP':'D', 'NSER':'S', 'NGLN':'Q', 'NLYS':'K', 'NILE':'I', 'NPRO':'P', 'NTHR':'T', 'NPHE':'F', 'NASN':'N', 'NGLY':'G', 'NHIS':'H', 'NLEU':'L', 'NARG':'R', 'NTRP':'W', 'NALA':'A', 'NVAL':'V', 'NGLU':'E', 'NTYR':'Y', 'NMET':'M'}

#############################################################################################################################################

def checkpdb(name_of_file,segid,start,stop,chain):
	'''Get sequence from a PDB file in a given interval defined by a combination of Segment Identifier (segid), starting residue number (start), end residue number (stop), chain identifier (chain). All can be left in blank. Returns 1) a list of minilist: each minilist has the resid and the aminoacid code. 2) a string with the sequence.'''
	fpdb=open(name_of_file,'r')
	cpos=0 #current residue position
	ppos=0 #previous residue position
	ppos2='0' #previous position after converting hexadecimals to decimals
	pchain='' #previous chain
	seqplain=list() #list of minilist. each minilist contains the residue number and its aminoacid.
	flag=0
	hexflag=0
	pfields=['','' ,'','AAA','Z','0','0','0','0','']
	for line in fpdb:
		if useline(line):
			fields=[ '','' ,'' ,line[17:21],line[21],line[22:27],line[31:39],line[39:47],line[47:55],line[72:77]] 
			#fields=[ '','' ,'' ,line[16:20],line[21],line[22:27],line[31:39],line[39:47],line[47:55]] 8/9/2016
			#fields[3]:Aminoacid code, fields[4]:chain, fields[5]:resid, fields[6-8]:coordinates
			fields[3]=fields[3].replace(" ", "") #it is a standard aa with 3 letters, eliminate whitespace.
			fields[5]=fields[5].replace(" ", "") #it is a standard RESID with 4 characters, eliminate whitespace.
			i=3
			while i<9:
				if fields[i]=='':
					#raise Exception('Missing required field in line: '+line)
					return 'Missing required field in the PDB file at line: '+line
				i+=1

			if fields[5]!=pfields[5]: #resid has changed->new aa
				
				if fields[4]!=pfields[4]  or fields[9]!=pfields[9] or fields[5]=='1': #resid count has been reseted by new chain, new segid or whatever. 
					ppos='0'
					flag=0
				cpos=fields[5] #current position (resid) in the pdb during the present loop cycle
				if flag==1:
					cpos2=int(str(cpos),16)
					ppos2=int(str(ppos),16)
				elif flag==0:
					cpos2=int(cpos)
					ppos2=int(ppos)
				if cpos=='2710' and ppos=='9999':
					cpos2=int(cpos,16)
					flag=1
					hexflag=1

				if (fields[4]==chain or chain == '') and cpos2 >= start and cpos2 <= stop and (segid in line[72:77] or segid==''):
					if cpos2>=ppos2+1:
						try:
							seqplain.append([d[fields[3]],cpos,cpos2])
						except: #Modified aminoacid
							seqplain.append(('X',cpos,cpos2)) #THIS IS NOT NECESSARY NOW! DELETE IT
							#print ('Modified aminoacid %s found in position %s, X inserted in sequence.' % (fields[3],cpos))

					elif cpos2<ppos2 and cpos!=1: 
						#print(cpos2,ppos2)
						#raise Exception('Residue numbering order is corrupted in position:'+str(cpos2))
						return 'Residue numbering order is corrupted in position:'+str(cpos2)

			pchain=fields[4]
			pfields=fields
			ppos=cpos

	fpdb.close()
	onlyaa='' #ignore the resids, pick the aa and that is it.
	for minilist in seqplain:
		onlyaa=onlyaa+minilist[0]

	return (seqplain,onlyaa,hexflag)

#############################################################################################################################################

def matchpdbfa(faseq,pdbseq,tablepdb,hexflag):
	'''Compare sequence from database with the one given in the pdb.
	 Do an alignment to check if the resids are corrupted in the pdb. Returns a table showing
	 the changes in the pdb numbering according to the fasta.'''
	
	bestalig=pairwise2.align.localms(faseq, pdbseq,100,-1,-10,-10)[0] #select the aligment with the best score.
	#pairwise2.align.localms(seq1,seq2,score for identical matches, score for mismatches, score for opening a gap, score for extending a gap)
	print(bestalig)
	biglist=list()
	counterepair=1
	i=0
	pdbalig=bestalig[1] #PDB sequence after alignment
	fastalig=bestalig[0]
	if '-' in fastalig:
		#raise Exception('PDB file contains insertions with respect to fasta, this is not allowed') 
		return 'PDB file contains insertions with respect to fasta, this is not allowed'
	duos=list()
	mismatchlist=list()
	while i < len(fastalig):
		newpos=i+1
		if i+1>9999 and hexflag==1: #hexflag==1 means that the original PDB uses hexadecimal notation
			newpos=format(i+1,'x')	#hexadecimal once 9999 resid is used.
		
		if pdbalig[i]=='-':
			tablepdb.insert(i,'-')
			minilist=[tablepdb[i],[fastalig[i],newpos]]
			duos.append(minilist)

		elif fastalig[i]!=pdbalig[i] and pdbalig[i]!='-':
			minilist=[tablepdb[i], [fastalig[i],newpos]]
			duos.append(minilist)
			mismatchlist.append(minilist)

		else:
			minilist=[tablepdb[i],[fastalig[i],newpos]]
			duos.append(minilist)
		i=i+1

	if len(mismatchlist)>0:
		#print('Mismatch list:',mismatchlist)
		#raise Exception('One or more missmatches were found, this is not allowed. ')
		return ('One or more missmatches were found, this is not allowed. ',mismatchlist)

	return (duos)

#############################################################################################################################################

def repairpdb(pdbfile, guide,segid,start,stop,chain):	

	'''Takes a pdb file as input, the numbering of this pdb is modified according to the fasta sequence of the PDB whose relation
	 is represented in a schema called guide like: [[A,'27',27],[A,28]] where the first element is the pdb item and the second is the 
	 fasta one. The number between '' can ben in hexadecimal format. The format used to write numbers bigger than 9999 (hexadecimal or 	 	 insertion code)  in the new PDB file is the same that was used in the original PDB'''

	oldpdb=open(pdbfile, 'r')
	pdbfile=pdbfile[pdbfile.rfind('/'):]
	newpdb=open('/tmp'+pdbfile[:-4]+'_corrected.pdb','w')
	count=-1
	pvresid=-1
	pfields=['','' ,'','AAA','Z','0','0','0','0','']
	pchain='Z'
	ppos=0
	for line in oldpdb:
		if useline(line):
			fields=[ '','' ,'' ,line[17:21],line[21],line[22:27],line[31:39],line[39:47],line[47:55],line[72:77]]
			fields[3]=fields[3].replace(" ", "") #it is a standard aa with 3 letters, eliminate whitespace.
			fields[5]=fields[5].replace(" ", "") #it is a standard RESID with 4 characters, eliminate whitespace.
			#fields[3]:Aminoacid code, fields[4]:chain, fields[5]:resid, fields[6-8]:coordinates
			cpos=fields[5]
			if fields[4]!=pfields[4] or fields[9]!=pfields[9] or fields[5]=='1': #resid count has been reseted by new chain or whatever. 
				ppos='0'
				flag=0
			if flag==1:
				cpos2=int(str(cpos),16)
				ppos2=int(str(ppos),16)
			elif flag==0:
				cpos2=int(cpos)
				ppos2=int(ppos)
			if cpos=='2710' and ppos=='9999':
				cpos2=int(cpos,16)
				flag=1

			if (fields[4]==chain or chain=='') and cpos2>=start and cpos2<=stop and (segid in line[72:77] or segid==''):
				if fields[5]!=pvresid: #if a new resid is found
					n=1 #count is not refreshed yet. your count is set in the previous aminoacid.
					try:
						while (guide[count+n][0]=='-'): #jump the deletions in the pdb (pdb:12,fasta:12)(pdb:-,fasta:13), (pdb:-,fasta:14), (pdb:13,fasta:15) you can NOT write 13 or 14!
							n=n+1
					except IndexError: #user PDB range has ended but PDB and fasta do not
						newpdb.write(line)
						continue
					count=count+n-1

					count=count+1 #Count gets NOW updated.
				spacesn=4-len(str(guide[count][1][1])) #divide the 4 columns between numbers and spaces.
				newline=line[0:22]+' '*spacesn+str(guide[count][1][1])+' '+line[27:] #the space before line[27:] is to delete the insertion code from AMBER.
				if len(str(guide[count][1][1]))==5: #AMBER notation after 9999 uses 5 digits.
					newline=line[0:22]+str(guide[count][1][1])+line[27:]
				newpdb.write(newline)
				pvresid=fields[5]

			else:
				newpdb.write(line)

			pchain=fields[4]
			ppos=cpos
		elif line.startswith('TER') and fields[4]==chain and cpos2>=start and cpos2<=stop and (segid in line[72:77] or segid==''):
			ter=line[:23]+ (3-len(str(guide[count][1][1])))*' '+str(guide[count][1][1])+'\n'
			newpdb.write(ter)

		elif line.startswith('ENDMDL'):
			break

		else:
			newpdb.write(line)

	

	newpdb.close()
	oldpdb.close()
	return '/tmp'+pdbfile[:-4]+'_corrected.pdb'
#############################################################################################################################################

def uniqueset(pdbname, segid, start, stop, chain):
	'''Checks if the definied combination of resid interval, segid and chain can lead to ambiguity. If two lines in the PDB file share the values for the resid, the segid (if defined) and chain (if defined) it will STOP the program.'''
	flag=0
	pdbset=set()
	oldpdb=open(pdbname,'r')
	pfields=['','' ,'','AAA','Z','0','0','0','0','']
	ppos=0
	for line in oldpdb:
		if useline(line):
			#fields[3]:Aminoacid code, fields[4]:chain, fields[5]:resid, fields[6-8]:coordinates
			fields=[ '','' ,'' ,line[17:21],line[21],line[22:27],line[31:39],line[39:47],line[47:55],line[72:77]]
			csegid=fields[9]
			if fields[5]!=pfields[5]: #do not run same aa more than 1 time.
				if (fields[4]!=pfields[4]) or (fields[9]!=pfields[9]) or fields[5]=='1': #different chain and new counting
					ppos=0
					flag=0
				if flag==1:
					cpos=int(fields[5],16)
				else:
					cpos=int(fields[5])
					if flag!=1 and (int(pfields[5])==9999 and cpos==2710): #decimal numbers are finished 99999->2710
						cpos=int(str(cpos),16)
						flag=1
				if (fields[4]==chain or chain=='') and cpos>=start and cpos<=stop and (segid in line[72:77] or segid==''):
					newele=str(cpos)+'_'+fields[4]+'_'+csegid
					if chain=='':
						if segid=='':
							newele=str(cpos)+'_ _ ' #only resid interval is used
						else:
							newele=str(cpos)+'_ _'+csegid #only resid interval and segid
					elif segid=='':
						newele=str(cpos)+'_'+chain+'_ ' #onlye chain and resid interval

					if newele in pdbset:
						#raise Exception('This combination:\n start:'+ str(start) + '\n stop:'+ str(stop) + '\n chain:'+ chain + '\n segid:' + segid +' \nis not unique as: ' + newele + ' is repeated')
						return 'This combination:\n start:'+ str(start) + '\n stop:'+ str(stop) + '\n chain:'+ chain + '\n segid:' + segid +' \nis not unique as: ' + newele + ' is repeated'

						oldpdb.close()
						#return False
					else:
						pdbset.add(newele)

			pfields=fields
			ppos=cpos
	oldpdb.close()
	return True

#############################################################################################################################################

def useline(line):
	'''returns True if line starts with ATOM, or HETATM with a resname included in the d dictionary''' 
	if line.startswith('ATOM') or line.startswith('HETATM'):
		trykey=line[17:21]
		trykey=trykey.replace(" ", "")
		if trykey in d.keys():
			return True
		else:
			return False #this heteroatom is not useful

	else:
		return False

#############################################################################################################################################

def segment_id(pdbname, segid, start, stop, chain):
	'''Looks for gaps in the sequence between start and stop in the given chain and segid ONCE the PDB file has been corrected. If the distance with de previous atom is bigger than 5 units it considers that the two atoms belong to different segments''' 
	seq=list()
	flag=0
	newpdb=open(pdbname[:-4]+'_corrected.pdb','r')
	pfields=['','' ,'','AAA','Z','0','0','0','0','']
	ppos=0
	ccoor=[0,0,0]
	pcoor=[0,0,0]
	for line in newpdb:
		if useline(line):
			#fields[3]:Aminoacid code, fields[4]:chain, fields[5]:resid, fields[6-8]:coordinates
			fields=[ '','' ,'' ,line[17:21],line[21],line[22:27],line[31:39],line[39:47],line[47:55],line[72:77]]
			fields[3]=fields[3].replace(" ", "")
			fields[5]=fields[5].replace(" ", "")
			ccoor[0]=float(fields[6])
			ccoor[1]=float(fields[7])
			ccoor[2]=float(fields[8])

			if fields[5]!=pfields[5]: #do not run same aa more than 1 time.
				if fields[4]!=pfields[4] or fields[9]!=pfields[9] or fields[5]=='1': #different chain and new counting
					ppos=0
					flag=0
				if flag==1:
					cpos=int(fields[5],16)
				else:
					cpos=int(fields[5])

				if flag!=1 and (int(pfields[5])==9999 and cpos==2710): #decimal numbers are finished 99999->2710
					cpos=int(str(cpos),16)
					flag=1
				if (fields[4]==chain or chain=='') and cpos>=start and cpos<=stop and (segid in line[72:77] or segid==''):
					if cpos==ppos+1: #No gap between current and previous position.
						seq.append(d[fields[3]])

					elif cpos>ppos+1: #There is a gap, but is it solded or segmented?
						distance=(((ccoor[0]-pcoor[0])**2)+((ccoor[1]-pcoor[1])**2) + ((ccoor[2]-pcoor[2])**2))**0.5

						if distance < 5: #SOLDED GAP
							for i in range(cpos-ppos-1): #if there is a jump from 2 to 4 #print 1 "-"
								seq.append('-') #seq.append('-'*cpos-ppos-1)
							try:
								seq.append(d[fields[3]])
							except:
								seq.append('X')
						else: #NEW SEGMENT
							for i in range(cpos-ppos-1):
								seq.append('/')
							seq.append('\n') #newline is IMPORTANT to represent the segment jump!

							try:
								seq.append(d[fields[3]])
							except:
								seq.append('X')


			pcoor=ccoor.copy()
			pfields=fields
			ppos=cpos

	newpdb.close()
	fullseq=''.join(seq)
	fullseq.lstrip('/') #delete starting / as they appear due to resid count jumping because of change of chains, etc.
	return fullseq




#############################################################################################################################################
def main(pdbname,fastaname,segid='',start=-1,starthex=False,stop=99999,stophex=False,chain='A'): #we need to know if start and stop are hexadecimal or not!
	if starthex is True:
		start=int(str(start),16)
	if stophex is True:
		stop=int(str(stop),16)
	if start>=stop:
		raise Exception('Start resid is larger or equal to the end resid')
		#return 'Start resid is larger or equal to the end resid'
	if len(segid)>4:
		raise Exception('Segid string length is larger than 4 characters.')
		#return 'Segid string length is larger than 4 characters.'

	if uniqueset(pdbname, segid, start, stop, chain):
		tablepdb,simplified_sequence,hexflag=checkpdb(pdbname,segid,start,stop,chain)
		#print('\n',tablepdb,simplified_sequence,'\n')
		guide=matchpdbfa(fastaname,simplified_sequence,tablepdb,hexflag)
		#print(guide,'\n') #Table containing the relation between the numbering of the original PDB file and the corrected one.
		repairpdb(pdbname,guide,segid,start,stop,chain)
		#print(segment_id(pdbname, segid, start, stop, chain),'\n')


#main('4RES.pdb','4res.fa',segid='',start=0,starthex=False,stop=999,stophex=False,chain='A')

