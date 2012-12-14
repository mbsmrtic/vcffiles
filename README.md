VcfFiles
========

The VcfFiles repository contains my first Python scripts.  My goal for this project 
is to use it to learn Python. I chose to learn Python by getting a dataset and writing scripts 
that manipulate it into file formats that are easily visualized.  

I chose the Crohn's disease genomic dataset from the Critical Assessment of Genome Interpretation (CAGI)
website.  

Critical Assessment of Genome Interpretation website: https://genomeinterpretation.org/ 

Crohn's disease dataset: https://genomeinterpretation.org/content/crohns-disease-2012 
If you want to run the python scripts on this dataset, register at the above link
and download the data into a folder called vcfdata under the existing vcffiles/data directory. 

The format of the Crohn's disease dataset is Variant Call Format (vcf) files. A Variant Call Format file
is a standard format for storing gene sequence variations. It only stores the single nucleotide polymorphisms (SNP)
that have alleles (A,C,G or T) that are different from a reference genome. 

The SNPs that have been identified as having alleles with significant association with Crohn's disease
are from Franke, A., & et.al. (2010, December). Genome-wide meta-analysis increases to 71 the number of 
confirmed Crohn's disease susceptibility loci. Nature Genetics, 42(12), 1118-25.
http://www.ncbi.nlm.nih.gov/pubmed/21102463 

Input file formats
---------------------

	* VcfFile 
			Variant Call Format is a file format for storing genetic data. It stores the differences from a
			reference genome.  Our input data from the CAGI website is stored in this format. The class
			VcfFile pulls the relevant snp alleles from the file to put into the desired output format.
			There is one sample file included in this repository under data/vcffiles. The remaining files
			can be downloaded from the CAGI website above.  
	* RiskSnps
			I've included a table from the above paper that has a list of snps alleles with a significant 
			association with Crohn's disease.  This file is included here in data/risksnps.csv
                                                
Current output file formats
---------------------------------

	* TallTable
			This class encapsulates a file format with at least these columns: personId, snpId, allele
	* TallSomePpl
			A tall table that can be filled with specific people. This is needed because when we include
			all the people, the file is too large to pull into Tableau.
	* SnpsInCommon
			This class creates a difference matrix. Each row of the table is a person and each column is 
			a person. Each cell contains the count of snps for which the two people have different alleles.
	* RiskSnpTallTable
			This class encapsulates a file format with 3 columns: personId, snpId, and alleleNumber.
			I use this table format to create a heatmap visualization where each dot is one of five
			colors depending on whether the allele is missing (the same as the reference genome),
			A, C, G, or T. We want the highest contrast color to be the risk allele, so VcfFile converts 
			the letters to numbers where 4 is the risk allele.  
	* RiskSnpTable
			This class encapsulates a file format where there is one row per person and one column
			per risk SNP. The output table is data/risksnptable.csv.  I use this table to create 
			a parallel coordinates visualization where each line is a person and each axis is 
			a risk SNP. 
	* SomeSnpsTable
			This class encapsulates a file format with one row per snp and one column per person.  
			Each cell contains the allele.  We'll use this to create a parallel coordinates view of 
			the snps.
                                                
