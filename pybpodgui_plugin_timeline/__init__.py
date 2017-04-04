# !/usr/bin/python3
# -*- coding: utf-8 -*-

__version__ = "1.0.0"
__author__ = "Carlos Mão de Ferro"
__credits__ = ["Carlos Mão de Ferro", "Ricardo Ribeiro"]
__license__ = "Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>"
__maintainer__ = ["Carlos Mão de Ferro", "Ricardo Ribeiro"]
__email__ = ["cajomferro@gmail.com", "ricardojvr@gmail.com"]
__status__ = "Development"

from pysettings import conf;

conf += 'pybpodgui_plugin_timeline.settings'

from pybpodgui_plugin_timeline.trials_plot_window import TrialsPlotWindow as TrialsPlot
