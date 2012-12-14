import os
import vcffile
import risksnps

DEFAULT_DATA_DIR = '../data/'
DEFAULT_SNPTABLE_FILE_NAME = DEFAULT_DATA_DIR + 'risksnptable.csv'
DEFAULT_OUTPUT_DIFFS_NAME = DEFAULT_DATA_DIR + 'risksnpdiffs.csv'
DEFAULT_OUTPUT_DIFFS_TALL_NAME = DEFAULT_DATA_DIR + 'risksnpdiffstall.csv'
DEFAULT_VCFS_DIR = DEFAULT_DATA_DIR + 'vcfdata/'

class RiskSnpTable():
    '''
    RiskSnpTable is the table we'll create from then vcf files. It contains
    one row per person and one column per risk snp. 

    A risk snp is a Single Nucleotide Polymorphism (snp) that has an allele
    with a significant association with the disease.

    The data for each person is stored in a vcf file, so we loop through the
    directory adding a row at a time.
    
    '''
    #todo Decide on a consistent naming convention for variables: camel caps or underscores?

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
        headerLine = self.get_file_header()
        with open(self.filename, 'w') as destFile:
            print "created " + self.filename + "\n"
            destFile.write(headerLine + "\n")

            #loop through the files in the directory and add a column for each
            srcFileNames = os.listdir(self.inputDir)
            fileCount = 0
            for srcFileName in srcFileNames:
                lineOut = self.get_one_person_from_file(self.inputDir + srcFileName)
                destFile.write(lineOut)
                fileCount += 1
            if (fileCount == 1):
                print ("You ran this on one snp file. For the entire dataset go to " +
                        "https://genomeinterpretation.org/content/crohns-disease-2012 \n")

    def get_one_person_from_file(self, srcFileName):
        '''
        Returns a comma separated string that's one row for the table:
        one person's risk alleles.
        '''
        print srcFileName
        srcData = vcffile.VcfFile(srcFileName)
        personId = srcData.get_person_id()
        riskAlleles = srcData.get_these_risksnps(self.riskSnps)
        lineOut = personId + ',' + ','.join(riskAlleles) + '\n'
        return lineOut

    def get_risk_snps(self):
        self.riskSnps.read_from_file()
        
    def get_file_header(self):
        '''
        Gets the risk snps from a RiskSnps object and creates a header line
        labeling each column with the risk snp's snpId.
        '''

        #get the risk snps and write out the header line
        if (self.riskSnps.len() == 0):
            self.get_risk_snps()
        headerLine = "PersonId"
        for snpId in self.riskSnps.snps:
            headerLine += ", "
            headerLine += snpId
        return headerLine

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

    def go(self):
        '''
        
        '''
        
        sameCounts = self.getSameCounts()
        self.writeDiffsTallTable(sameCounts)
        self.writeDiffsWideTable(sameCounts)
        
    def writeDiffsTallTable(self, sameCounts):                
        #open the destination tall file and write the header line
        headerLine = 'snpIdA,snpIdB,sameAlleleCount\n'
        with open(self.diffsTallName, 'w') as destTallFile:
            print 'created ' + self.diffsTallName + '    '
            destTallFile.write(headerLine)
            #loop through the counts and write them out
            recordsWritten = 0
            for key in sameCounts:
                counts = sameCounts[key]
                for k in counts:
                    count = sameCounts[key][k]
                    if (key.startswith('rs') and k.startswith('rs') and count > 0):
                        lineOut = key + ',' + k + ',' + str(count) + '\n'
                        destTallFile.write(lineOut)    
                        recordsWritten += 1
            print 'wrote ' + str(recordsWritten) + ' records \n'

        #write out the wide table
        #    lineOut = 'snpId,' + ','.join(snpIds) + '\n'
    def writeDiffsWideTable(self, sameCounts):
        #collect all the column snps
        columnSnps = []
        for snpIdA in sameCounts:
            for snpIdB in sameCounts[snpIdA]:
                if snpIdB not in columnSnps:
                    columnSnps.append(snpIdB)

        #write out the header line with the column snps
        headerLine = 'snpId'
        for snpId in columnSnps:
            headerLine += ',' + snpId
        headerLine += '\n'
        with open(self.diffsFileName, 'w') as destFile:
            print 'create ' + self.diffsFileName + '    '
            destFile.write(headerLine)
            #loop through counts and write them out
            recordsWritten = 0
            for snpIdA in sameCounts:
                lineOut = snpIdA
                snpIdBs = sameCounts[snpIdA]
                for snpIdB in snpIdBs:
                    count = snpIdBs[snpIdB]
                    assert snpIdA.startswith('rs')
                    assert snpIdB.startswith('rs')
                    lineOut += ',' + str(count)
                lineOut += '\n'
                destFile.write(lineOut)
                recordsWritten += 1
        print 'wrote ' + str(recordsWritten) + ' records \n'
            
        
    def getSameCounts(self):
        with open(self.inputFileName, 'r') as srcFile:
            lineIn = srcFile.readline()
            snpIds = lineIn.split(',')
            #remove the first column label
            snpIds = snpIds[1:]
            
            #strip whitespace from snpIds
            for i in range(len(snpIds)):
                snpIds[i] = snpIds[i].strip()
            
            #initialize our dictionary of same counts
            sameCounts = {}
            for snpIdA in snpIds:
                bDict = {} 
                for snpIdB in snpIds:
                    bDict[snpIdB] = 0
                sameCounts[snpIdA] = bDict
                
            #loop through the file, counting
            for lineIn in srcFile:
                alleles = lineIn.split(',')
                personId = alleles[0]
                #don't count the normalization lines
                if (len(personId) > 2):
                    #remove the first element in the line, it's the personId
                    alleles = alleles[1:]
                    aIndex = 0
                    for alleleA in alleles:
                        bIndex = 0
                        for alleleB in alleles:
                            #we're defining 'same' as 'they both have the risk allele
                            if (alleleA == '4' and alleleB == '4'):
                                snpA = snpIds[aIndex]
                                snpB = snpIds[bIndex]
                                sameCounts[snpA][snpB] = sameCounts[snpA][snpB] + 1
                            bIndex += 1
                        aIndex += 1
            
            return sameCounts

                
if __name__ == '__main__':
    #destObj = RiskSnpTable()
    #destObj.add_all()
    #destObj.add_normalization_data()
    destObj = RiskSnpCompare()
    destObj.go()
    
        
        
        
