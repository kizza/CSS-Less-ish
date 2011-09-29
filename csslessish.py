import sublime, sublime_plugin
from modules import cssvariables
from modules import cssnesting
import sys, os

#
# Text Commands
#

class strip_css_variables_command(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		#reload_modules()
		cssvariables.apply(view, edit)
		cssnesting.apply(view, edit)
		print "Applied css variables and nesting for save"

class restore_css_variables_command(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		#reload_modules()
		cssnesting.remove(view, edit)
		cssvariables.remove(view, edit)
		
		print "Restored css variables and nesting for editing"

#
# Helpers
#

def reload_modules():
	load_module('cssvariables')
	load_module('cssnesting')

# reload module - borrowed from sublimelint
basedir = os.getcwd()
modpath = 'modules'
def load_module(name):
	fullmod = '%s.%s' % (modpath, name)
	# make sure the path didn't change on us (this is needed for submodule reload)
	#pushd = os.getcwd()
	os.chdir(basedir)
	__import__(fullmod)
	# this following line does two things:
	# first, we get the actual module from sys.modules, not the base mod returned by __import__
	# second, we get an updated version with reload() so module development is easier
	# (save sublimelint_plugin.py to make sublime text reload language submodules)
	#mod = 
	sys.modules[fullmod] = reload(sys.modules[fullmod])
	# update module's __file__ to absolute path so we can reload it if saved with sublime text
	#mod.__file__ = os.path.abspath(mod.__file__).rstrip('co')
	#os.chdir(pushd)

#
# Hooks
#

class cssvariables_plugin(sublime_plugin.EventListener):
	def on_load(self, view):
		process(view, 'restore')		
	def on_pre_save(self, view):
		process(view, 'strip')		
	def on_post_save(self, view):
		process(view, 'restore')	

def process(view, type):
	if view.file_name().endswith('.css'):
		# Only process if there are variables
		if not view.find("@\w+", 0):
			return
		if type=='restore':
			settings = sublime.load_settings('css less-ish.sublime-settings')
			restore_delay = int(settings.get('restore_delay', 300))
			if restore_delay != 0:
				callback = lambda: delayed_restore(view)
				sublime.set_timeout(callback, restore_delay)
			else:
				view.run_command('restore_css_variables')
		else:
			view.run_command('strip_css_variables')

def delayed_restore(view):
	view.run_command('restore_css_variables')