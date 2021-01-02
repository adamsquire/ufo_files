import pandas as pd
import pdfplumber
import os
import sys
import numpy as np
import glob
import re

"""
Base path
"""
path = "/home/adam/downloads/ufo_files/"

"""
Output Headers
Each file contains the same columns but the headers are slightly different, 
conform here
"""
headers = ['Date','Time','Town / Village','Area','Occupation (Where Relevant)','Description','Page','File','ReportYear']

"""
Some of the PDF pages do not have a bottom line at the end of the table on the first page
PDFPlumber can't identify the end of the table so it takes the penultimate row as the final
row of the table, add the filename and position of the line at the bottom of the page
"""
line = {"UFOReports2006WholeoftheUK.pdf":521,"UFOReports2004WholeoftheUK.pdf":552.875}

"""
Some of the PDF documents repeat the header on each page. Add the document
title to this list to use the headers from the table on the first page and
drop the headers from the rest of the tables
"""
drop = ["ufo_report_2008.pdf",
	"UFOReport2000.pdf",
	"UFOReport1999.pdf",
	"UFOReport1998.pdf"]

"""Function make_df()

 Args:
        page_number (int): The page number being processed.
        table (list): List representing the table as prepared by PDFPlumber.
	dropheader (bool): used to denote files that have repeated headers

 Returns:
	df: pandas dataframe containing the table data. Page number is added, empty rows are removed, tabs and new line are removed
"""
def make_df(page_number,table,dropheader=False):
	df = pd.DataFrame(table)
	df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["",""], regex=True, inplace=True) # replace tab, new line
	df.replace("", np.nan, inplace=True) # convert empty strings to NaN for removal of full rows
	df.dropna(axis = 0, how = 'all', inplace = True) # remove empty rows
	df.loc[df[3].str.count(r'(^[a-z]+)') >0, 3] = df[2].str[-1] + df[3] # instances where the first character has been cut off (2 = Town / Village, 3 = Area
	df.loc[df[2].str.count(r'\w[A-Z]') >0, 2] = df[3].str[:-1] #instances where the last character is uppercase
	df['Page']=page_number+1
	if page_number == 0:
		df = df[1:] # remove header from first page data
	if page_number > 0 and dropheader:
		df = df[1:] # remove repeated header if present
	return  df

def process_pdf(file):
	with pdfplumber.open(os.path.join(path,"srcpdfs",file)) as pdf:
		data = []
		year = re.findall('\d+',file)[0]
		for page_number,page in enumerate(pdf.pages):
			settings = {}
			dropheaders = False
			if file in line and page_number == 0:
				settings["explicit_horizontal_lines"] = [line[file]]
			if file in drop:
				dropheaders = True
			table=page.extract_table(table_settings=settings)
			filedata = make_df(page_number,table,dropheaders)
			data.append(filedata)
		csv_file = os.path.join(path,"csvs",file.replace(".pdf",".csv"))
		df = pd.concat(data, axis=0)
		df['File'],df['ReportYear']=file,year
		df.columns = headers
		df.to_csv(csv_file,index=False,header=True)
		print("CSV File Written to ",csv_file)


files = os.listdir(os.path.join(path, "srcpdfs"))
for file in files:
	if ".pdf" in file:
		print("Processing file ",file)
		process_pdf(file)

files = glob.glob(os.path.join(path, "csvs","*.csv"))
if len(files) > 0:
	full_file = os.path.join(path,"ufo_all_data.csv")
	df = pd.concat((pd.read_csv(f, header=0, names=headers) for f in files), ignore_index=True)
	df.to_csv(full_file, index=False,header=True)
	print("Created file ",full_file)
else:
	print("No CSV files found")
