DEFAULTDATADIR = '../data/'
DEFAULTFILENAME = DEFAULTDATADIR + 'oddsratio.csv'

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
        with open(sourceFileName) as srcfile:
            #the first line is the header line
            firstLine = True
            for a_line in srcfile:
                if (firstLine):
                    firstLine = False
                else:
                    #remove newline character
                    if (a_line[-1] == "\n"):
                        a_line = a_line[0:-1]
                    fields = a_line.split(',')
                    self.snps.append(fields[0])
                    self.alleles.append(fields[3])

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
    
    
