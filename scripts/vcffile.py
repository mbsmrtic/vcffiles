import risksnps

class VcfFile():
    '''Variant Call Format files.

    Each variant call format (vcf) file represents genetic information for
    one person. Snps that are different from the reference genome are listed
    along with the reference allele and the alternative allele found for this
    person.

    Here we provide methods to pull the snps from the file to support the
    creation of file formats that contain more than one person for visualization
    and analysis of the genomic data provided.  
    '''


    def __init__(self,filename = ""):
        self.filename = filename
    
    def get_first_snp_line(self):
        '''
        Reads the file until it encounters a line with a snp id (rsxxx) and
        returns the line containing the snp or blank if none are found.
        '''
        with open(self.filename, 'r') as snp_file:
            #using with so that the file doesn't get left open it's automatically closed when
            #we leave this code block
            for a_line in snp_file:
                snpId = self.get_a_snp_id(a_line)
                if (snpId):
                    return(a_line)
        return("")

    def get_these_risksnps(self, riskSnps):
        '''
        Reads the file looking for the snps in the riskSnps argument.
        Returns a list of the allele numbers for the snps that were found.
        '''
        alleles = ['0']*(riskSnps.len())
        with open(self.filename, 'r') as snp_file:
            for a_line in snp_file:
                snpId = self.get_a_snp_id(a_line)
                if (snpId in riskSnps.snps):
                    index = riskSnps.snps.index(snpId)
                    riskAllele = riskSnps.alleles[index]
                    sourceAllele = self.get_an_allele(a_line)
                    alleleNumber = self.get_an_allele_number(sourceAllele, riskAllele)
                    alleles[index] = alleleNumber
        return alleles

    def get_these_snps(self, snpsToUse):
        '''
        Reads the file looking for the snps in the snpsToUse argument.
        Returns a list of the alleles for the snps that were found.
        '''
        alleles = ['0']*(len(snpsToUse))
        with open(self.filename, 'r') as snp_file:
            for a_line in snp_file:
                snpId = self.get_a_snp_id(a_line)
                if (snpId in snpsToUse):
                    index = snpsToUse.index(snpId)
                    sourceAllele = self.get_an_allele(a_line)
                    alleles[index] = sourceAllele
        return alleles

    def get_all_snps_and_alleles(self):
        '''
        Reads the file and returns a list containing all the snp, allele combinations.
        '''
        alldata = []
        index = 0
        with open(self.filename, 'r') as snp_file:
            for a_line in snp_file:
                snpId = self.get_a_snp_id(a_line)
                if (len(snpId) > 0):
                    sourceAllele = self.get_an_allele(a_line)
                    alldata.append([snpId, sourceAllele])
                    index += 1
        return alldata
        
    def get_all_snps_and_locations(self):
        '''
        '''
        alldata = []
        index = 0
        with open(self.filename, 'r') as snp_file:
            for a_line in snp_file:
                snpId = self.get_a_snp_id(a_line)
                if (len(snpId) > 0):
                    chrom = self.get_a_chrom(a_line)
                    location = self.get_a_location(a_line)
                    sourceAllele = self.get_an_allele(a_line)
                    alldata.append([snpId, sourceAllele, chrom, location])
                    index += 1
        return alldata
        
    def get_a_snp_id(self, line):
        '''
        Looks for a snp id, a string starting with rs. If one is found, it's
        returned, otherwise an empty string.
        '''
        split = line.split();
        if (split.__len__() < 3):
            return('')
        snpname = split[2]
        if (snpname.find('rs') == 0):
            return snpname
        else:
            return('')

    def get_an_allele_number(self, allele, riskAllele):
        '''
        Returns a number that represents the allele.

        We convert it to a number so that the risk alleles are given the
        highest value (4), nas are still nas and everything else falls between those two.
        This emphasizes risk alleles in the visualization.  
        '''
        alleleNumber = '0'
        riskAlleleDictionary = {'C': {'C':'4', 'G':'3', 'T':'2', 'A':'1'},
                                'A': {'A':'4', 'G':'3', 'T':'2', 'C':'1'},
                                'T': {'T':'4', 'G':'3', 'C':'2', 'A':'1'},
                                'G': {'G':'4', 'T':'3', 'C':'2', 'A':'1'}}
        personId = self.get_person_id()
        if (riskAllele in riskAlleleDictionary):
            alleleDictionary = riskAlleleDictionary[riskAllele]
            if (allele in alleleDictionary):
                alleleNumber = alleleDictionary[allele]
        return alleleNumber
        
        
    def get_an_allele(self, line):
        '''
        Returns the allele from this line.  
        '''
        split = line.split()
        if (split.__len__() < 5):
            return('')
        allele = split[4]
        return allele;

    def get_a_chrom(self,line):
        '''
        Returns the chromosome from this line.
        '''
        split = line.split()
        chrom = split[0]
        if chrom.find('chr') == 0:
            return chrom
        else:
            return ''
        
    def get_a_location(self,line):
        split = line.split()
        location = split[1]
        return location

    def get_persons_file_name(self, personId):
        '''
        Returns the name of the file that contains this person's data.
        '''
        filename = personId + '_hg19.gatk.flt.vcf'
        return filename
        
    def get_person_id(self):
        '''
        Returns the person id from the filename.
        '''
        parts = self.filename.split('/')
        filename = parts[-1]   #the last one
        parts = filename.split('_')
        personId = parts[0]
        return personId

