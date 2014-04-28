import re
import sublime, sublime_plugin

__author__ = 'johannes82'

# global pattern
# pattern = r'(([0-1][0-9]-[0-3][\d]\s[0-2][0-9]:[0-5][0-9]:[0-5][0-9]\.\d\d\d)(\s*|:)(\d*:\s*\d*\s)(V|I|W|D|E)/($|[^\[$\n]*))'

base_pattern = '^(\[\s)*[0-1][0-9]-[0-3][\d]\s[0-2][0-9]:[0-5][0-9]:[0-5][0-9]\.\d\d\d(\s*|:)\d*:\s*\d*\s'
global info_pattern
info_pattern = r'(' + base_pattern + '(I)/.*[^\n])'
global verbose_pattern
verbose_pattern = r'(' + base_pattern + '(V)/.*[^\n])'
global warning_pattern
warning_pattern = r'(' + base_pattern + '(W)/.*[^\n])'
global debug_pattern
debug_pattern = r'(' + base_pattern + '(D)/.*[^\n])'
global error_pattern
error_pattern = r'(' + base_pattern + '(E)/.+[^\n])'
global myspin_pattern
myspin_pattern = r'(' + base_pattern + '(.{1})/MySpin.+[^\n])'


def plugin_loaded():
	print ('AndLog plugin loaded.')
	global Pref
	Pref = Pref()
	Pref.load()


class Pref:
	def load(self):
		settings = sublime.load_settings('AndLog.sublime-settings')
		Pref.highlighting_info   = settings.get('highlighting_info', False)
		Pref.highlighting_verbose   = settings.get('highlighting_verbose', False)
		Pref.highlighting_warning   = settings.get('highlighting_warning', False)
		Pref.highlighting_debug   = settings.get('highlighting_debug', True)
		Pref.highlighting_error   = settings.get('highlighting_error', True)
		Pref.highlighting_myspin   = settings.get('highlighting_myspin', True)
		Pref.highlighted         = False
		Pref.color_scope_info    = settings.get('color_scope_info', "comment")
		Pref.color_scope_verbose = settings.get('color_scope_verbose', "support.type.exception")
		Pref.color_scope_warning = settings.get('color_scope_warning', "comment")
		Pref.color_scope_debug   = settings.get('color_scope_debug', "string")
		Pref.color_scope_error   = settings.get('color_scope_error', "invalid")


class EnableHighlightingCommand(sublime_plugin.TextCommand):
	"""
	Command for highlighting static logfiles.
	"""
	def run(self, edit):
		global Pref

		if not (Pref.highlighted):
			Pref.highlighted = True
			print ("Highlighting", Pref.highlighted)
			if (Pref.highlighting_info):
				self.highlight_text(self.view, info_pattern, Pref.color_scope_info)
			if (Pref.highlighting_verbose):
				self.highlight_text(self.view, verbose_pattern, Pref.color_scope_verbose)
			if (Pref.highlighting_warning):
				self.highlight_text(self.view, warning_pattern, Pref.color_scope_warning)
			if (Pref.highlighting_debug):
				self.highlight_text(self.view, debug_pattern, Pref.color_scope_debug)
			if (Pref.highlighting_error):
				self.highlight_text(self.view, error_pattern, Pref.color_scope_error)
			if (Pref.highlighting_myspin):
				self.highlight_text(self.view, myspin_pattern, Pref.color_scope_error)
		else:
			Pref.highlighted = False
			print ("Highlighting", Pref.highlighted)
			self.view.erase_regions(info_pattern)
			self.view.erase_regions(verbose_pattern)
			self.view.erase_regions(warning_pattern)
			self.view.erase_regions(debug_pattern)
			self.view.erase_regions(error_pattern)
			self.view.erase_regions(myspin_pattern)


	def highlight_text(self, view, pattern, color):
		print ("Highlighting ", pattern, "with color", color)
		regions = []
		regions += view.find_all(pattern, False)
		key = pattern
		view.add_regions(key, regions, color, "", True)


class StartLiveLoggingCommand(sublime_plugin.TextCommand):
	"""
	Command for live logging endless.
	"""
	def run(self, edit):
		print ("This is not implemented yet.")
