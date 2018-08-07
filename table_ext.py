from tabula import read_pdf, convert_into

convert_into("1.pdf", 'tbl_output.csv', encoding='cp1252', pages="all")

