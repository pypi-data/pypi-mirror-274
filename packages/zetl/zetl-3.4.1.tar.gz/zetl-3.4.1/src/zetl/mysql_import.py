"""
  Dave Skura,2023
"""
import sys,os
from schemawizard_package.schemawizard import schemawiz

def main():
	if len(sys.argv) == 1 or sys.argv[1] == 'mysql_import.py': # no parameters
		print('usage: ')
		print('mysql_import.py [csv_filename] [tablename] [WithTruncate]') 
		print('')
		print('bool WithTruncate = [True,False]')

	elif (len(sys.argv) == 2) : 
		csv_filename = sys.argv[1]
		myexp = dbimport(csv_filename)

	elif (len(sys.argv) == 3) : 
		csv_filename = sys.argv[1]
		tablename = sys.argv[2]

		myexp = dbimport(csv_filename,tablename)

	elif (len(sys.argv) == 4) : 
		csv_filename = sys.argv[1]
		tablename = sys.argv[2]
		WithTruncate = bool(sys.argv[2])

		myexp = dbimport(csv_filename,tablename,WithTruncate)

	else:
		print('Error: Incorrect number of parameters.')
		print('')
		print('usage: ')
		print('mysql_import.py [csv_filename] [tablename] [WithTruncate]') 
		print('')
		print('bool WithTruncate = [True,False]')

class dbimport():
	def get_dir_separator(self):
			somepath = os.getcwd()
		if somepath.find('/') > -1:
			self.dir_sep = '/'
		else:
			self.dir_sep = '\\'

		return self.dir_sep

	def __init__(self,csv_filename,tablename='',WithTruncate=False):
		self.dir_sep = self.get_dir_separator()
		tbl = tablename
		dber = schemawiz()
		if ((tablename != '') and (dber.dbthings.mysql_db.does_table_exist(tablename))):
			dber.justload_mysql_from_csv(csv_filename,tablename,WithTruncate)
		else:
			output_ddl_filename = 'z.' + self.getoutputfilename(csv_filename,tablename) + '.ddl'
			tbl = dber.createload_mysql_from_csv(csv_filename,tablename,output_ddl_filename)

		print(dber.dbthings.mysql_db.queryone('SELECT COUNT(*) FROM ' + tbl))
		dber.dbthings.mysql_db.close()

		print(csv_filename + ' imported to ' + tbl)

	def getoutputfilename(self,csv_filename,ddl_output_filename):
		# zetl_scripts/someetl/thisfile.csv
		filedelimiter = self.dir_sep
		if csv_filename.find('/') > -1:
			filedelimiter = '/'

		newfile = ''
		partlist = csv_filename.split(filedelimiter)
		if partlist[0] != csv_filename:
			for i in range(0,len(partlist)-1):
				newfile += partlist[i] + filedelimiter

		newfile += ddl_output_filename
		return newfile

if __name__ == '__main__':
	#myexp = dbimport('BMONAS-Finalresend.csv','sample8',True)
	#tbl = schemawiz().createload_mysql_from_csv('sample7.csv','restored_sample7')
 
	main()

		