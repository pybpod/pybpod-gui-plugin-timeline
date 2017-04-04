# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from pysettings import conf

if conf.PYFORMS_USE_QT5:
	from PyQt5.QtGui import QIcon
else:
	from PyQt4.QtGui import QIcon

from pyforms.gui.Controls import ControlTree

from pybpodgui_plugin_timeline.trials_plot_window import TrialsPlotWindow

logger = logging.getLogger(__name__)


class SessionTreeNode(object):
	def create_treenode(self, tree):
		"""

		:param ControlTree tree: project tree

		:return: this session tree node
		"""
		node = super(SessionTreeNode, self).create_treenode(tree)
		tree.add_popup_menu_option('Bars graph', self.__open_trials_plot_plugin, item=self.node,
		                           icon=QIcon(conf.TIMELINE_PLUGIN_ICON))
		return node

	def __open_trials_plot_plugin(self):
		if not hasattr(self, 'trials_plugin'):
			self.trials_plugin = TrialsPlotWindow(self)
			self.trials_plugin.show()
			self.trials_plugin.subwindow.resize(*conf.TIMELINE_PLUGIN_WINDOW_SIZE)
		else:
			self.trials_plugin.show()

	def node_double_clicked_event(self):
		super(SessionTreeNode, self).node_double_clicked_event()
		self.__open_trials_plot_plugin()

	def remove(self):
		if hasattr(self, 'trials_plugin'): self.mainwindow.mdi_area -= self.trials_plugin
		super(SessionTreeNode, self).remove()

	@property
	def name(self):
		return super(SessionTreeNode, self.__class__).name.fget(self)

	@name.setter
	def name(self, value):
		super(SessionTreeNode, self.__class__).name.fset(self, value)
		if hasattr(self, 'trials_plugin'): self.trials_plugin.title = value
