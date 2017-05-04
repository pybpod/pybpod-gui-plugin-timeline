#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" pycontrolgui_plugin_timeline.trials_plot"""

import logging

from pysettings import conf

if conf.PYFORMS_USE_QT5:
	from PyQt5.QtCore import QTimer
else:
	from PyQt4.QtCore import QTimer

from pyforms.Controls import ControlEventsGraph
from pyforms import BaseWidget

from pybpodgui_plugin.com.messaging.state_entry import StateEntry
from pybpodgui_plugin.api.exceptions.run_setup import RunSetupError

logger = logging.getLogger(__name__)


class TrialsPlotWindow(BaseWidget):
	""" Show all boxes live state for an experiment"""

	def __init__(self, session):
		"""
		:param session: session reference
		:type session: pycontrolgui.windows.detail.entities.session_window.SessionWindow
		"""
		BaseWidget.__init__(self, session.name)
		self.session = session
		self._events = ControlEventsGraph(session.name)

		for state_id, state_name in sorted(self.session.setup.board_task.states.items(), key=lambda x: x[0]):
			self._events.add_track(state_name)

		self._history_index = 0
		self._last_event = None

		self._formset = ['_events']

		self._list_of_states_colors = ['#E0E0E0', '#FFCC99', '#FFFF99', 'CCFF99', '#99FFFF', '#99CCFF', '#FF99CC']

		self.read_message_queue()

		self._timer = QTimer()
		self._timer.timeout.connect(self.read_message_queue)

	def show(self):
		# Prevent the call to be recursive because of the mdi_area
		if hasattr(self, '_show_called'):
			BaseWidget.show(self)
			return
		self._show_called = True
		self.mainwindow.mdi_area += self
		del self._show_called

		self._timer.start(conf.TIMELINE_PLUGIN_REFRESH_RATE)

	def hide(self):
		self._timer.stop()

	def beforeClose(self):
		self._timer.stop()
		return False

	def __add_event(self, start_timestamp, end_timestamp, track_id, name):

		self._last_event = self._events.add_event(
			start_timestamp, end_timestamp, track=track_id,
			title=name, color=self._list_of_states_colors[track_id % len(self._list_of_states_colors)]
		)
		self._events.value = start_timestamp

	def read_message_queue(self):
		""" Update board queue and retrieve most recent messages """

		try:
			recent_history = self.session.messages_history[self._history_index:]
			states = self.session.setup.board_task.states

			for message in recent_history:
				if isinstance(message, StateEntry):
					try:
						self.__add_event(int(round(message.start_timestamp * 1000)),
						                 int(round(message.end_timestamp * 1000)),
						                 message.state_id - 1,
						                 message.state_name)
					except ValueError as err:
						logger.warning(str(err))

				self._history_index += 1

		except RunSetupError as err:
			logger.error(str(err), exc_info=True)
			self._timer.stop()

	@property
	def mainwindow(self):
		return self.session.mainwindow

	@property
	def title(self):
		return BaseWidget.title.fget(self)

	@title.setter
	def title(self, value):
		title = 'Trials-plot: {0}'.format(value)
		BaseWidget.title.fset(self, title)
