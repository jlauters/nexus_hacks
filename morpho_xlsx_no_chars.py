import xlrd
from nexus import NexusWriter
from math import trunc

nw = NexusWriter()
book = xlrd.open_workbook("matrices/Appendix_S7_-_Morphological_matrix.xlsx")
sh = book.sheet_by_index(0)

##################
# Write To Nexus
##################

# util
def is_number(s):
  try:
    int(s)
    return True
  except ValueError:
    return False


nw.add_comment("Morphobank generated Nexus File")

# Species List Taxa
for rx in range(sh.nrows):

  if rx:
    for cx in range(sh.ncols):
      if cx:

        value = None
        taxon_name = str(sh.cell_value(rowx=rx, colx=0)).strip()

        if is_number( sh.cell_value(rowx=rx, colx=cx)):
          value = int(sh.cell_value(rowx=rx, colx=cx))
        else:
          value = sh.cell_value(rowx=rx, colx=cx)

        nw.add(taxon_name, cx, value)

nw.write_to_file(filename="output.nex", interleave=False, charblock=False)



