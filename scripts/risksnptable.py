import os
import vcffile
import risksnps

DEFAULT_DATA_DIR = '../data/'
DEFAULT_OUTPUT_FILE_NAME = DEFAULT_DATA_DIR + 'risksnptable.csv'
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

    def __init__(self, inputDirectoryName = DEFAULT_VCFS_DIR, outputFileName=DEFAULT_OUTPUT_FILE_NAME):
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
            destFile.write(headerLine + "\n")

            #loop through the files in the directory and add a column for each
            srcFileNames = os.listdir(self.inputDir)
            for srcFileName in srcFileNames:
                lineOut = self.get_one_person_from_file(self.inputDir + srcFileName)
                destFile.write(lineOut)

    def get_one_person_from_file(self, srcFileName):
        '''
        Returns a comma separated string that's one row for the table:
        one person's risk alleles.
        '''
        print srcFileName
        srcData = vcffile.VcfFile(srcFileName)
        personId = srcData.get_person_id()
        riskAlleles = srcData.get_these_snps(self.riskSnps)
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
            lineOut = '#N/A' + ',#N/A'*snpsCount + '\n'
            destFile.write(lineOut)

            lineOut = '1' + ',1'*snpsCount + '\n'
            destFile.write(lineOut)

            lineOut = '2' + ',2'*snpsCount + '\n'
            destFile.write(lineOut)

            lineOut = '3' + ',3'*snpsCount + '\n'
            destFile.write(lineOut)

            lineOut = '4' + ',4'*snpsCount + '\n'
            destFile.write(lineOut)
                          
    
if __name__ == '__main__':
    destObj = RiskSnpTable()
    destObj.add_all()
    destObj.add_normalization_data()
    
        
        
        
