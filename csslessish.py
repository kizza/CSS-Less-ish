from __future__ import print_function
import sys, os, sublime, sublime_plugin
if sys.version_info < (3, 0):
	from modules import cssvariables, cssnesting
	import tests
else:
	from .modules import cssvariables, cssnesting
	from . import tests


def plugin_loaded():
    """The ST3 entry point for plugins."""


#
# Global 
#
is_running = False
def is_finished():
	global is_running
	return not is_running

def mark_as_running():
	global is_running
	is_running = True

def mark_as_finished():
	global is_running
	is_running = False

#
# Text Commands
#

class css_less_ish_compile_command(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		cssvariables.apply(view, edit)
		cssnesting.apply(view, edit)

class css_less_ish_decompile_command(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		cssnesting.remove(view, edit)
		cssvariables.remove(view, edit)
		highlight(view)

class css_less_ish_scope_command(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		regions = view.sel()
		for region in regions:
			print(view.scope_name(region.a))

class css_less_ish_run_tests_command(sublime_plugin.TextCommand):
	def run(self, edit):
		reload_modules()
		reload_modules()
		tests.run(self.view, edit)

#
# Helpers
#

def highlight(view):
	highlight_delay = get_setting('highlight_delay', int)
	if highlight_delay > 0:		
		highlight_module(view, 'variables', cssvariables.highlights(view))
		highlight_module(view, 'nesting', cssnesting.highlights(view))
		callback = lambda: unhighlight(view)
		sublime.set_timeout(callback, highlight_delay)

def highlight_module(view, name, regions):
	colour = get_setting(name + '_highlight_scope', str)
	outline = get_setting(name + '_highlight_outline', bool)
	if sys.version_info < (3, 0):
		view.add_regions('css-less-ish-'+name, regions, colour, sublime.DRAW_OUTLINED if outline else sublime.DRAW_EMPTY)
	else:
		view.add_regions('css-less-ish-'+name, regions, colour, '', sublime.DRAW_NO_FILL if outline else sublime.DRAW_NO_OUTLINE)
		
def unhighlight(view):
	view.erase_regions('css-less-ish-variables')
	view.erase_regions('css-less-ish-nesting')
	mark_as_finished()

def get_setting(name, typeof=str):
	settings = sublime.load_settings('csslessish.sublime-settings')
	setting = settings.get(name)
	if setting:
		if typeof == str:
			return setting
		if typeof == bool:
			return setting == True
		elif typeof == int:
			return int(settings.get(name, 500))
	else:
		if typeof == str:
			return ''
		else:
			return None

def save_setting(name, value):
	settings = sublime.load_settings('csslessish.sublime-settings')
	settings.set(name, value)

def reload_modules():
	if sys.version_info < (3, 0):
	 	pass
	else:
	 	return
	load_module('modules.cssvariables')
	load_module('modules.cssnesting')
	load_module('modules.csscolours')
	load_module('modules.cssfuncs')
	load_module('tests')
	load_module('tests.testcase')
	load_module('tests.testvariables')
	load_module('tests.testnesting')
	load_module('tests.testcolours')
	load_module('tests.testfuncs')

# reload module (borrowed from sublimelint for ease when debugging)
basedir = os.getcwd()
def load_module(path):
	os.chdir(basedir)
	print("--Reloading "+path)
	__import__(path)
	sys.modules[path] = reload(sys.modules[path])

#
# Hooks
#

class cssvariables_plugin(sublime_plugin.EventListener):
	def on_load(self, view):
		process(view, 'restore')		
	def on_pre_save(self, view):
		view.set_status('css-compile', 'Compiling css(ish)...')
		process(view, 'strip')		
	def on_post_save(self, view):
		process(view, 'restore')
		view.erase_status('css-compile')
	def on_modified(self, view):
		if is_finished():
			view.set_scratch(False) # display as non-scratch view

def process(view, type):
	filename = view.file_name()
	if filename and filename.endswith('.css'):
		# Only process if there are variables or nestings
		if not view.find("@\w+", 0) and not view.find("\w+\s*\[", 0):
			return
		# Handle the buffer scratching
		mark_as_running()
		view.set_scratch(True)
		if type=='restore':
			restore_delay = get_setting('restore_delay', int)
			if restore_delay and restore_delay > 0:
				callback = lambda: restore(view)
				sublime.set_timeout(callback, restore_delay)
			else:
				restore(view)
		else:
			view.run_command('css_less_ish_compile')
			

def restore(view):
	view.run_command('css_less_ish_decompile')