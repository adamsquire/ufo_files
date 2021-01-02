#!/bin/bash
for filename in ../csvs/pdfplumber_csvs/*.csv; do
	rowcount=$(wc -l $filename)
	echo $rowcount
done
rowcount=$(wc -l ../outputs/csv/ufo_all_data.csv)
echo $rowcount
