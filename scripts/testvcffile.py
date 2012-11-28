import unittest
import vcffile
import os
import risksnps

TESTDATADIR = '../data/'        
SAMPLEFILENAME = TESTDATADIR + 'A0024_hg19.gatk.flt.vcf'

class TestVcfFile(unittest.TestCase):
    '''
    Tests for the VcfFile class.
    '''

    def test_person_id(self):
        '''VcfFile.get_person_id should pull the person id from the file name'''
        self.assertTrue(os.path.exists(SAMPLEFILENAME))
        inputfile = vcffile.VcfFile(SAMPLEFILENAME)
        personid = inputfile.get_person_id()
        self.assertEqual("A0024", personid)

    def test_get_first_snp_line(self):
        '''VcfFile.get_first_snp_line should return the first snp in the file'''
        self.assertTrue(os.path.exists(SAMPLEFILENAME))
        inputfile = vcffile.VcfFile(SAMPLEFILENAME)
        firstSnpLine = inputfile.get_first_snp_line()
        firstSnp = inputfile.get_a_snp_id(firstSnpLine)
        self.assertEqual('rs12028261', firstSnp)

    def test_get_an_allele(self):
        '''VcfFile.get_an_allele should return the snps allele'''
        self.assertTrue(os.path.exists(SAMPLEFILENAME))
        inputfile = vcffile.VcfFile(SAMPLEFILENAME)
        firstSnpLine = inputfile.get_first_snp_line()
        firstSnpAllele = inputfile.get_an_allele(firstSnpLine)
        self.assertEqual('A', firstSnpAllele)
        
    def test_get_an_allele_number(self):
        '''get_an_allele_number should convert from a character allele to a number'''
        inputfile = vcffile.VcfFile()
        alleleNumber = inputfile.get_an_allele_number('A', 'G')
        self.assertEqual('1', alleleNumber)
        alleleNumber = inputfile.get_an_allele_number('G', 'G')
        self.assertEqual('4', alleleNumber)

    def test_get_these_snps(self):
        '''
        VcfFile.get_these_snps should return a list of allele numbers.
        Note that they will usually be 4s because 4 represents the risk
        allele and in this dataset, if a person has an allele that is different
        from the reference genome, and it is for one of the risk snps,
        it is usually, but not always the risk allele. 
        '''
        riskSnps = risksnps.RiskSnps()
        riskSnps.set_snps(['rs102275', 'rs3764147', 'rs7927997', 'rs415890', 'rs4077515', 'rs3810936', 'rs2476601', 'rs3792109'])
        riskSnps.set_alleles(['C','G','T','C','T','C','G','A'])
        inputfile = vcffile.VcfFile(SAMPLEFILENAME)
        alleleNumbers = inputfile.get_these_snps(riskSnps)
        self.assertEqual(riskSnps.len(), len(alleleNumbers))
        self.assertEqual('4', alleleNumbers[0])
        self.assertEqual('4', alleleNumbers[1])

def main():
    unittest.main()

if __name__ =='__main__':
    main()
    
