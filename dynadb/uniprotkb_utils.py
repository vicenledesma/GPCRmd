import re
import sys
import time
import requests
from requests.exceptions import HTTPError,ConnectionError,Timeout,TooManyRedirects
from django.conf import settings

class StreamSizeLimitError(Exception):
    pass
class StreamTimeoutError(Exception):
    pass
class ParsingError(Exception):
    pass


def valid_uniprotkbac(uniprotkbac):
    reupkbac1 = re.compile(r'^[OPQ][0-9][A-Z0-9]{3}[0-9]([-][0-9]*)?$')
    reupkbac2 = re.compile(r'^[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}([-][0-9]*)?$')
    if reupkbac1.search(str(uniprotkbac)) is not None or reupkbac2.search(uniprotkbac) is not None:
      return True
    else:
      return False
    
def retreive_protein_names_uniprot(acnum,size_limit=5242880,buffer_size=512000,recieve_timeout=120,connect_timeout=30):
    URL = 'http://www.uniprot.org/uniprot/?'
    data = dict()
    errdata = dict()
    do_not_skip_on_debug = False
    try:
      response = requests.get(URL+'query=accession:'+str(acnum)+'&format=txt',timeout=recieve_timeout,stream=True)
      response.raise_for_status()
      encoding = response.encoding
      proteindesc = re.compile('^DE\s+')
      fullrecname = re.compile('^DE\s+RecName:\s+Full=(.*);')
      shortrecname = re.compile('^DE\s+RecName:\s+Short=(.*);')
      fullaltname = re.compile('^DE\s+AltName:\s+Full=(.*);')
      shortaltname = re.compile('^DE\s+AltName:\s+Short=(.*);')
      fullname = re.compile('^DE\s+Full=(.*);')
      shortname = re.compile('^DE\s+Short=(.*);')
      data['RecName'] = []
      data['AltName'] = []
      data['RecName'].append({'Full' : [], 'Short' : []})
      data['AltName'].append({'Full' : [], 'Short' : []})
      defound = False
      lastfield = ''
      
      size = 0
      chunkend = False
      remain = ''
      start = time.time()
      chunks = response.iter_content(chunk_size=buffer_size)
      while True:
        try:
          chunk = next(chunks)
          size += sys.getsizeof(chunk)
          if size > size_limit:
                raise StreamSizeLimitError('Response too large.')
          if time.time() - start > recieve_timeout:
                raise StreamTimeoutError('Stream download time limit reached.')
          chunk = chunk.decode(encoding)
          chunk = remain+chunk
        except StopIteration:
          if chunkend:
            break
          else:
            lines = [remain]
            chunkend = True
            pass
        except:
          raise
        else:
          lines = chunk.split('\n')
          remain = lines.pop()
          for line in lines:
            #if protein description section DE starts
            if line != '':
              if proteindesc.match(line):
                  defound = True
                  #parser
                  fullrecnamematch = fullrecname.match(line)
                  if fullrecnamematch:
                      data['RecName'][-1]['Full'].append(fullrecnamematch.group(1).strip())
                      lastfield = 'RecName'
                  else:
                      shortrecnamematch = shortrecname.match(line)
                      if shortrecnamematch:
                          data['RecName'][-1]['Short'].append(shortrecnamematch.group(1).strip())
                          lastfield = 'RecName'
                      else:
                          fullaltnamematch = fullaltname.match(line)
                          if fullaltnamematch:
                              data['AltName'][-1]['Full'].append(fullaltnamematch.group(1).strip())
                              lastfield = 'AltName'
                          else:
                              shortaltnamematch = shortaltname.match(line)
                              if shortaltnamematch:
                                  data['AltName'][-1]['Short'].append(shortaltnamematch.group(1).strip())
                                  lastfield = 'AltName'
                              else:
                                  fullnamematch = fullname.match(line)
                                  if fullnamematch:
                                      data[lastfield][-1]['Full'].append(fullnamematch.group(1).strip())
                                  else:
                                      shortnamematch = shortname.match(line)
                                      if shortnamematch:
                                          data[lastfield][-1]['Short'].append(shortnamematch.group(1).strip())
                                      else:
                                          continue         
                  
              else:
                  #if protein description section DE ends, stop the parser
                  if defound:
                      return
            


    except HTTPError:
      errdata['Error'] = True
      errdata['ErrorType'] = 'HTTPError'
      errdata['status_code'] = response.status_code
      errdata['reason'] = response.reason
    except ConnectionError as e:
      errdata['Error'] = True
      errdata['ErrorType'] = 'ConnectionError'
      errdata['reason'] = 'Cannot connect.'
    except Timeout as e:
      errdata['Error'] = True
      errdata['ErrorType'] = 'Timeout'
      errdata['reason'] = 'Timeout exceeded.'
    except TooManyRedirects as e:
      errdata['Error'] = True
      errdata['ErrorType'] = 'TooManyRedirects'
      errdata['reason'] = 'Too many redirects.'
    except StreamSizeLimitError as e:
      errdata['Error'] = True
      errdata['ErrorType'] = 'StreamSizeLimitError'
      errdata['reason'] = str(e)
    except StreamTimeoutError as e:
      errdata['Error'] = True
      errdata['ErrorType'] = 'StreamTimeoutError'
      errdata['reason'] = str(e)

    except:
      errdata['Error'] = True
      errdata['ErrorType'] = 'Internal'
      do_not_skip_on_debug = True
      raise
    finally:
      try:
        response.close()
      except:
        pass
      if not (settings.DEBUG and do_not_skip_on_debug):
        return (data,errdata)

    
def get_other_names(protnames):
    name = ''
    other_names = []

    if len(protnames['RecName'][0]['Full']) > 0:
        name = protnames['RecName'][0]['Full'][0]
    if len(protnames['RecName'][0]['Short']) > 0:
        if name == '':
          name = protnames['RecName'][0]['Short'][0]
        else:
          other_names.append(protnames['RecName'][0]['Short'][0])
          
    if len(protnames['RecName'][0]['Full']) > 1:
      for oname in protnames['RecName'][0]['Full'][1:]:
        other_names.append(oname)
    if len(protnames['RecName'][0]['Short']) > 1:
      for oname in protnames['RecName'][0]['Short'][1:]:
        other_names.append(oname)
        
    if len(protnames['RecName']) > 1:   
      for sfdict in protnames['RecName'][1:]:
          for oname in sfdict['Full']:
              other_names.append(oname)
          for oname in sfdict['Short']:
              other_names.append(oname)

    for sfdict in protnames['AltName']:
        for oname in sfdict['Full']:
            other_names.append(oname)
        for oname in sfdict['Short']:
            other_names.append(oname)
    return(name, other_names)


def retreive_data_uniprot(acnum,columns='id,entry name,reviewed,protein names,organism,length',\
  size_limit=512000,buffer_size=512000,recieve_timeout=120,connect_timeout=30):
  ### Returns a dictionary with the selected columns as keys. 'id' --> 'entry'
    URL = 'http://www.uniprot.org/uniprot/?'
    data = dict()
    errdata = dict()
    do_not_skip_on_debug = False
    try:
      response = requests.get(URL+'query=accession:'+str(acnum)+'&columns='+columns+'&format=tab',timeout=connect_timeout,stream=True)
      response.raise_for_status()
      encoding = response.encoding
      
      size = 0
      start = time.time()
      headersread=False
      chunkend = False
      remain = ''
      chunks = response.iter_content(chunk_size=buffer_size)
      while True:
        
        
        try:
          
          chunk = next(chunks)
          size += sys.getsizeof(chunk)
          if size > size_limit:
                raise StreamSizeLimitError('Response too large.')
          if time.time() - start > recieve_timeout:
                raise StreamTimeoutError('Stream download time limit reached.')
          chunk = chunk.decode(encoding)
          chunk = remain+chunk
          
        except StopIteration:
          if chunkend:
            break
          else:
            lines = [remain]
            chunkend = True
            pass
        except:
          raise
        else:
          lines = chunk.split('\n')
          remain = lines.pop()
        for line in lines:

            if line != '':
              vallist = line.split('\t')
              if headersread:
                  if len(headers) == len(vallist):
                    for header,value in zip(headers,vallist):
                        data[str(header.strip())] = value.strip()
                    response.close()
                    return
                  else:
                    raise ParsingError('Error parsing data.')
              else:
                  #do only for first line
                  
                  headers = vallist
                  headersread = True
                   
            

    except HTTPError:
      errdata['Error'] = True
      errdata['ErrorType'] = 'HTTPError'
      errdata['status_code'] = response.status_code
      errdata['reason'] = response.reason
    except ConnectionError as e:
      errdata['Error'] = True
      errdata['ErrorType'] = 'ConnectionError'
      errdata['reason'] = 'Cannot connect.'
    except Timeout as e:
      errdata['Error'] = True
      errdata['ErrorType'] = 'Timeout'
      errdata['reason'] = 'Timeout exceeded.'
    except TooManyRedirects as e:
      errdata['Error'] = True
      errdata['ErrorType'] = 'TooManyRedirects'
      errdata['reason'] = 'Too many redirects.'
    except StreamSizeLimitError as e:
      errdata['Error'] = True
      errdata['ErrorType'] = 'StreamSizeLimitError'
      errdata['reason'] = str(e)
    except StreamTimeoutError as e:
      errdata['Error'] = True
      errdata['ErrorType'] = 'StreamTimeoutError'
      errdata['reason'] = str(e)

    except ParsingError as e:
      errdata['Error'] = True
      errdata['ErrorType'] = 'ParsingError'
      errdata['reason'] = str(e)
    except:
      errdata['Error'] = True
      errdata['ErrorType'] = 'Internal'
      do_not_skip_on_debug = True
      raise
    finally:
      try:
        response.close()
      except:
        pass
      if not (settings.DEBUG and do_not_skip_on_debug):
        return (data,errdata)
def retreive_fasta_seq_uniprot(acnum,size_limit=102400,buffer_size=512000,recieve_timeout=120,connect_timeout=30):
    URL = 'http://www.uniprot.org/uniprot/'
    data = dict()
    errdata = dict()
    do_not_skip_on_debug = False
    try:
      response = requests.get(URL+str(acnum)+'.fasta',timeout=recieve_timeout,stream=True)
      response.raise_for_status()
      encoding = response.encoding
      sequencere = re.compile('^[A-Z]+$')
      header=''
      sequence=''
      size = 0
      headerread=False
      chunkend = False
      remain=''
      start = time.time()
      chunks = response.iter_content(chunk_size=buffer_size)
      while True:
        try:
          
          chunk = next(chunks)
          size += sys.getsizeof(chunk)
          if size > size_limit:
                raise StreamSizeLimitError('Response too large.')
          if time.time() - start > recieve_timeout:
                raise StreamTimeoutError('Stream download time limit reached.')
          chunk = chunk.decode(encoding)
          chunk = remain+chunk
          
        except StopIteration:
          if chunkend:
            break
          else:
            lines = [remain]
            chunkend = True
            pass
        except:
          raise
        else:
          lines = chunk.split('\n')
          remain = lines.pop()   
        for line in lines:
            if line != '':
              isheader = line.find('>sp|') == 0 or line.find('>tr|') == 0
              if headerread or not isheader:
                  if sequencere.search(line):
                    sequence += line.replace('-','X')
                  elif line.find('*') < 0:
                    ParsingError('Cannot parse fasta line:\n'+' translation stop character ("*") not accepted.')
                  elif isheader:
                    return
                  else:
                    raise ParsingError('Cannot parse fasta line:\n'+'"'+line+'"')
              else:
                  #do only for header
                  header = line
                  headerread = True
        data['header'] = header
        data['sequence'] = sequence

    except HTTPError:
      errdata['Error'] = True
      errdata['ErrorType'] = 'HTTPError'
      errdata['status_code'] = response.status_code
      errdata['reason'] = response.reason
    except ConnectionError as e:
      errdata['Error'] = True
      errdata['ErrorType'] = 'ConnectionError'
      errdata['reason'] = 'Cannot connect.'
    except Timeout as e:
      errdata['Error'] = True
      errdata['ErrorType'] = 'Timeout'
      errdata['reason'] = 'Timeout exceeded.'
    except TooManyRedirects as e:
      errdata['Error'] = True
      errdata['ErrorType'] = 'TooManyRedirects'
      errdata['reason'] = 'Too many redirects.'
    except StreamSizeLimitError as e:
      errdata['Error'] = True
      errdata['ErrorType'] = 'StreamSizeLimitError'
      errdata['reason'] = str(e)
    except StreamTimeoutError as e:
      errdata['Error'] = True
      errdata['ErrorType'] = 'StreamTimeoutError'
      errdata['reason'] = str(e)

    except ParsingError as e:
      errdata['Error'] = True
      errdata['ErrorType'] = 'ParsingError'
      errdata['reason'] = str(e)
    except:
      errdata['Error'] = True
      errdata['ErrorType'] = 'Internal'
      do_not_skip_on_debug = True
      raise
    finally:
      try:
        response.close()
      except:
        pass
      if not (settings.DEBUG and do_not_skip_on_debug):
        return (data,errdata)
def retreive_isoform_data_uniprot(acnum,\
  size_limit=512000,buffer_size=512000,recieve_timeout=120,connect_timeout=30):
  COLUMNS='comment(ALTERNATIVE PRODUCTS)'
  KEYS = set(('Synonyms', 'Event', 'Named isoforms', 'Sequence', 'Note', 'Name', 'IsoId','Comment'))
  do_not_skip_on_debug = False
  data,errdata = retreive_data_uniprot(acnum,columns=COLUMNS,\
  size_limit=size_limit,buffer_size=buffer_size,recieve_timeout=recieve_timeout,connect_timeout=connect_timeout)
  try:

    if data == dict():
      return
    elif 'Alternative products (isoforms)' not in data.keys():
      raise ParsingError('Cannot parse isoform data.')

    rawdata = data.pop('Alternative products (isoforms)')
    if rawdata.find('ALTERNATIVE PRODUCTS:') == 0:
      rawdata = rawdata[22:].strip()
      rows = rawdata.split(';')
      if rawdata[-1] == ';':
        rows.pop()
      for row in rows:

        row = row.strip()
        keyval = row.split('=')
        key = keyval[0]
        val = keyval[1].strip()
        if key not in data.keys():
          data[key] = []
        if key not in set(('Name','Note','Comment')):
          val = [i.strip() for i in val.split(',')]
        data[key].append(val)
        if data.keys() == KEYS:
          for acnlist,seqlist in zip(data['IsoId'],data['Sequence']):
            for seq in seqlist:
              if seq == 'Displayed':
                data['Displayed'] = acnlist[0]
                
        else:
          raise ParsingError('Cannot parse isoform data, invalid format.')
    elif rawdata != '':
      raise ParsingError('Cannot parse isoform data.')
  except ParsingError as e:
    errdata['Error'] = True
    errdata['ErrorType'] = 'ParsingError'
    errdata['reason'] = str(e)
  except:
    errdata['Error'] = True
    errdata['ErrorType'] = 'Internal'
    do_not_skip_on_debug = True
    raise
  finally:
    if not (settings.DEBUG and do_not_skip_on_debug):
      return (data,errdata)
  

  
