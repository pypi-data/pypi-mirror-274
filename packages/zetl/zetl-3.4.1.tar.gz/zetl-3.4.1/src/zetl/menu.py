"""
  Dave Skura
  
"""
import os, sys
import readchar
from zetl.run import zetl


def main():
	em = etl_menu()
	while True:
		print('')
		option_count = em.show_menu()
		print('')
		if option_count > 1:
			if option_count < 10:
				print('SINGLE CHAR ENTRY.  Select from 0 to ' + str(option_count-1))
				user_selection = int(readchar.readchar())
			else:
				user_msg = 'Select from 0 to ' + str(option_count-1) + ' :'
				user_selection = int(input(user_msg) or 0)

			if user_selection == 0:
				sys.exit(0)
			elif user_selection <= option_count and user_selection > -1:
				print("Running ", user_selection, em.etl_list[user_selection])
				em.run_zetl(em.etl_list[user_selection])
			else:
				print("You broke something ")
		else:
			sys.exit(0)

class etl_menu:
	def get_dir_separator(self):
		somepath = os.getcwd()
		if somepath.find('/') > -1:
			self.dir_sep = '/'
		else:
			self.dir_sep = '\\'
		self.dir_sep = 	os.sep
		return self.dir_sep

	def __init__(self):
		self.dir_sep = self.get_dir_separator()
		self.etl_path = os.getcwd() + self.dir_sep + 'zetl_scripts'
		self.etl_list = []
		self.etlcount = 0
		self.findetls()

	def run_zetl(self,etl_name_to_run):
		run_parameter = ''
		my_zetl = zetl()
		my_zetl.zetldb.empty_zetl()						
		my_zetl.zetldb.load_folders_to_zetl() 
		my_zetl.proper_run(etl_name_to_run,run_parameter)

	def findetls(self):
		self.etl_list.append('0 - exit from zetl.menu')
		subfolders = [ f.path for f in os.scandir(self.etl_path) if f.is_dir() ]
		for etlwithpath in subfolders:
			etl_with_char = etlwithpath.split(self.etl_path)[1] 
			etl = etl_with_char.split(self.get_dir_separator())[1]
			self.etl_list.append(etl)
			self.etl_list.sort()
		self.etlcount = len(self.etl_list)

	def show_menu(self):

		print ("zetl menu v1.0 \n --------------") #
		for nbr in range(0,self.etlcount):
			print(nbr,'\t' + self.etl_list[nbr])

		return self.etlcount

if __name__ == '__main__':
	main()
