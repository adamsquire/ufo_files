#!/usr/bin/env bash
wget https://www.gov.uk/government/publications/ufo-reports-in-the-uk -P ../srchtml
grep '<a href="' ../srchtml/ufo-reports-in-the-uk | grep pdf | cut -d '"' -f4 > ../urls/urls.txt
