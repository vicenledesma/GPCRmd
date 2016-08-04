import re
import sys
import time
import requests
def valid_uniprotkbac(uniprotkbac):
    reupkbac1 = re.compile(r'^[OPQ][0-9][A-Z0-9]{3}[0-9]([-][0-9]*)?$')
    reupkbac2 = re.compile(r'^[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}([-][0-9]*)?$')
    if reupkbac1.search(str(uniprotkbac)) is not None or reupkbac2.search(uniprotkbac) is not None:
      return True
    else:
      return False
    
def retreive_protein_names_uniprot(acnum):
    URL = 'http://www.uniprot.org/uniprot/'
    SIZE_LIMIT = 512000
    RECIEVE_TIMEOUT = 120
    response = requests.get(URL+str(acnum)+'&format=txt',timeout=30,stream=True)
    if response.status_code != 404 or response.status_code != 410:
        response.raise_for_status()
    else:
        response.close()
        return None
    encoding = response.encoding
    proteindesc = re.compile('^DE\s+')
    fullrecname = re.compile('^DE\s+RecName:\s+Full=(.*);')
    shortrecname = re.compile('^DE\s+RecName:\s+Short=(.*);')
    fullaltname = re.compile('^DE\s+AltName:\s+Full=(.*);')
    shortaltname = re.compile('^DE\s+AltName:\s+Short=(.*);')
    fullname = re.compile('^DE\s+Full=(.*);')
    shortname = re.compile('^DE\s+Short=(.*);')
    data = dict()
    data['RecName'] = []
    data['AltName'] = []
    data['RecName'].append({'Full' : [], 'Short' : []})
    data['AltName'].append({'Full' : [], 'Short' : []})
    defound = False
    lastfield = ''
    size = 0
    start = time.time()
    lines = response.iter_lines()
    for line in lines:
        if size > SIZE_LIMIT:
            raise ValueError('response too large')
        if time.time() - start > RECIEVE_TIMEOUT:
            raise ValueError('timeout reached')
        uline = line.decode(encoding)
        
        

        #if protein description section DE starts
        if proteindesc.match(uline):
            if not defound:
                defound = True
            #parser
            fullrecnamematch = fullrecname.match(uline)
            if fullrecnamematch:
                data['RecName'][-1]['Full'].append(fullrecnamematch.group(1).strip())
                lastfield = 'RecName'
            else:
                shortrecnamematch = shortrecname.match(uline)
                if shortrecnamematch:
                    data['RecName'][-1]['Short'].append(shortrecnamematch.group(1).strip())
                    lastfield = 'RecName'
                else:
                    fullaltnamematch = fullaltname.match(uline)
                    if fullaltnamematch:
                        data['AltName'][-1]['Full'].append(fullaltnamematch.group(1).strip())
                        lastfield = 'AltName'
                    else:
                        shortaltnamematch = shortaltname.match(uline)
                        if shortaltnamematch:
                            data['AltName'][-1]['Short'].append(shortaltnamematch.group(1).strip())
                            lastfield = 'AltName'
                        else:
                            fullnamematch = fullname.match(uline)
                            if fullnamematch:
                                data[lastfield][-1]['Full'].append(fullnamematch.group(1).strip())
                            else:
                                shortnamematch = shortname.match(uline)
                                if shortnamematch:
                                    data[lastfield][-1]['Short'].append(shortnamematch.group(1).strip())
                                else:
                                    continue         
            
        else:
            #if protein description section DE ends, stop the parser
            if defound:
                break
        
        size += sys.getsizeof(line) 


    response.close()

    return data
    
def get_other_names(protnames):
    if len(data['RecName'][0]['Full']) > 0:
        name = data['RecName'][0]['Full'][0]
    else:
        name = None
    other_names = []
    for sfdict in data['RecName'][1:]:
        for oname in sfdict['Full']:
            other_names.append(oname)
        for oname in sfdict['Short']:
            other_names.append(oname)
    for sfdict in data['AltName']:
        for oname in sfdict['Full']:
            other_names.append(oname)
        for oname in sfdict['Short']:
            other_names.append(oname)
    return(name, other_names)


def retreive_data_uniprot(acnum,columns='id,entry name,reviewed,protein names,organism,length'):
  ### Returns a dictionary with the selected columns as keys. 'id' --> 'entry'
    URL = 'http://www.uniprot.org/uniprot/'
    SIZE_LIMIT = 51200
    RECIEVE_TIMEOUT = 120
    response = requests.get(URL+str(acnum)+'&columns='+columns+'&format=tab',timeout=30,stream=True)
    if response.status_code != 404 and response.status_code != 410:
        response.raise_for_status()
    else:
        response.close()
        return None
    encoding = response.encoding
    data = dict()
    size = 0
    start = time.time()
    lines = response.iter_lines()
    headersread=False
    for line in lines:
        if size > SIZE_LIMIT:
            raise ValueError('response too large')
        if time.time() - start > RECIEVE_TIMEOUT:
            raise ValueError('timeout reached')
        uline = line.decode(encoding)
        vallist = uline.split('\t')
        if headersread:
            for header,value in zip(headers,vallist):
                data[str(header.strip())] = value.strip()
        else:
            #do only for first line
            headers = vallist
            headersread = True
                
        size += sys.getsizeof(line) 


    response.close()
    return data
    
def retreive_fasta_seq_uniprot(acnum):
    URL = 'http://www.uniprot.org/uniprot/'
    SIZE_LIMIT = 51200
    RECIEVE_TIMEOUT = 120
    response = requests.get(URL+str(acnum)+'&format=fasta',timeout=30,stream=True)
    if response.status_code != 404 or response.status_code != 410:
        response.raise_for_status()
    else:
        response.close()
        return None
    encoding = response.encoding
    data = dict()
    sequence=''
    size = 0
    start = time.time()
    lines = response.iter_lines()
    headerread=False
    for line in lines:
        if size > SIZE_LIMIT:
            raise ValueError('response too large')
        if time.time() - start > RECIEVE_TIMEOUT:
            raise ValueError('timeout reached')
        uline = line.decode(encoding)
        print(uline)

        if headerread:
            sequence += uline
        else:
            #do only for first line
            header = uline
            headerread = True
                
        size += sys.getsizeof(line) 


    response.close()
    return(sequence, header)
