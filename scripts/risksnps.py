import csv

DEFAULTDATADIR = '../data/'
DEFAULTFILENAME = DEFAULTDATADIR + 'oddsratio.csv'
FIELD_SNP_ID = 'dbSNP ID'
FIELD_ODDS_RATIO = 'OddsRatio'
FIELD_ALLELE = 'Risk Allele'

class RiskSnps():
    '''
    RiskSnps is a collection of SNPs that have alleles that are associated
    with a higher risk of disease.

    The current implementation stores a list of snps and a list of corresponding
    risk alleles.  We read from a comma separated file where the snpId is in
    the first column and the risk allele is in the forth column.

    The sort order of the file is maintained. In the sample file used here,
    oddsRatio.csv I have the snps sorted in order of oddsRatio, low to high.
    '''


    def __init__(self):
        self.snps = []
        self.alleles = []        
    
    def read_from_file(self, sourceFileName = DEFAULTFILENAME):
        '''
        Reads the snps from the file, maintaining the sort order in the file.
        '''
        self.snps = []
        self.alleles = []
        self.oddsratio = []
        #count the number of records we read
        countOfRecordsRead = 0
        with open(sourceFileName, 'r') as srcfile:
            reader = csv.DictReader(srcfile)
            
            for row in reader:
                self.snps.append(row[FIELD_SNP_ID])
                self.alleles.append(row[FIELD_ALLELE])
                self.oddsratio.append(row[FIELD_ODDS_RATIO])
                countOfRecordsRead += 1
            
        print "read " + str(countOfRecordsRead) + " records from " + sourceFileName

    def len(self):
        '''The count of snps in the collection.'''
        return len(self.snps)
    
    def set_snps(self,snps):
        '''Puts this list of snps into the collection.'''
        self.snps = snps

    def set_alleles(self, alleles):
        '''Puts this list of alleles into the collection.'''
        self.alleles = alleles

    def get_snp(self,index):
        '''Return the snp id at this index.'''
        return self.snps[index]

    def get_allele(self, index):
        '''Return the allele at this index.'''
        return self.alleles[index]

if __name__ == '__main__':

    destObj = RiskSnps()
    destObj.read_from_file()
    
    
