import sys
import gzip

# sys.argv[1] = CCLE data
# sys.argv[2] = output file with the averages - .tsv

with gzip.open(sys.argv[1], 'r') as inFile:

    cell_indexes = []  # Holds the indexes of the cell lines we want from the CCLE data
    # my_cells = the cell lines we want
    my_cells = ["U-2_OS", "MDA-MB-175-VII", "MDA-MB-361", "SW480", "A549", "SW_1990", "AGS", "HL-60", "NCI-H1299",
                "KATO-III", "PC-3", "AU565", "SK-BR-3", "LS123", "HCC70", "COLO-320", "KASUMI-1", "CA46", "NAMALWA",
                "DB", "MIA-PaCa-2", "MDA-MB-468", "HCC38", "NCI-H1048","NCI-H1975", "PANC-1", "DU_145"]

    cell_lines = inFile.readline().decode().strip('\n').split('\t')
    for name in cell_lines:
        for my_name in my_cells:
            if my_name in name:
                cell_indexes.append(cell_lines.index(name))

    print("my_cells size is {0}".format(len(my_cells)))
    print("cell_indexes size is {0}".format(len(cell_indexes)))

    # ------------------------------------------------------------------------------------------------------------------
    outFile = open(sys.argv[2], 'w')
    outFile.write("Gene\tTranscript\tType\tAverage\n")  # Column headers for the output file

    for line in inFile:
        line = line.decode().strip('\n').split('\t')

        data = line[0].split('|')  # The first column has a bunch of data separated by '|'
        if data[5] == "HPRT1" or data[5] == "TK1":
            outFile.write("{0}\t{1}\t{2}\t".format(data[5], data[4], data[7]))

            sum = 0.0
            average = 0.0
            for index in cell_indexes:
                sum += float(line[index])
            average = sum / len(cell_indexes)

            outFile.write("{0}\n".format(round(average, 4)))

    outFile.close()
    # ------------------------------------------------------------------------------------------------------------------



