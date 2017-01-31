import codecs
from matrix_utils import verifyTaxa


class TxtHandler():
  """ Txt File Type implementation of matrix handling needs """

  input_file = None
  first_line = None
  ncols = 0
  nrows = 0
  custom_block = None

  def __init__(self, input_file):
    self.input_file = input_file
    self.read_file()

  def read_file(self):
  
    with open( self.input_file, 'r') as f:
      self.first_line = f.readline()
   
      # xread has some other potential clues
      xread_filename = f.readline().strip().replace("'", "")
      xread_matrix_dimensions = f.readline()
      lines = f.readlines()

      f.close

    if "#NEXUS" == self.first_line.strip():
      print "text file is nexus"
  
      # TODO: rename file to .nex
      # TODO: restart mediator with new file

    elif "xread" == self.first_line.strip():
    
      print "xread format found"

      dimensions = str(xread_matrix_dimensions).split(' ')
      self.ncols = int(dimensions[0])
      self.nrows = int(dimensions[1])

      custom_block = "\n\nBEGIN VERIFIED_TAXA;\n"
      custom_block += "Dimenstions ntax=" + str(self.nrows) + "nchar=4;\n"

      matrix = ""
      line_buffer = ""
      for l in lines:
        if ";proc/;" != l.strip():

          if line_buffer:
            line_row = line_buffer + " " + l.strip()
          else:
            line_row = l.strip()
        
          if len(line_row) >= self.ncols:
 
            # reconstitute broken rows, then remove space/tabbing
            line_parts = line_row.split(' ')
            line_parts = list(filter(None, line_parts))

            taxon_name = line_parts[0]
            taxon_chars = line_parts[1].replace("[", "{")
            taxon_chars = taxon_chars.replace("]", "}")
          
            #  verify taxa
            verified_taxa = verifyTaxa(taxon_name)
            verified_name = None

            if verified_taxa:
              for taxa in verified_taxa:
                verified_name = taxa['name_string'].lower()
                custom_block += taxon_name + "    " + taxa['name_string'] + "    " + taxa['match_value'] + "    " + taxa['datasource'] + "\n"

              matrix += "    " + verified_name + "    " + taxon_chars.strip() + "\n"
            else:

              custom_block += taxon_name + "\n"
              matrix += "    " + taxon_name.strip() + "    " + taxon_chars.strip() + "\n"

            line_buffer = ""
          else:
            line_buffer += l.strip()

      custom_block += ";\n"
      custom_block += "END;\n"

      self.custom_block = custom_block      
 
      #print "matrix content: "
      #print matrix

      # print " We need to write NEXUS File"
     
      nexus_file = codecs.open('./nexus/' + xread_filename + '.nex', 'w', 'utf-8')
      nexus_file.write("#NEXUS\n")
      nexus_file.write("[Morphobank Generated Neuxus file]\n\n")

      # Data Section
      nexus_file.write("BEGIN DATA;\n")
      nexus_file.write("    DIMENSIONS NTAX=" + str(self.nrows) + " NCHAR=" + str(self.ncols) + ";\n")
      nexus_file.write('    FORMAT GAP=- MISSING=? DATATYPE=STANDARD SYMBOLS="  0 1 2 3";\n')
      nexus_file.write("    MATRIX\n")
      nexus_file.write(matrix)
      nexus_file.write(";\nEND;\n\n")

      # Custom Block Section
      nexus_file.write(custom_block)
      nexus_file.close()      



    else:
      print "do not know how to process this .txt file"

