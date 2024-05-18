"""
  Dave Skura, Dec,2022

pip install psycopg2-binary
pip install mysql-connector-python
"""
from sqlitedave_package.sqlitedave import sqlite_db
from postgresdave_package.postgresdave import postgres_db 
from mysqldave_package.mysqldave import mysql_db 
from zetl.common import var

import warnings
import sys
import os
import re
from datetime import *

def get_dir_separator():
	somepath = os.getcwd()
	if somepath.find('/') > -1:
		dir_sep = '/'
	else:
		dir_sep = '\\'

	return dir_sep

def main():
	dir_sep = get_dir_separator()

	#my_zetl = zetl()
	my_zetl = zetl('c:' + get_dir_separator() +  'dave' + get_dir_separator() +  'git' + get_dir_separator() +  'zetl' + get_dir_separator() +  'tests','c:' + get_dir_separator() +  'dave' + get_dir_separator() +  'git' + get_dir_separator() +  'zetl' + get_dir_separator() +  'tests' + get_dir_separator() +  'zetl_scripts')
	my_zetl.set_logging_on()
	my_zetl.zetldb.empty_zetl()						# empty the master zetl table	
	my_zetl.zetldb.load_folders_to_zetl() # load master zetl table from folders

	if len(sys.argv) == 1 or sys.argv[1] == 'run.py': # no parameters
		my_zetl.loggerman('')
		my_zetl.loggerman('usage: ')
		my_zetl.loggerman('python -m zetl.run [etl_name] ') 
		my_zetl.loggerman('python -m zetl.view [etl_name] ') 
		my_zetl.loggerman(' ')
		my_zetl.loggerman('python -m zetl.postgres_import [csv_filename] [tablename] [WithTruncate]') 
		my_zetl.loggerman('python -m zetl.postgres_export [tablename] [csvfilename] [delimiter] ') 
		my_zetl.loggerman(' ')
		my_zetl.loggerman('python -m zetl.mysql_import [csv_filename] [tablename] [WithTruncate]') 
		my_zetl.loggerman('python -m zetl.mysql_export [tablename] [csvfilename] [delimiter] ') 
		my_zetl.loggerman('-----------')
		my_zetl.show_etl_name_list()

	else: # run the etl match the etl_name in the etl table
		etl_name_to_run = sys.argv[1]
		run_parameter = ''
		if len(sys.argv) > 2:
			run_parameter = sys.argv[2] # ARGV1 in the .sql files in zetl_scripts
		my_zetl.proper_run(etl_name_to_run,run_parameter)

	#my_zetl.proper_run('etl1','')
	#my_zetl.proper_run('demo2','')
	my_zetl.proper_run('audit','')
	sys.exit(0)

class zetl:
	def __init__(self,parent_dir = '',script_dir='',silent_on=False):
		launch_dir =  '.' + get_dir_separator()
		filepath_delimiter = get_dir_separator()
		if parent_dir != '':

			if parent_dir[-1:] != filepath_delimiter:
				launch_dir =  parent_dir + filepath_delimiter
			else:
				launch_dir = parent_dir


		self.script_directory = '.' + filepath_delimiter +'zetl_scripts'

		if script_dir != '':
			self.script_directory = script_dir

		#now = (datetime.now())
		#sztoday=str(now.year) + '-' + ('0' + str(now.month))[-2:] + '-' + str(now.day)
		self.silent_on = silent_on
		self.tempfilename = launch_dir + 'zetl_pythonscript_temp.log'
		self.singlefile_zetlname = 'zetl.zetl_this_file'

		self.force = True
		self.zetldb = zetldbaccess(launch_dir,self.script_directory,self.silent_on)

	def set_logging_on(self):
		print(self.tempfilename)
		self.silent_on = True
		self.zetldb.silent_on = self.silent_on
		f = open(self.tempfilename,'w')
		f.write('Begin Logging')
		f.close()
	def loggerman(self,logline):
		if self.silent_on:
			f = open(self.tempfilename,'a')
			f.write(logline + '\n')
			f.close()
		else:
			print(logline)

	def forcerun(self,etl_name_to_run,run_parameter=''):
		self.force = True
		self.proper_run(etl_name_to_run,run_parameter)

	def force_folder_run(self,folder):
		self.force = True
		self.proper_folder_run(folder)

	def proper_file_run(self,filename):
		self.zetldb.empty_zetl(self.singlefile_zetlname)		# empty the master zetl table
		self.zetldb.load_thisfile_to_zetl(self.singlefile_zetlname,filename) # 'f:\git\helloworld'

		activity = self.get_current_activity()
		if activity == 'idle' or self.force:
			self.execute('DELETE FROM z_activity')
			self.execute("INSERT INTO z_activity(currently,previously) VALUES ('Running " + filename + "','" + activity + "')")
			
			self.run_file_etl(filename)

			self.execute("UPDATE z_activity SET currently = 'idle',previously='Running " + filename + "'")
			self.commit()

		else:
			self.loggerman("zetl is currently busy with '" + activity + "'.  You can wait for it to finish or call zetl.force_folder_run(folder).")
	
	def proper_folder_run(self,folder):
		self.loggerman('Running ' + folder)
		self.zetldb.load_thisfolder_to_zetl(folder) # 'f:\git\helloworld'
		self.zetldb.export_thisfolder_zetl(folder)

		activity = self.get_current_activity()
		if activity == 'idle' or self.force:
			self.execute('DELETE FROM z_activity')
			self.execute("INSERT INTO z_activity(currently,previously) VALUES ('Running " + folder + "','" + activity + "')")
			
			self.runfolderetl(folder)

			self.execute("UPDATE z_activity SET currently = 'idle',previously='Running " + folder + "'")
			self.commit()

		else:
			self.loggerman("zetl is currently busy with '" + activity + "'.  You can wait for it to finish or call zetl.force_folder_run(folder).")

	def proper_run(self,etl_name_to_run,run_parameter=''):

		self.loggerman('Running ' + etl_name_to_run)
		self.zetldb.load_folders_to_zetl(etl_name_to_run)
		self.zetldb.export_zetl()

		activity = self.get_current_activity()
		if activity == 'idle' or self.force:
			self.execute('DELETE FROM z_activity')
			self.execute("INSERT INTO z_activity(currently,previously) VALUES ('Running " + etl_name_to_run + "','" + activity + "')")

			#self.loggerman('blat')
			self.runetl(etl_name_to_run,run_parameter)

			self.execute("UPDATE z_activity SET currently = 'idle',previously='Running " + etl_name_to_run + "'")
			self.commit()

		else:
			self.loggerman("zetl is currently busy with '" + activity + "'.  You can wait for it to finish or call zetl.forcerun(etlname,run_parameter).")

	def logstepstart(self,etl_name,stepnum,cmdfile,steptablename,query,ipart):

		try:
			zsql = "INSERT INTO z_log (etl_name,dbuser,stepnum,cmdfile,steptablename,"
			zsql += "cmd_to_run,part,rundtm) VALUES ('" + etl_name + "','zetl.run',"
			zsql += str(stepnum) + ",'" + str(cmdfile) + "','" + str(steptablename) + "','" 
			zsql += query.replace('?','').replace("'","`") + "'," + str(ipart) + ", current_timestamp);"
			self.execute(zsql)

		except:
			self.zetldb.create_table('z_log')
			self.execute(zsql)

		lid = self.queryone("SELECT max(id) FROM z_log ")
		return lid

	def logstepend(self,lid,the_rowcount,consoleoutput='not-passed-in',database='not-passed-in'):
		usql = "UPDATE z_log SET "

		if consoleoutput!='not-passed-in':
			usql += "script_output='" + consoleoutput.replace("'",'`') + "',"

		if database!='not-passed-in':
			usql += "database='" + database.replace("'",'`') + "',"

		usql += "rowcount = " + str(the_rowcount) + ", endtime = current_timestamp WHERE id = " + str(lid) 

		try:
			self.execute(usql)
		except Exception as e:
			self.loggerman(str(e))
			sys.exit(1) 


	def f1(self,foo=''): return iter(foo.splitlines())

	def RemoveComments(self,asql):
		foundacommentstart = 0
		foundacommentend = 0
		ret = ""

		for line in self.f1(asql):
			
			if not line.startswith( '--' ):
				if line.find('/*') > -1:
					foundacommentstart += 1

				if line.find('*/') > -1:
					foundacommentend += 1
				
				if foundacommentstart == 0:
					ret += line + '\n'

				if foundacommentstart > 0 and foundacommentend > 0:
					foundacommentstart = 0
					foundacommentend = 0	

		return ret

	def log_script_error(self,lid=-1,pscript_error='',database='',pscript_output=''):
		script_error = pscript_error
		if len(pscript_error) > 250:
			script_error = pscript_error[250:]

		script_output = pscript_output
		if len(pscript_output) > 8100:
			script_output = pscript_output[-8100:]


		usql = "UPDATE z_log SET database='" + database.replace("'",'`') + "', script_output = '" + script_output.replace("'","`") + "', script_error = '" + script_error.replace("'","`") + "', endtime = current_timestamp WHERE id = " + str(lid) 
		try:
			self.execute(usql)
			self.commit()
		except Exception as e:
			self.loggerman(str(e))

	def run_one_etl_step(self,etl_name,stepnum,steptablename,cmdfile,run_parameter='',cmdfilename=''):
		script_variables = {'SHOWQUERY':'True','DB_TYPE':'','DB_USERNAME':'','DB_USERPWD':'','DB_HOST':'','DB_PORT':'','DB_NAME':'','DB_SCHEMA':''}
		global_variables = {}

		if cmdfilename != '':
			findcmdfile = cmdfilename
		else:
			findcmdfile = self.script_directory + get_dir_separator() + etl_name + get_dir_separator() + cmdfile

		try:
			f = open(findcmdfile,'r') 
			sqlfromfile = f.read()
			sqlfromfile = sqlfromfile.replace('\\r','')

			f.close()
		except Exception as e:
			raise Exception('cannot open cmd file ' + cmdfile)
			self.loggerman(str(e))
			sys.exit(0)

		sqllines = sqlfromfile.split('\n')
		for i in range(0,len(sqllines)):
			line = sqllines[i].split('=')
			variable_name = line[0].strip()

			if (len(line) > 1 )and (variable_name in script_variables):
				script_variables[variable_name] = line[1].strip()
			elif len(line) > 1 and variable_name.upper().find('GBLVAR_') == 0: # global variable created

				var().set_global_variable(variable_name,line[1].strip())
				global_variables[variable_name] = line[1].strip()

			elif len(line) > 1 and variable_name.upper().find('USE GLOBAL VARIABLES') == 0: # found use global variables=something,some other thing,this one thing
				gblvariables = line[1].strip()
				for onevar in gblvariables.split(','):
					if onevar not in global_variables: # only add if not there
						global_variables[onevar] = var().get_global_variable(onevar)

		sql = self.RemoveComments(sqlfromfile.strip())

		ipart = 0
		for individual_query in sql.split(';'):

			ipart += 1
			individual_query = individual_query.strip()
			if not individual_query.isspace() and individual_query != '':
				script_output = ''

				self.loggerman('\n file ' + cmdfile + ', step ' + str(ipart))
				if script_variables['SHOWQUERY'].upper().strip() == 'TRUE':
					self.loggerman(individual_query)

				#script_output += individual_query + '\n \n'
				for variable in script_variables:
					individual_query = individual_query.replace('SCRIPT{' + variable + '}',script_variables[variable])

				for variable in global_variables:
					individual_query = individual_query.replace('SCRIPT{' + variable + '}',global_variables[variable])

				lid = self.logstepstart(etl_name,stepnum,cmdfile,steptablename,individual_query,ipart)
				database = ''

				try:
					if script_variables['DB_TYPE'] != '': # dont use default connection
						new_postgresdb = postgres_db()
						new_mysqldb = mysql_db()

						if script_variables['DB_TYPE'].strip().upper() == 'POSTGRES':
							self.connect_mysql(new_postgresdb,script_variables)

							script_output, database = self.run_db_query(new_postgresdb,individual_query)
							database = script_variables['DB_TYPE'] + ': ' + database
							self.logend_steptable(new_postgresdb,lid,script_variables,steptablename,script_output,database)

						elif script_variables['DB_TYPE'].strip().upper() == 'MYSQL':
							self.connect_mysql(new_mysqldb,script_variables)

							script_output, database = self.run_db_query(new_mysqldb,individual_query)
							database = script_variables['DB_TYPE'] + ': ' + database
							self.logend_steptable(new_mysqldb,lid,script_variables,steptablename,script_output,database)

						else:
							self.loggerman('DB_TYPE must be either Postgres or MySQL')
							sys.exit(0)


					else: # use default connection
						database = 'default: ' + self.zetldb.db.dbstr()
						if individual_query.strip().upper().find('SELECT') == 0:
							results = self.zetldb.db.export_query_to_str(individual_query)
							self.loggerman('\n' + results)
							script_output += results

						else:

							self.zetldb.db.execute(individual_query)

						
						self.logend_steptable(self.zetldb.db,lid,script_variables,steptablename,script_output,database)
				except Exception as e:
					self.log_script_error(lid,str(e),database, script_output)
					self.loggerman(str(e))
					sys.exit(1)

	def connect_postgres(self,postgresdb,script_variables):
		if script_variables['DB_HOST'] != '': # variables set in file.  use them to connect
			postgresdb.useConnectionDetails(script_variables['DB_USERNAME']
							,script_variables['DB_USERPWD']
							,script_variables['DB_HOST']
							,script_variables['DB_PORT']
							,script_variables['DB_NAME']
							,script_variables['DB_SCHEMA']
							)
		else: # use default mysql connection
			postgresdb.connect()
		self.loggerman(postgresdb.dbstr())

	def connect_mysql(self,mysqldb,script_variables):
		if script_variables['DB_HOST'] != '': # variables set in file.  use them to connect
			mysqldb.useConnectionDetails(script_variables['DB_USERNAME']
							,script_variables['DB_USERPWD']
							,script_variables['DB_HOST']
							,script_variables['DB_PORT']
							,script_variables['DB_NAME']
							)
		else: # use default mysql connection
			mysqldb.connect()
		self.loggerman(mysqldb.dbstr())


	def run_db_query(self,dbconn,individual_query):
		script_output = ''

		if individual_query.strip().upper().find('SELECT') == 0:
			results = dbconn.export_query_to_str(individual_query)
			script_output += results
			self.loggerman('\n' + results)

		else:

			dbconn.execute(individual_query)
			dbconn.commit()

		return script_output, dbconn.dbstr()


	def logend_steptable(self,dbconn,lid,script_variables,steptablename='',script_output='',database=''):
		tblrowcount = 0
		qualified_table = ''
		if script_variables['DB_TYPE'] != '': # dont use default connection
			if script_variables['DB_TYPE'].upper() == 'MYSQL':
				qualified_table = steptablename
				tblrowcount = dbconn.cur.rowcount

			elif (script_variables['DB_TYPE'].upper() == 'POSTGRES'):
				try:
					this_table = steptablename.split('.')[1]
					this_schema = steptablename.split('.')[0]
				except:
					this_table = steptablename
					if script_variables['DB_SCHEMA'] != '':
						this_schema = script_variables['DB_SCHEMA']
					else:
						this_schema = 'public'
				qualified_table = this_schema + '.' + this_table
				if dbconn.does_table_exist(qualified_table):
					tblrowcount = dbconn.queryone("SELECT COUNT(*) FROM " + qualified_table)
					dbconn.close()

			else:
				self.loggerman('DB_TYPE must be Postgres or MySQL')

		else: # use default connection
			qualified_table = steptablename
			if dbconn.does_table_exist(qualified_table):
				tblrowcount = dbconn.queryone("SELECT COUNT(*) FROM " + qualified_table)
				dbconn.close()

		self.logstepend(lid,tblrowcount,script_output,database)

	def get_current_activity(self):
		sql = """
			SELECT *
			FROM (
					SELECT currently,activity_type FROM z_activity
					UNION
					SELECT '' as currently,'default' as activity_type
					) L
			ORDER BY 1 desc
		"""
		try:
			data = self.zetldb.db.query(sql)
		except:
			self.loggerman('z_activity does not exist, creating it')
			self.zetldb.create_table('z_activity')
			data = self.zetldb.db.query(sql)
		
		for row in data:
			if row[1] == 'default':
				return_value = 'idle'
			else:
				return_value = row[0] 

		return return_value

	def runfolderetl(self,folder):
		self.loggerman(folder)
		sql = """
		SELECT stepnum,steptablename,cmdfile 
		FROM z_etl 
		WHERE etl_name = '""" + folder + """'
		ORDER BY etl_name, stepnum
		"""

		data = self.zetldb.db.query(sql)
		for row in data:
			consoleoutput = ''
			stepnum = row[0]
			steptablename = ''
			if row[1]:
				steptablename = row[1]

			cmdfile = row[2]
			foundfile = folder + get_dir_separator() + cmdfile
			if cmdfile.lower().endswith('.sql') or cmdfile.lower().endswith('.ddl'):
				self.run_one_etl_step(folder,stepnum,steptablename,cmdfile,'',folder + get_dir_separator() + cmdfile)

			elif cmdfile.lower().endswith('.py'):

				lid = self.logstepstart(folder,stepnum,cmdfile,steptablename,'Python script',0)

				self.loggerman('\n file ' + cmdfile + '\n')
				cmd_to_run = 'python ' + foundfile + ' '
				if self.silent_on:
					cmd_to_run += ' >> ' + self.tempfilename

				self.loggerman(cmd_to_run)
				exit_code = os.system(cmd_to_run)

				if self.silent_on:
					f = open(self.tempfilename,'r')
					consoleoutput = f.read()
					f.close()

				if exit_code != 0:
					self.loggerman(consoleoutput + '\n exit_code=' + str(exit_code))
					self.log_script_error(lid,foundfile + ' failed with error_code ' + str(exit_code),self.zetldb.db.dbstr(),consoleoutput.strip())
					self.logstepend(lid,0)

					sys.exit(exit_code)

				self.logstepend(lid,0,consoleoutput.strip(),self.zetldb.db.dbstr())

			elif cmdfile.lower().endswith('.bat'):
				lid = self.logstepstart(folder,stepnum,cmdfile,steptablename,'Windows bat script',0)

				self.loggerman('\n file ' + cmdfile + '\n')
				cmd_to_run = foundfile + ' ' 
				if self.silent_on:
					cmd_to_run += ' >> ' + self.tempfilename

				exit_code = os.system(cmd_to_run)

				if self.silent_on:
					f = open(self.tempfilename,'r')
					consoleoutput = f.read()
					f.close()
				
				if exit_code != 0:
					self.loggerman(consoleoutput + '\n exit_code=' + str(exit_code))
					self.log_script_error(lid,foundfile + ' failed with error_code ' + str(exit_code),self.zetldb.db.dbstr(),consoleoutput.strip())
					self.logstepend(lid,0)

					sys.exit(exit_code)

				self.logstepend(lid,0,consoleoutput.strip(),self.zetldb.db.dbstr())

	def run_file_etl(self,cmdfile,run_parameter=''):
		etl_name = self.singlefile_zetlname
		stepnum = '1'
		steptablename = ''
		consoleoutput=''
		foundfile = cmdfile

		if cmdfile.lower().endswith('.sql') or cmdfile.lower().endswith('.ddl'):
			self.run_one_etl_step(etl_name,stepnum,steptablename,cmdfile,run_parameter,cmdfile)

		elif cmdfile.lower().endswith('.py'):

			lid = self.logstepstart(etl_name,stepnum,cmdfile,steptablename,'Python script',0)

			self.loggerman('\n file ' + cmdfile + '\n')
			cmd_to_run = 'python ' + cmdfile + ' ' + run_parameter

			self.loggerman(cmd_to_run)
			exit_code = os.system(cmd_to_run)

			if exit_code != 0:
				self.loggerman(consoleoutput + '\n exit_code=' + str(exit_code))
				self.log_script_error(lid,foundfile + ' failed with error_code ' + str(exit_code),self.zetldb.db.dbstr(),consoleoutput.strip())
				self.logstepend(lid,0)

				sys.exit(exit_code)

			self.logstepend(lid,0,consoleoutput.strip(),self.zetldb.db.dbstr())

		elif cmdfile.lower().endswith('.bat'):
			lid = self.logstepstart(etl_name,stepnum,cmdfile,steptablename,'Windows bat script',0)

			self.loggerman('\n file ' + cmdfile + '\n')
			cmd_to_run = cmdfile + ' ' + run_parameter

			exit_code = os.system(cmd_to_run)
			
			if exit_code != 0:
				self.loggerman(consoleoutput + '\n exit_code=' + str(exit_code))
				self.log_script_error(lid,foundfile + ' failed with error_code ' + str(exit_code),self.zetldb.db.dbstr(),consoleoutput.strip())
				self.logstepend(lid,0)

				sys.exit(exit_code)

			self.logstepend(lid,0,consoleoutput.strip(),self.zetldb.db.dbstr())

	def runetl(self,etl_name,run_parameter=''):
		sql = """
		SELECT stepnum,steptablename,cmdfile 
		FROM z_etl 
		WHERE etl_name = '""" + etl_name + """'
		ORDER BY etl_name, stepnum
		"""
		data = self.zetldb.db.query(sql)
		
		for row in data:
			consoleoutput = ''
			stepnum = row[0]
			steptablename = ''
			if row[1]:
				steptablename = row[1]

			cmdfile = row[2]
			foundfile = self.script_directory + get_dir_separator() + etl_name + get_dir_separator() + cmdfile
			#print('stepnum = \t\t' + str(stepnum))
			#print('steptablename = \t' + steptablename)
			#print('cmdfile = \t\t' + cmdfile)
			if cmdfile.lower().endswith('.sql') or cmdfile.lower().endswith('.ddl'):
				self.run_one_etl_step(etl_name,stepnum,steptablename,cmdfile,run_parameter)

			elif cmdfile.lower().endswith('.py'):

				lid = self.logstepstart(etl_name,stepnum,cmdfile,steptablename,'Python script',0)

				self.loggerman('\n file ' + cmdfile + '\n')
				cmd_to_run = 'python ' + foundfile + ' ' + run_parameter
				if self.silent_on:
					cmd_to_run += ' >> ' + self.tempfilename

				self.loggerman(cmd_to_run)
				exit_code = os.system(cmd_to_run)

				if self.silent_on:
					f = open(self.tempfilename,'r')
					consoleoutput = f.read()
					f.close()

				if exit_code != 0:
					self.loggerman(consoleoutput + '\n exit_code=' + str(exit_code))
					self.log_script_error(lid,foundfile + ' failed with error_code ' + str(exit_code),self.zetldb.db.dbstr(),consoleoutput.strip())
					self.logstepend(lid,0)

					sys.exit(exit_code)

				self.logstepend(lid,0,consoleoutput.strip(),self.zetldb.db.dbstr())

			elif cmdfile.lower().endswith('.bat'):
				lid = self.logstepstart(etl_name,stepnum,cmdfile,steptablename,'Windows bat script',0)

				self.loggerman('\n file ' + cmdfile + '\n')
				cmd_to_run = foundfile + ' ' + run_parameter
				if self.silent_on:
					cmd_to_run += ' >> ' + self.tempfilename

				exit_code = os.system(cmd_to_run)

				if self.silent_on:
					f = open(self.tempfilename,'r')
					consoleoutput = f.read()
					f.close()
				
				if exit_code != 0:
					self.loggerman(consoleoutput + '\n exit_code=' + str(exit_code))
					self.log_script_error(lid,foundfile + ' failed with error_code ' + str(exit_code),self.zetldb.db.dbstr(),consoleoutput.strip())
					self.logstepend(lid,0)

					sys.exit(exit_code)

				self.logstepend(lid,0,consoleoutput.strip(),self.zetldb.db.dbstr())

	def show_etl_name_list(self):
		data = self.zetldb.db.query('SELECT distinct etl_name from z_etl order by etl_name')
		for row in data:
			self.loggerman(' ' + row[0])

	def execute(self,prm):
		return self.zetldb.db.execute(prm)

	def commit(self):
		return self.zetldb.db.commit()

	def queryone(self,prm):
		return self.zetldb.db.queryone(prm)


class zetldbaccess:

	def __init__(self,parent_dir = '',script_dir='',silent_on=False):
		dbfile = ''
		launch_dir = '.' + get_dir_separator()
		if parent_dir != '':
			launch_dir = parent_dir

		
		dbfile = launch_dir + 'local_sqlite_db'
		self.db = sqlite_db(dbfile)
		self.db.connect()
	
		if script_dir != '':
			self.script_directory = script_dir
		else:
			self.script_directory = './/zetl_scripts'

		self.tempfilename = launch_dir + 'zetl_pythonscript_temp.log'
		
		self.silent_on = silent_on

		self.version=3.0

	def loggerman(self,logline):
		if self.silent_on:
			f = open(self.tempfilename,'a')
			f.write(logline + '\n')
			f.close()
		else:
			print(logline)


	def export_thisfolder_zetl(self,folder):
		zsql = ' SELECT DISTINCT etl_name FROM z_etl '
		if folder != '':
			zsql += "WHERE upper(etl_name) like upper('" + folder + "') "
		zsql += ' ORDER BY etl_name '
		etl_list = self.db.query(zsql)
		for etl in etl_list:
			etl_name = etl[0]
			qry = "SELECT stepnum,cmdfile,steptablename,estrowcount FROM z_etl WHERE etl_name = '" + etl_name + "' ORDER BY stepnum"
			csv_filename = folder + get_dir_separator() + 'z_etl.csv'
			self.db.export_query_to_csv(qry,csv_filename)


	def export_zetl(self,etl_name =''):
		zsql = ' SELECT DISTINCT etl_name FROM z_etl '
		if etl_name != '':
			zsql += "WHERE upper(etl_name) like upper('" + etl_name + "') "
		zsql += ' ORDER BY etl_name '
		etl_list = self.db.query(zsql)
		for etl in etl_list:
			etl_name = etl[0]
			qry = "SELECT stepnum,cmdfile,steptablename,estrowcount FROM z_etl WHERE etl_name = '" + etl_name + "' ORDER BY stepnum"
			csv_filename = self.script_directory + get_dir_separator() + etl_name + get_dir_separator() + 'z_etl.csv'
			self.db.export_query_to_csv(qry,csv_filename)

	def empty_zetl(self,etl_name=''):
		try:
			dsql = "DELETE FROM z_etl "
			if etl_name != '':
				dsql += " WHERE upper(etl_name) like upper('" + etl_name + "') "
			self.db.execute(dsql)
			self.db.commit()
		except:
			self.create_table('z_etl')

	def create_table(self,tbl):
		csql = "SELECT 'cannot create table " + tbl + "'  "
		if tbl.lower() == 'z_etl':
			csql = """
			CREATE TABLE z_etl (
				etl_name text, 
				stepnum real, 
				steptablename text, 
				estrowcount integer, 
				cmdfile text, 
				cmd_to_run text, 
				note text, 
				dtm text 
			);
			"""
		elif tbl.lower() == 'z_activity':
			csql = """
			CREATE TABLE z_activity (
				activity_type real PRIMARY KEY,
				currently text, 
				previously text, 
				keyfld text, 
				prvkeyfld text, 
				dtm text
			);

			"""
		elif tbl.lower() == 'z_log':
			csql = """
			CREATE TABLE z_log (
				id INTEGER PRIMARY KEY AUTOINCREMENT , 
				dbuser text, 
				rundtm text, 
				etl_name text, 
				stepnum real, 
				part INTEGER, 
				steptablename text, 
				rowcount integer, 
				starttime text,  
				endtime text, 
				cmd_to_run text, 
				script_output text, 
				script_error text, 
				cmdfile text, 
				database tect, 
				dtm text
			);

			"""
		self.loggerman(csql)
		self.db.execute(csql)
		self.db.commit()

	def load_z_etlcsv_if_forced(self,etl_name='',option=''):
		szdelimiter = ','
		if (etl_name != '' and option == '-f'):
			self.empty_zetl()
			qualified_table = "z_etl"
			csv_filename = self.script_directory + get_dir_separator() + etl_name + get_dir_separator() + 'z_etl.csv'
			f = open(csv_filename,'r')
			hdrs = f.read(1000).split('\n')[0].strip().split(szdelimiter)
			f.close()		
			
			isqlhdr = 'INSERT INTO ' + qualified_table + '('

			for i in range(0,len(hdrs)):
				isqlhdr += hdrs[i] + ','
			isqlhdr = isqlhdr[:-1] + ') VALUES '

			skiprow1 = 0
			ilines = ''

			with open(csv_filename) as myfile:
				for line in myfile:
					if skiprow1 == 0:
						skiprow1 = 1
					else:
						row = line.rstrip("\n").split(szdelimiter)

						newline = '('
						for j in range(0,len(row)):
							if row[j].lower() == 'none' or row[j].lower() == 'null':
								newline += "NULL,"
							else:
								newline += "'" + row[j].replace(',','').replace("'",'') + "',"
							
						ilines += newline[:-1] + ')'
						
						qry = isqlhdr + ilines
						ilines = ''
						self.db.execute(qry)
						self.db.commit()

	def is_an_int(self,prm):
			try:
				if int(prm) == int(prm):
					return True
				else:
					return False
			except:
					return False

	def add_etl_step(self,p_etl_name,p_etl_step,p_etl_filename):
		isql = "INSERT INTO z_etl(etl_name,stepnum,cmdfile) VALUES ('" + p_etl_name + "'," + p_etl_step + ",'" + p_etl_filename + "')"
		self.db.execute(isql)
		self.db.commit()

	def etl_step_exists(self,etl_name,etl_step):
		sql = "SELECT COUNT(*) FROM z_etl WHERE etl_name = '" + etl_name + "' and stepnum = " + etl_step
		etlrowcount = self.db.queryone(sql)
		if etlrowcount == 0:
			return False
		else:
			return True

	# sample folder: 1.this.sql
	def load_thisfile_to_zetl(self,etl_name,etl_script_file):

		if etl_script_file.endswith(".sql") or etl_script_file.endswith(".ddl") or etl_script_file.endswith(".py") or etl_script_file.endswith(".bat"):

			# only interest in files that follow the namoing convention '#.name.suffix'
			if len(etl_script_file.split('.')) == 3:
				# eg 1.something.sql
				
				# file_suffix = something.sql
				file_suffix = etl_script_file.split('.')[1] + '.' + etl_script_file.split('.')[2]
				
				# etl_step = 1
				etl_step = etl_script_file.split('.')[0]

				# etl_step must be a number
				if self.is_an_int(etl_step):
					
					# only add if it doesn't exist already
					if not self.etl_step_exists(etl_name,etl_step):

						self.add_etl_step(etl_name,etl_step,etl_script_file)		


	# sample folder: f:\git\project1
	def load_thisfolder_to_zetl(self,folder):
		for etl_script_file in os.listdir(folder):
			# only interest in files that follow the namoing convention '#.name.suffix'
			if len(etl_script_file.split('.')) == 3:
				# eg 1.something.sql
				
				# file_suffix = something.sql
				file_suffix = etl_script_file.split('.')[1] + '.' + etl_script_file.split('.')[2]
				
				# etl_step = 1
				etl_step = etl_script_file.split('.')[0]

				# etl_step must be a number
				if self.is_an_int(etl_step):
					
					# only add if it doesn't exist already
					if not self.etl_step_exists(folder,etl_step):

						self.add_etl_step(folder,etl_step,etl_script_file)		

	def load_folders_to_zetl(self,this_etl_name='all'):
		etl_folder = self.script_directory 
		subdirs = [x[0] for x in os.walk(etl_folder)]
		for i in range(0,len(subdirs)):

			possible_etl_dir = subdirs[i]
			zetl_foldername_only=possible_etl_dir.split(etl_folder)[1]

			if len(zetl_foldername_only.split(get_dir_separator())) == 2:
				etl_name = zetl_foldername_only.split(get_dir_separator())[1]

				if (etl_name != 'zetl_scripts') and (this_etl_name == 'all' or etl_name == this_etl_name):
					for etl_script_file in os.listdir(etl_folder + get_dir_separator() + etl_name):
						if etl_script_file.endswith(".sql") or etl_script_file.endswith(".ddl") or etl_script_file.endswith(".py") or etl_script_file.endswith(".bat"):
							if len(etl_script_file.split('.')) == 3:
								etl_step = etl_script_file.split('.')[0]
								file_suffix = etl_script_file.split('.')[1] + '.' + etl_script_file.split('.')[2]
								if self.is_an_int(etl_step):
									if not self.etl_step_exists(etl_name,etl_step):
										self.add_etl_step(etl_name,etl_step,etl_script_file)		


if __name__ == '__main__':
	main()

		


