"""
  Dave Skura, 2023
"""
import sys

from mysqldave_package.mysqldave import mysql_db #install pip install mysqldave-package

def main():
	if len(sys.argv) == 1 or sys.argv[1] == 'mysql_extract.py': # no parameters
		print('usage: ')
		print('mysql_extract.py [query] [csvfilename] [delimiter] ') 
		print('')

	elif (len(sys.argv) == 2) : 
		query = sys.argv[1]
		myexp = dbexport(query)

	elif (len(sys.argv) == 3) : 
		query = sys.argv[1]
		csv_filename = sys.argv[2]
		myexp = dbexport(query,csv_filename)

	elif (len(sys.argv) == 4) : 
		query = sys.argv[1]
		csv_filename = sys.argv[2]
		delimiter = sys.argv[3]
		myexp = dbexport(query,csv_filename,delimiter)

	else:
		print('Error: Incorrect number of parameters.')
		print('')
		print('usage: ')
		print('mysql_extract.py [query] [csvfilename] [delimiter] ') 
		print('')

class dbexport():
	def __init__(self,query='',csv_filename='',delimiter='\t'):
		self.mydb = mysql_db()
		if csv_filename == '':
			csv_filename='query.tsv'

		self.mydb.export_query_to_csv(query,csv_filename,delimiter)
		self.mydb.close()

		print('query exported to ' + csv_filename)


if __name__ == '__main__':
	main()

		

