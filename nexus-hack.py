import os
from nexus import NexusReader
n = NexusReader()

NEXUS_DIR = os.path.join(os.path.dirname(__file__), 'nexus')
n.read_file(os.path.join(NEXUS_DIR, 'Wilberg_JVP_2015_matrix.nex'))

n = NexusReader(os.path.join(NEXUS_DIR, 'Wilberg_JVP_2015_matrix.nex'))

print "Chars:"
print n.data.nchar

print "Taxa:"
print n.data.ntaxa

print "Format:"
print n.data.format

print "Matrix Keys:"
print n.data.matrix.keys()
