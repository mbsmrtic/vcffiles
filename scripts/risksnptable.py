import os
import vcffile
import risksnps
from csv import DictWriter
from csv import DictReader

DEFAULT_DATA_DIR = '../data/'
DEFAULT_SNPTABLE_FILE_NAME = DEFAULT_DATA_DIR + 'risksnptable.csv'
DEFAULT_OUTPUT_DIFFS_NAME = DEFAULT_DATA_DIR + 'risksnpdiffs.csv'
DEFAULT_OUTPUT_DIFFS_TALL_NAME = DEFAULT_DATA_DIR + 'risksnpdiffstall.csv'
DEFAULT_VCFS_DIR = DEFAULT_DATA_DIR + 'vcfdata/'
FIELD_PERSONID = 'PersonId'
FIELD_SNPIDA = 'snpIdA'
FIELD_SNPIDB = 'snpIdB'
FIELD_SNPID = 'snpId'
FIELD_SAMEALLELECOUNT = 'sameAlleleCount'

class RiskSnpTable():
    '''
    RiskSnpTable is the table we'll create from then vcf files. It contains
    one row per person and one column per risk snp. 

    A risk snp is a Single Nucleotide Polymorphism (snp) that has an allele
    with a significant association with the disease.

    The data for each person is stored in a vcf file, so we loop through the
    directory adding a row at a time.
    
    '''

    def __init__(self, inputDirectoryName = DEFAULT_VCFS_DIR, outputFileName=DEFAULT_SNPTABLE_FILE_NAME):
        self.filename = outputFileName
        self.riskSnps = risksnps.RiskSnps()
        self.inputDir = inputDirectoryName

    def add_all(self):
        '''
        Loops through all the files in inputDir directory, adding one row per file/person,
        one column per risk snp.
        '''

        #open the destination file and write the header line
        headerFields = self.get_file_header()
        with open(self.filename, 'w') as destFile:
            print "created " + self.filename + "\n"
            writer = DictWriter(destFile, headerFields, lineterminator='\n')
            writer.writeheader()

            #loop through the files in the directory and add a column for each
            srcFileNames = os.listdir(self.inputDir)
            fileCount = 0
            for srcFileName in srcFileNames:
                rowOut = self.get_one_person_from_file(self.inputDir + srcFileName)
                writer.writerow(rowOut)
                fileCount += 1
            if (fileCount == 1):
                print ("You ran this on one snp file. For the entire dataset go to " +
                        "https://genomeinterpretation.org/content/crohns-disease-2012 \n")
            else:
                print ("Wrote " + str(fileCount) + " rows to " + self.filename)

    def get_one_person_from_file(self, srcFileName):
        '''
        Returns a comma separated string that's one row for the table:
        one person's risk alleles.
        '''
        print srcFileName
        srcData = vcffile.VcfFile(srcFileName)
        personId = srcData.get_person_id()
        rowOut = {FIELD_PERSONID:personId}
        riskAlleles = srcData.get_these_risksnps(self.riskSnps)
        riskSnpIndex = 0
        for allele in riskAlleles:
            riskSnp = self.riskSnps.snps[riskSnpIndex]
            rowOut[riskSnp] = allele
            riskSnpIndex += 1
        return rowOut

    def get_risk_snps(self):
        self.riskSnps.read_from_file()
        
    def get_file_header(self):
        '''
        Gets the risk snps from a RiskSnps object and creates a header line
        labeling each column with the risk snp's snpId.
        '''

        #get the risk snps and collect the header fields
        if (self.riskSnps.len() == 0):
            self.get_risk_snps()
        headerFields = [FIELD_PERSONID]
        for snpId in self.riskSnps.snps:
            headerFields.append(snpId)
        return headerFields

    def add_normalization_data(self):
        '''
        For normalizing, we add lines for the different possible values
        '''
        headerLine = self.get_file_header()
        columnCount = len(headerLine.split(','))
        snpsCount = columnCount - 1
        with open(self.filename, 'a') as destFile:
            lineOut = '0' + ',0'*snpsCount + '\n'
            destFile.write(lineOut)

            lineOut = '1' + ',1'*snpsCount + '\n'
            destFile.write(lineOut)

            lineOut = '2' + ',2'*snpsCount + '\n'
            destFile.write(lineOut)

            lineOut = '3' + ',3'*snpsCount + '\n'
            destFile.write(lineOut)

            lineOut = '4' + ',4'*snpsCount + '\n'
            destFile.write(lineOut)

class RiskSnpCompare():
    '''
    RiskSnpCompare compares the risk snps to each other. The output file contains
    the number of times the snps alleles are the same.  
    
    We create two formats, one that is a wide table where each row is snp and each
    column is a snp, and another where each row has three values snpId, snpId, samecount.
    '''

    def __init__(self, inputFileName = DEFAULT_SNPTABLE_FILE_NAME, 
                 outputDiffsName=DEFAULT_OUTPUT_DIFFS_NAME, outputTallName=DEFAULT_OUTPUT_DIFFS_TALL_NAME):
        self.diffsFileName = outputDiffsName
        self.diffsTallName = outputTallName
        self.riskSnps = risksnps.RiskSnps()
        self.inputFileName = inputFileName

    def write_tall_and_wide_compares(self):
        '''
        RiskSnpTable contains one row per person and one column per risk snp. Here we 
        loop through the table and compare each snp to each other snp.  The measure
        we use to compare is the count of alleles that are the 
        '''
        
        sameCounts = self.getSameCounts()
        self.writeDiffsTallTable(sameCounts)
        self.writeDiffsWideTable(sameCounts)
        
    def writeDiffsTallTable(self, sameCounts):                
        #open the destination tall file and write the header line
        headerFields = [FIELD_SNPIDA, FIELD_SNPIDB, FIELD_SAMEALLELECOUNT]
        with open(self.diffsTallName, 'w') as destTallFile:
            writer = DictWriter(destTallFile, headerFields, lineterminator='\n')
            print 'created ' + self.diffsTallName + '    '
            writer.writeheader()
            #loop through the counts and write them out
            recordsWritten = 0
            row = {}
            for key in sameCounts:
                counts = sameCounts[key]
                for k in counts:
                    count = sameCounts[key][k]
                    if (key.startswith('rs') and k.startswith('rs') and count > 0):
                        row[FIELD_SNPIDA] = key
                        row[FIELD_SNPIDB] = k
                        row[FIELD_SAMEALLELECOUNT] = count
                        writer.writerow(row)
                        recordsWritten += 1
            print 'wrote ' + str(recordsWritten) + ' records \n'

    def writeDiffsWideTable(self, sameCounts):
        #collect all the column snps
        headerFields = [FIELD_SNPID]
        for snpIdA in sameCounts:
            for snpIdB in sameCounts[snpIdA]:
                if snpIdB not in headerFields:
                    headerFields.append(snpIdB)

        with open(self.diffsFileName, 'w') as destFile:
            print 'create ' + self.diffsFileName + '    '
            writer = DictWriter(destFile, headerFields, lineterminator='\n')
            writer.writeheader()
            #loop through counts and write them out
            recordsWritten = 0
            for snpIdA in sameCounts:
                rowOut = {FIELD_SNPID:snpIdA}
                snpIdBs = sameCounts[snpIdA]
                for snpIdB in snpIdBs:
                    count = snpIdBs[snpIdB]
                    assert snpIdA.startswith('rs')
                    assert snpIdB.startswith('rs')
                    rowOut[snpIdB] = count
                writer.writerow(rowOut)
                recordsWritten += 1
        print 'wrote ' + str(recordsWritten) + ' records \n'
            
        
    def getSameCounts(self):
        '''
        Gets a two dimensional array of counts. The counts are the number of rows in 
        which both snps have the risk allele. 
        '''
        with open(self.inputFileName, 'r') as srcFile:
            reader = DictReader(srcFile)
            colHeaders = reader.fieldnames
            #remove the first col header, the person Id column header to get the snpIds
            snpIds = colHeaders[1:]
            
            #initialize our dictionary of same counts
            sameCounts = {}
            for snpIdA in snpIds:
                bDict = {} 
                for snpIdB in snpIds:
                    bDict[snpIdB] = 0
                sameCounts[snpIdA] = bDict

            #loop through the rows incrementing our counts 
            for row in reader:
                #read and remove the personId so that we can loop over all the snps
                personId = row[FIELD_PERSONID]
                del(row[FIELD_PERSONID])
                #don't count the normalization lines
                if (len(personId) > 2):
                    for snpIdA in row:
                        alleleA = row[snpIdA]
                        for snpIdB in row:
                            alleleB = row[snpIdB]
                            if (alleleA == '4' and alleleB == '4'):
                                sameCounts[snpIdA][snpIdB] += 1

            return sameCounts

                
if __name__ == '__main__':
    #destObj = RiskSnpTable()
    #destObj.add_all()
    #destObj.add_normalization_data()
    destObj = RiskSnpCompare()
    destObj.write_tall_and_wide_compares()
    
        
        
        
