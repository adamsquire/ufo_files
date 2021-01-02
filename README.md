# UFO Files PDF Processing

A set of notebooks and scripts that process [UK UFO sightings report listings PDF files](https://www.gov.uk/government/publications/ufo-reports-in-the-uk) to csv files. The project does not hold a copy of the PDF files or their extracted content, just the mechanisms to generate the content (see running steps below).

## Requirements

It is assumed that Jupyter is installed along with Pandas and Numpy. In order to run the notebooks, the relevant PDF processing library will be required. 

For [PDFPlumber](https://github.com/jsvine/pdfplumber).

```
pip install pdfplumber
```

and for [Camelot](https://camelot-py.readthedocs.io/en/master/)

```
pip install camelot[all]
```

for data evaluation 

```
pip install csvs-to-sqlite
```

## Project Structure

The project is structured as follows:

```
/
--/csvs       
  --/pdfplumber_csvs -- holds csvs that are generated during processing
  --/camelot_csvs   -- holds csvs that are generated during processing
--/notebooks  -- holds notebooks
--/outputs    
  --/csv      -- holds output csvs
  --/sqldb    -- holds output sql dbs
--/scripts    -- holds scripts
--/srchtml    -- holds source html
--/srcpdfs    -- holds source pdfs
--/urls       -- holds urls
```

## Running steps

It is assumed that there is a single run performed of each step including only 1 of the "Using..." notebooks. No effort has been made to clear the existing files prior to running. The directories csvs, outputs/csvs, output/sqldb, srchtml, srdpdf and urls are all expected to be empty at the start of this process

| Step | Action               | What does this do                                            |
| ---- | -------------------- | ------------------------------------------------------------ |
| 1    | scripts/get_urls.sh  | This pulls a copy of the web page https://www.gov.uk/government/publications/ufo-reports-in-the-uk to the folder ./srchtml and extracts the urls to the pdf files to ursl/urls.txt |
| 2    | scripts/get_files.sh | This runs wget for each line in urls.txt to download the pdf file to ./srcpdfs |
| 3    | notebooks/*          | Pick a notebook to run from the list below to generate a csv file to ./output/csv/ |

## Notebooks

| Notebook                                            | Purpose                                                     |
| --------------------------------------------------- | ----------------------------------------------------------- |
| Using PDFPlumber to process PDFs.ipyn               | PDFPlumber processing                                       |
| Using Camelot to process PDFs.ipyn                  | Camelot Processing with CLI                                 |
| Using Camelot to process PDFs non cli.ipyn          | Camelot Processing without CLI                              |
| PDFPlumber handling tables with no bottom rows.ipyn | Example of handling missing lines in tables with PDFPlumber |
| Generating a Word Cloud                             | Example of generating a word cloud (used in the blogpost)   |

## Scripts

| Script                     | Purpose                                                      |
| -------------------------- | ------------------------------------------------------------ |
| script/get_urls.sh         | Extract PDF urls from the source web page                    |
| script/get_files.sh        | For each line in ./urls/urls.txt down the file from that url using wget |
| script/check_file_sizes.sh | Outputs the line count from files in ./csvs/pdfplumber and ./output/csv/ufo_all_data.csv |
| script/make_db.sh          | Generate a sqlitedb from the csvs files in ./output/csv/     |

## Data Structure and Record Counts

The following data is the output data structure:

| Field                       | Type    | Notes                                                   |
| --------------------------- | ------- | ------------------------------------------------------- |
| Date                        | TEXT    | Generally in format DD-MMM-YY where populated correctly |
| Time                        | TEXT    | Generally HH:MM where populated correctly               |
| Town / Village              | TEXT    |                                                         |
| Area                        | TEXT    |                                                         |
| Occupation (Where Relevant) | TEXT    | Sparsely populated                                      |
| Description                 | TEXT    |                                                         |
| Page                        | INTEGER | From processing, page number 1 - n of the PDF File      |
| File                        | TEXT    | File name of the source PDF                             |
| ReportYear                  | INTEGER | Year from the File name                                 |

The following are the expected record counts in the resulting individual files and combined output file

```
Lines (inc. header)		File
432 					ufo_report_1997.csv
246 					UFOReport1998.csv
246  					UFOReport1999.csv
195  					UFOReport2000.csv
201  					UFOReport2001.csv
105  					UFOReports2002WholeoftheUK.csv
97  					UFOReports2003WholeoftheUK.csv
92  					UFOReports2004WholeoftheUK.csv
159  					UFOReports2005WholeoftheUK.csv
98  					UFOReports2006WholeoftheUK.csv
136  					ufo_report_2007.csv
286  					ufo_report_2008.csv
644  					ufo_report_2009.csv

Output csv line count inc. header
2925  				ufo_all_data.csv
```

## Known limitations

- No attempt is made to handle errors through an appropriate mechanism within any of the scripts or notebook actions. 
- The scripts and notebooks write files to the folder structure noted above without any attempt to check for pre-existence therefore they will overwrite existing files without warning.

## Licence

This work is released under the MIT Licence, a copy of the licence is included in this repository.