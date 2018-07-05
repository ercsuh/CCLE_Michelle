import gzip
import requests

# Download CCLE data from the given url
# Chunk the data into a new file because it's super huge
url = "https://osf.io/brkh6/download"
CCLE_data = requests.get(url, stream=True)
with open("CCLE_data.tsv.gz", "wb") as tsv:
    for chunk in CCLE_data.iter_content(chunk_size=1000):

        # Writing one chunk at a time to tsv file
        if chunk:
            tsv.write(chunk)

# Open files for reading and writing
CCLE_file = gzip.open("CCLE_data.tsv.gz", "r")  # File downloaded above
lines_file = open("CCLE_celllines_wanted.txt", "r")  # Contains the cell lines needed, categorized by group
outFile = open("transcripts_HPRT1_TK1.tsv", 'w')  # File to write output to

# Create dictionary from lines_file - {key = group : value = cell line}
lines_dict = {}
groups = lines_file.readline().strip('\n').split('\t')  # Contains group names
for group in groups:  # Initialize dictionary
    lines_dict[group] = []

for line in lines_file:  # Add to dictionary
    line = line.strip('\n').split('\t')
    if line[0] != "NA":
        lines_dict["WildType"].append(line[0])
    if line[1] != "NA":
        lines_dict["Null"].append(line[1])
    if line[2] != "NA":
        lines_dict["R175H"].append(line[2])
    if line[3] != "NA":
        lines_dict["R248Q"].append(line[3])
    if line[4] != "NA":
        lines_dict["R273H"].append(line[4])

# Create dictionary from CCLE_file using lines_dict - {key = cell line : value = index of cell line in CCLE_file}
index_dict = {}
cell_lines = CCLE_file.readline().decode().strip('\n').split('\t')  # Contains all cell lines from CCLE_file
for group in lines_dict:
    for cell_line in cell_lines:
        for my_line in lines_dict[group]:
            if my_line in cell_line:
                index_dict[my_line] = cell_lines.index(cell_line)

# # Write all cell lines to a file
# outCellLines = open("CCLE_celllines.tsv", 'w')
# outCellLines.write("CELL LINES\n")
# for line in cell_lines:
#     keep = line[7:]
#     keep = keep[:-2]
#     outCellLines.write("{}\n".format(keep))
# outCellLines.close()

outFile.write("Gene\tTranscriptID\tTranscriptType\tGroup\tCell_Line\tValue\n")  # Column headers for output file

for line in CCLE_file:
    line = line.decode().strip('\n').split('\t')
    data = line[0].split('|')  # The first column has a bunch of data separated by '|'
    if data[5] == "HPRT1" or data[5] == "TK1":
        for group in lines_dict:
            for my_line in lines_dict[group]:
                outFile.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format
                              (data[5], data[4], data[7], group, my_line, line[index_dict[my_line]]))

# Close all files
CCLE_file.close()
lines_file.close()
outFile.close()
