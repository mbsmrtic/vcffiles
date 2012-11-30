import os
import vcffile
import risksnps

DEFAULT_DATA_DIR = '../data/'
DEFAULT_OUTPUT_FILE_NAME = DEFAULT_DATA_DIR + 'talltable.csv'
DEFAULT_VCFS_DIR = DEFAULT_DATA_DIR + 'vcfdata/'

class TallTable():
    '''
    TallTable is a table we'll create from the vcf files. It contains one
    column of personids, one column of risksnpids and one column of allele values.

    The data for each person is stored in a vcf file, so we loop through the vcf 
    directory adding a person at a time.
    
    '''
    
    def __init__(self, inputDirectoryName = DEFAULT_VCFS_DIR, outputFileName=DEFAULT_OUTPUT_FILE_NAME):
        self.filename = outputFileName
        self.inputDir = inputDirectoryName

    def add_all(self):
        '''
        Loops through all the files in inputDir directory, adding a column of personIds,
        a column of snpIds and a column of alleles
        '''
        
        os.remove(self.filename)
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
        Gets the alleles for the snps from srcFile and writes them to the output file
        '''

        srcData = vcffile.VcfFile(srcFileName)
        personId = srcData.get_person_id()
        snpsAndAlleles = srcData.get_all_snps_and_alleles()
        recordCount = 0
        for snpAndAllele in snpsAndAlleles:
            if (snpAndAllele[1] != '0'):
                lineOut = personId + ',' + snpAndAllele[0] + ',' + snpAndAllele[1] + '\n'
                destFile.write(lineOut)
            recordCount += 1
        print srcFileName + ' wrote ' + str(recordCount) + ' records to ' + self.filename

class RiskSnpTallTable(TallTable):
    '''
    RiskSnpTallTable is the same format as TallTable, but instead of including all the snps
    from all the vcf files, we include only the snps that in riskSnps.  This will result
    in a table with fewer rows.  

    A risk snp is a Single Nucleotide Polymorphism (snp) that has an allele
    with a significant association with the disease.


    '''

    def __init__(self, inputDirectoryName = DEFAULT_VCFS_DIR, outputFileName=DEFAULT_OUTPUT_FILE_NAME):
        TallTable.__init__(self, inputDirectoryName, outputFileName)
        self.riskSnps = risksnps.RiskSnps()


    def write_one_person_to_file(self, srcFileName, destFile):
        '''
        Gets the alleles for the risk snps from srcFile and writes them to the output file
        '''

        if (self.riskSnps.len() == 0):
            self.riskSnps.read_from_file()
        
        srcData = vcffile.VcfFile(srcFileName)
        personId = srcData.get_person_id()
        riskAlleles = srcData.get_these_snps(self.riskSnps)
        index = 0
        recordCount = 0;
        for allele in riskAlleles:
            if (allele != '0'):
                lineOut = personId + ',' + self.riskSnps.snps[index] + ',' + allele + '\n'
                destFile.write(lineOut)
                recordCount += 1
            index += 1
        print srcFileName + ' wrote ' + str(recordCount) + ' records to ' + self.filename

if __name__ == '__main__':
    destObj = TallTable()
    destObj.add_all()
    destObj = RiskSnpTallTable(outputFileName='../data/risksnptalltable.csv')
    destObj.add_all()
    
    
        
        
        
