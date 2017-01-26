import os
import sys
import xlrd
import json
import requests
from nexus import NexusWriter, NexusReader
from math import trunc


# init
dir_path = os.path.dirname(os.path.realpath(__file__))
input_file = dir_path + '/' + sys.argv[1]

# util
def is_number(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

def verifyTaxa(sci_name):

  sanitized_sci_name = sci_name.replace('H_', '')

  print "in verifyTaxa, looking up name: " + sci_name

  verifiedTaxa = []

  # NCBI is what Morphobank uses, checking all to try to get as many verified as possible
  data_sources = '4' 
  gnparser_url = 'http://resolver.globalnames.org/name_resolvers.json?perferred_data_sources=' + data_sources + '&best_match_only=true&resolve_once=false&names='
 
  gnparser = requests.get(gnparser_url + sanitized_sci_name + '&with_context=true')
  if 200 == gnparser.status_code:
    gnp_json = json.loads( gnparser.content )

    for data in gnp_json['data']:
      if data['is_known_name']:
        
        verifiedTaxa.append({
          "datasource": data['results'][0]['data_source_title'],
          "match_value": data['results'][0]['match_value'],
          "name_string": data['results'][0]['name_string']
        })

  return verifiedTaxa


# check file
if os.path.isfile(input_file):
 
  filename, file_extension = os.path.splitext(input_file)

  if ".nex" == file_extension:

    # If we have a nexus file already, we should verify the taxa and add our custom block,
    # do any syntax clean up needed to get Mesquite to parse without error

    nr = NexusReader(input_file)
    nrows = nr.data.ntaxa

    custom_block = "\n\nBEGIN VERIFIED_TAXA;\n"
    custom_block += "Dimensions ntax=" + str(nrows) + " nchar=4;\n" 

    for tax in nr.data.taxa:

      verified_taxa = verifyTaxa(tax)
      verified_name = None 

      if verified_taxa:
        for taxa in verified_taxa:
          verified_name = taxa['name_string'].lower()
          custom_block += tax + "    " + taxa['name_string'] + "    " + taxa['match_value'] + "    " + taxa['datasource'] + "\n"
      else:
        custom_block += tax + "\n"

    custom_block += ";\n"
    custom_block += "END;\n\n"

    #### quick and dirty append Custom Block ####
    nexus_file = open(input_file, 'a')
    nexus_file.write(custom_block)
    nexus_file.close()

  elif ".xlsx" == file_extension:

    book = xlrd.open_workbook(input_file)
    sh = book.sheet_by_index(0)

    nw = NexusWriter()
 
    nrows = sh.nrows
    ncols = sh.ncols


    
    ##################
    # Write To Nexus
    ##################

    nw.add_comment("Morphobank generated Nexus File")

    custom_block = "\n\nBEGIN VERIFIED_TAXA;\n"
    custom_block += "Dimensions ntax=" + str(nrows) + " nchar=4;\n" 

    # Species List Taxa
    for rx in range(nrows):
      if rx:

        taxon_name = str(sh.cell_value(rowx=rx, colx=0)).strip()
        print "taxon name: " + taxon_name

        verified_taxa = verifyTaxa(taxon_name)
        verified_name = None 

        if verified_taxa:
          for taxa in verified_taxa:
            verified_name = taxa['name_string'].lower()
            custom_block += taxon_name + "    " + taxa['name_string'] + "    " + taxa['match_value'] + "    " + taxa['datasource'] + "\n"
        else:
          custom_block += taxon_name + "\n"

        for cx in range(ncols):
          if cx:
        
            print "getting cell value for: " + taxon_name

            if is_number( sh.cell_value(rowx=rx, colx=cx)):
              cell_value = int(sh.cell_value(rowx=rx, colx=cx))
            else:
              cell_value = sh.cell_value(rowx=rx, colx=cx)
              cell_value = cell_value.replace("{", "(")
              cell_value = cell_value.replace("}", ")")
        
            if verified_name:
              nw.add(verified_name, cx, cell_value)
            else:
              nw.add(taxon_name, cx, cell_value)

  custom_block += ";\n"
  custom_block += "END;\n"

  nw.write_to_file(filename="output.nex", interleave=False, charblock=False)

  #### quick and dirty append Custom Block ####
  nexus_file = open('output.nex', 'a')
  nexus_file.write(custom_block)
  nexus_file.close()

else:
  print "file not found"









