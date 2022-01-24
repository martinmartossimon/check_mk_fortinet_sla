# -*- coding: utf-8 -*-
#
# License: GNU General Public License v2
#
# Author: martinmartossimon@gmail.com
# URL   : 
# Date  : 2022-01-19
#
# Monitor status of Fortinet SLAs

from cmk.gui.i18n import _

from cmk.gui.plugins.metrics import (
    metric_info,
    graph_info,
    perfometer_info
)


##############################
# Metricas del plugin
##############################

metric_info['LinkLatency'] = {
    'title': _('LinkLatency'),
    'unit': 'count',
    'color': '26/a',
}

metric_info['LinkPacketLoss'] = {
    'title': _('LinkPacketLoss'),
    'unit': 'count',
    'color': '11/a',
}





######################################################################################################################
#
# define perf-o-meter
#
######################################################################################################################

perfometer_info.append(('stacked', [
    {
        'type': 'linear',
        'segments': ['LinkLatency',
                     ],
        'total': 100,
    },
    {
        'type': 'linear',
        'segments': ['LinkPacketLoss',
                     ],
        'total': 500,
    }
]))

