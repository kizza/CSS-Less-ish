import sys, os, sublime, sublime_plugin
from modules import cssvariables, cssnesting

#
# Text Commands
#

class css_less_ish_compile_command(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		#reload_modules()
		cssvariables.apply(view, edit)
		cssnesting.apply(view, edit)
		print "CSS Less(ish) Compiled"

class css_less_ish_decompile_command(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		#reload_modules()
		cssnesting.remove(view, edit)
		highlights = cssvariables.remove(view, edit)
		highlight(view, highlights)
		print "CSS Less(ish) Decompiled"

#
# Helpers
#

def highlight(view, regions):
	highlight_delay = get_setting('highlight_delay')
	if highlight_delay > 0:
		view.add_regions('css-less-ish', regions, 'entity.name.class', sublime.DRAW_OUTLINED)
		callback = lambda: unhighlight(view)
		sublime.set_timeout(callback, highlight_delay)

def unhighlight(view):
	view.erase_regions('css-less-ish')

def get_setting(name):
	settings = sublime.load_settings('csslessish.sublime-settings')
	return int(settings.get(name, 500))
	
def reload_modules():
	load_module('cssvariables')
	load_module('cssnesting')

# reload module (borrowed from sublimelint for ease when debugging)
basedir = os.getcwd()
def load_module(name):
	path = 'modules.' + name
	os.chdir(basedir)
	__import__(path)
	sys.modules[path] = reload(sys.modules[path])

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
		# Only process if there are variables or nestings
		if not view.find("@\w+", 0) and not view.find("\w+\s*\[", 0):
			return
		if type=='restore':
			restore_delay = get_setting('restore_delay')
			if restore_delay > 0:
				callback = lambda: restore(view)
				sublime.set_timeout(callback, restore_delay)
			else:
				restore(view)
		else:
			view.run_command('css_less_ish_compile')

def restore(view):
	view.run_command('css_less_ish_decompile')