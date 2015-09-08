# codevturesultanalysis
VTU Result analysis using Python Web Scraping, Pentaho ETL and Weka data mining workbench
The  prototypes are done for VTU 2015 Sept results for B tech 4th Semester, 6th and 8th Semester and M tech 2nd Semester 
The ktr files are the Pentaho spoon ETL files ( used to get data from Mongo DB and transform to .arff file for weka)
The InsertDocument*.py files are the python code to extract the data from (HTML) result file set and put them into Mongo collections
The Scrape*.py are the files for web scraping from VTU result website 
Due to HTML result files (which are MS FrontPage generated) variations from semester to sremester, one needs to test the code with the scraped data set and change accordingly. For any change in format of result HTMLs, the programs will break and need to be modified. 


