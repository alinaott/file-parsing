import re

# checking cosmic genes for any not present in the CCDS gene list
ccds = open("CCDS.20160908.gene_name.cons.bed", 'r')
onco = open("cosmic_genes.csv", 'r')
output = open('cosmic_non_CCDS.bed', 'w')

genes = []
for i in ccds:
    genes.append(i.strip().split()[3])

next(onco)
for i in onco:
    fields = i.strip().split(",")
    ogene = str(fields[0])
    opos = fields[3]
    osyn = fields[19]
    # loop over the synonyms to see if any match genes; print if they don't
    if ogene not in genes:
        syns = osyn.split()
        for x in syns:
            if x not in genes and ogene not in genes:
                genes.append(ogene)
                chrom,start,stop = re.split('\W+', opos)
                output.write("{0}\t{1}\t{2}\t{3}".format(chrom, start, stop, str(ogene)))
    else:
        genes.append(ogene)
output.close()
ccds.close()
onco.close()
        
# pulling out gene names from genocde GTF file
ccds = open("CCDS.20160908.gene_name.cons.bed", 'r')
gencode = open("gencode.v29.annotation.gtf", 'r')
output = open('gencode.bed', 'w')

genes = []
for i in ccds:
    genes.append(i.strip().split()[3])
    
for l in gencode:
	if l.startswith('#'):
		continue
	fields = l.strip().split("\t")
	info = fields[8]
	# only using manual, full gene transcript info
	if fields[2] == 'gene' & fields[1] == "HAVANA":
		gene = re.search(r'gene_name\s"(\w+)', info).group(1)
		output.write("{0}\t{1}\t{2}\t{3}".format(fields[0], fields[3], fields[4], gene)
output.close()
ccds.close()
gencode.close()

# combining files
ccds = open("CCDS.20160908.gene_name.cons.bed", 'r')
onco = open('cosmic_genes_not_in_CCDS.bed', 'r')
gencode = open('gencode.bed', 'r')
output = open('ccds_cosmic_gencode.bed', 'w')

# output only genes and positions if not already present
genes = []
for i in ccds:
    genes.append(i.strip().split()[3])
    output.write(i)
    
for i in onco:
	if i.strip().split()[3] not in genes:
	    genes.append(i.strip().split()[3])
    	output.write(i)

for i in gencode:
	if i.strip().split()[3] not in genes:
	    genes.append(i.strip().split()[3])
    	output.write(i)

output.close()
ccds.close()
gencode.close()
onco.close()
