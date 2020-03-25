# Ahsan Khan's Data Engineering Coding Challenge for Insight

The federal government provides a way for consumers to file complaints against companies regarding different financial products, such as payment problems with a credit card or debt collection tactics. This project is about identifying the number of complaints filed and how they’re spread across different companies.

We want to know for each financial product and year, the total number of complaints, number of companies receiving a complaint, and the highest percentage of complaints directed at a single company.

An input file, complaints.csv, will be moved to the top-most input directory of the repository. My code will read that input file, process it and write the results to an output file, report.csv which will be placed in the top-most output directory of the repository 

Note–
Only allowed to use the default data structures that come with that programming language (can use I/O libraries). For example, should not use Pandas or any other external libraries (i.e. Python modules that must be installed using ‘pip’). 


Instructions: 
1) Insert csv file to be processed in the input folder
2) cd to the directory this repo is placed in on your local environment
3) Enter ./run.sh in the commandline for python script to process the csv file
4) Processed csv file will be placed in the output folder


Things to note:
1) Needed to set encoding to uft-8 for the large file big data because there were non-ascii characters in the file
2) Used dict and lists as data structures for working without pandas
3) Used the "CSV" library
4) Testsuite did not accept f strings 
5) Code written in python 3.7


