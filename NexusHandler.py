import codecs
from nexus import NexusReader
from matrix_utils import verifyTaxa

class NexusHandler():
  """ Nexus File Type implementation of matrix handling needs """

  input_file = None
  ncols = 0
  nrows = 0
  custom_block = None

  def __init__(self, input_file):
    self.input_File = input_file
    self.read_file()

  def read_file(self):

    # If we have a nexus file already, we should verify the taxa and add custom block,
    # do any syntax cleanup needed to get Mesquire to parse without error.

    nr = NexusReader(self.input_file)
    self.nrows = nr.data.ntaxa

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

    self.custom_block = custom_block

    ### Simple Append to end of file ####
    nexus_file = codecs.open(self.input_file, 'a', 'utf-8')
    nexus_file.write(self.custom_block)
    nexus_file.close()

