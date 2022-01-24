# -*- coding: utf-8 -*-
#
# License: GNU General Public License v2
#
# Author: martinmartossimon@gmail.com
# URL   : 
# Date  : 2022-01-19
#
# Monitor status of Fortinet SLAs

from cmk.gui.valuespec import (
    Dictionary,
    Integer,
    TextAscii,
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersOperatingSystem,
)

def _item_valuespec_SLA():
    return TextAscii(title=_("LinkLatency and LinkPacketLoss"))


def _parameter_valuespec_SLA():
    return Dictionary(
        elements=[
            ("warning_upper", Integer(title=_("Warning -> if latency over (>=) (ms):"))),
            ("critical_upper", Integer(title=_("Critical -> if latency over (>=) (ms):"))),
            ("packet_loss", Integer(title=_(" Max packet loss  percentage (>=) [0-100]%:"))),
        ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="sla_fortinet",
        group=RulespecGroupCheckParametersOperatingSystem,
        match_type="dict",
        item_spec=_item_valuespec_SLA,
        parameter_valuespec=_parameter_valuespec_SLA,
        title=lambda: _("LinkLatency and LinkPacketLoss"),
    ))
