import sublime, sublime_plugin
from modules import cssvariables
from modules import cssnesting
import sys, os

#
# Text Commands
#

class css_less_ish_compile_command(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		#reload_modules()
		cssvariables.apply(view, edit)
		cssnesting.apply(view, edit)
		print "Applied css variables and nesting for save"

class css_less_ish_decompile_command(sublime_plugin.TextCommand):
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
	os.chdir(basedir)
	__import__(fullmod)
	sys.modules[fullmod] = reload(sys.modules[fullmod])


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
				view.run_command('css_less_ish_decompile')
		else:
			view.run_command('css_less_ish_compile')

def delayed_restore(view):
	view.run_command('css_less_ish_decompile')