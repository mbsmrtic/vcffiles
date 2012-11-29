import os
import vcffile
import risksnps

DEFAULT_DATA_DIR = '../data/'
DEFAULT_OUTPUT_FILE_NAME = DEFAULT_DATA_DIR + 'risksnptalltable.csv'
DEFAULT_VCFS_DIR = DEFAULT_DATA_DIR + 'vcfdata/'

class RiskSnpTallTable():
    '''
    RiskSnpTallTable is a table we'll create from the vcf files. It contains
    column of personids, one column of risksnpids and one column of allele values.

    A risk snp is a Single Nucleotide Polymorphism (snp) that has an allele
    with a significant association with the disease.

    The data for each person is stored in a vcf file, so we loop through the
    directory adding a person at a time.
    
    '''
    #todo Decide on a consistent naming convention for variables: camel caps or underscores?

    def __init__(self, inputDirectoryName = DEFAULT_VCFS_DIR, outputFileName=DEFAULT_OUTPUT_FILE_NAME):
        self.filename = outputFileName
        self.riskSnps = risksnps.RiskSnps()
        self.inputDir = inputDirectoryName

    def add_all(self):
        '''
        Loops through all the files in inputDir directory, adding a column of personIds,
        a column of risk snpIds and a column of alleles
        '''
        self.riskSnps.read_from_file()
        
        #open the destination file and write the header line
        with open(self.filename, 'w') as destFile:
            print "created " + self.filename + "\n"
            headerLine = "personid, snpid, allele"
            destFile.write(headerLine + "\n")

            #loop through the files in the directory and add a column for each
            srcFileNames = os.listdir(self.inputDir)
            fileCount = 0
            for srcFileName in srcFileNames:
                self.write_one_person_to_file(self.inputDir + srcFileName, destFile)
                fileCount += 1
            if (fileCount == 1):
                print ("You ran this on one snp file, for the entire dataset go to " +
                        "https://genomeinterpretation.org/content/crohns-disease-2012 \n")

    def write_one_person_to_file(self, srcFileName, destFile):
        '''
        Gets the alleles for the risk snps from srcFile
        '''
        print srcFileName
        srcData = vcffile.VcfFile(srcFileName)
        personId = srcData.get_person_id()
        riskAlleles = srcData.get_these_snps(self.riskSnps)
        index = 0
        for allele in riskAlleles:
            if (allele != '0'):
                lineOut = personId + ',' + self.riskSnps.snps[index] + ',' + allele + '\n'
                destFile.write(lineOut)
            index += 1

if __name__ == '__main__':
    destObj = RiskSnpTallTable()
    destObj.add_all()
    
        
        
        
