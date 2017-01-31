import os
import sys
from matrix_mediator import matrixMediator


# init
dir_path = os.path.dirname(os.path.realpath(__file__))
input_file = dir_path + '/' + sys.argv[1]

mediator = matrixMediator(input_file)

print "Handler:"
print mediator.matrixHandler


"""

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
    nexus_file = codecs.open(input_file, 'a', 'utf-8')
    nexus_file.write(custom_block)
    nexus_file.close()

  elif ".xlsx" == file_extension or ".xls" == file_extension:

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

  elif ".txt" == file_extension:
    print "text file detected"
 
    # Infer if Nexus or otherwise:
    with open(input_file, 'r') as f:
      first_line = f.readline()
      xread_filename = f.readline()
      xread_matrix_dimensions = f.readline()
      lines = f.readlines()
      f.close()

      print "first line:"
      print first_line

    if "#NEXUS" == first_line.strip():
      print "text file is nexus!"

      # TODO: file to filename + .nex
      # TODO: restart script / recall begining ( refactored ) function 

    elif "xread" == first_line.strip():
 
      print "xread format found"
      dimensions = str(xread_matrix_dimensions).split(' ')

      ncols = int(dimensions[0])
      nrows = int(dimensions[1])

      print 'rows: ' + str(nrows)
      print 'cols: ' + str(ncols)


      custom_block = "\n\nBEGIN VERIFIED_TAXA;\n"
      custom_block += "Dimensions ntax=" + str(nrows) + " nchar=4;\n" 

      # This could be a MatLab module to read excel files
      # https://www.mathworks.com/matlabcentral/fileexchange/48551-the-x-collection/content/XRead.m?requestedDomain=www.mathworks.com

      # this starts with line 4  since we check the first and second line above
      line_buffer = ""
      for l in lines:

        if "proc/;" != l:

          if line_buffer:
            line_row = line_buffer + " " + l 
          else:
            line_row = l

          if len(line_row) >= ncols:

            # reconsitute broken rows, then remove space / tabbing issues
            line_parts = line_row.split(' ')
            line_parts = list(filter(None, line_parts))

            taxon_name = line_parts[0]
            taxon_chars = line_parts[1]

            # verify taxa
            verified_taxa = verifyTaxa(taxon_name)
            verified_name = None 

            if verified_taxa:
              for taxa in verified_taxa:
                verified_name = taxa['name_string'].lower()
                custom_block += taxon_name + "    " + taxa['name_string'] + "    " + taxa['match_value'] + "    " + taxa['datasource'] + "\n"
            else:
              custom_block += taxon_name + "\n"

         
            line_buffer = ""

          else: 
            line_buffer += l.strip()



      custom_block += ";\n"
      custom_block += "END;\n"

      print "Custom Block"
      print custom_block

    else:
      print "no idea what to do with this ..."

  else:
    print "File extension is unrecognized"

else:
  print "file not found"

"""

