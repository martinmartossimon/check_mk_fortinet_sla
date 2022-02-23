#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: GNU General Public License v2
#
# Author: martinmartossimon@gmail.com
# URL   : 
# Date  : 2022-01-19
#
# Monitor status of Fortinet SLAs
#
#
# sample snmpwalk:
# .1.3.6.1.4.1.12356.101.4.9.2.1.14.X 	CL-AWS-01    		LinkName (Str)
# .1.3.6.1.4.1.12356.101.4.9.2.1.4.X 	[0, 1]    		LinkState (int)
# .1.3.6.1.4.1.12356.101.4.9.2.1.9.X 	1.000 - 100.000 	LinkPacketLoss (Percent)
# .1.3.6.1.4.1.12356.101.4.9.2.1.5.X    0.000 - 123.251		LinkLatency (ms)

import datetime
from dataclasses import dataclass
from typing import Optional

from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    register,
    Service,
    Result,
    State,
    SNMPTree,
    exists,
    Metric,
    OIDEnd,
)
from cmk.base.plugins.agent_based.agent_based_api.v1.type_defs import (
    DiscoveryResult,
    CheckResult,
    StringTable,
)


@dataclass
class Sla_Fortinet:
    LinkName: str
    LinkState: int
    LinkPacketLoss: float
    LinkLatency: float


@dataclass
class Sla_Fortinet_List:
    ListaEnlaces: Sla_Fortinet

def parse_Sla(string_table: StringTable) -> Optional[Sla_Fortinet_List]:
    listaRetorno = []
    for registro in string_table:
        LinkName, LinkState, LinkLatency, LinkPacketLoss = registro
        listaRetorno.append(Sla_Fortinet(LinkName=LinkName, LinkState=int(LinkState), LinkPacketLoss=float(LinkPacketLoss), LinkLatency=float(LinkLatency)))
    return listaRetorno

def discovery_Sla_Fortinet(section):
    for service in section:
        yield Service(item=service.LinkName,parameters={
            'warning_upper': 150,
            'critical_upper': 200,
            'packet_loss': 5,
    })


def check_Sla_Fortinet(item, params, section):
    now = datetime.datetime.now()
    if section:
        for item2 in section:
            if item == item2.LinkName:
                latenciaWarning=params.get('warning_upper', None)
                latenciaCritical=params.get('critical_upper', None)
                umbralLinkPacketLoss=params.get('packet_loss', None)
                if item2.LinkState == 0:
                    yield Metric("LinkState", int(item2.LinkState))
                    yield Metric("LinkLatency", float(item2.LinkLatency), levels=(latenciaWarning,latenciaCritical))
                    yield Metric("LinkPacketLoss", float(item2.LinkPacketLoss), levels=(0,umbralLinkPacketLoss))
                    if item2.LinkLatency >= latenciaCritical:
                        yield Result(state=State.CRIT, summary='SLA Service %s is up. LinkState: %s Latency: %s (!!) LinkPacketLoss: %s Checked: %s' % (item2.LinkName, item2.LinkState, item2.LinkLatency, item2.LinkPacketLoss, now))
                    else:
                        if item2.LinkLatency >= latenciaWarning:
                            if item2.LinkPacketLoss >= umbralLinkPacketLoss:
                                yield Result(state=State.CRIT, summary='SLA Service %s is up. LinkState: %s Latency: %s (!) LinkPacketLoss: %s (!!) Checked: %s' % (item2.LinkName, item2.LinkState, item2.LinkLatency, item2.LinkPacketLoss, now))
                            else:
                                yield Result(state=State.WARN, summary='SLA Service %s is up. LinkState: %s Latency: %s (!) LinkPacketLoss: %s Checked: %s' % (item2.LinkName, item2.LinkState, item2.LinkLatency, item2.LinkPacketLoss, now))
                        else:
                            if item2.LinkPacketLoss >= umbralLinkPacketLoss:
                                yield Result(state=State.CRIT, summary='SLA Service %s is up. LinkState: %s Latency: %s LinkPacketLoss: %s (!!) Checked: %s' % (item2.LinkName, item2.LinkState, item2.LinkLatency, item2.LinkPacketLoss, now))
                            else:
                                yield Result(state=State.OK, summary='SLA Service %s is up. LinkState: %s Latency: %s LinkPacketLoss: %s Checked: %s' % (item2.LinkName, item2.LinkState, item2.LinkLatency, item2.LinkPacketLoss, now))
                else:
                    yield Result(state=State.CRIT, summary='SLA Service %s is down (!!). LinkState: %s Latency: %s LinkPacketLoss: %s Checked: %s' % (item2.LinkName, item2.LinkState, item2.LinkLatency, item2.LinkPacketLoss,now))
    else:
        yield Result(state=State.UNKN, summary='No metrics collectect on last check: %s' % (now))
    
register.snmp_section(
	name = "sla_fortinet",
	detect = exists(".1.3.6.1.4.1.12356.101.4.9.2.1.*"),
	fetch = SNMPTree(
	        base = '.1.3.6.1.4.1.12356.101.4.9.2.1',
		oids = [
			"14", #LinkName
			"4", #LinkState
			"5", #LinkLatency
			"9", #LinkPacketLoss
		],
	),
	parse_function=parse_Sla,
)

register.check_plugin(
    name='sla_fortinet',
    service_name='SLAv2_%s',
    discovery_function=discovery_Sla_Fortinet,
    check_function=check_Sla_Fortinet,
    check_ruleset_name='sla_fortinet',
    check_default_parameters={
        'warning_upper': 150,
        'critical_upper': 200,
        'packet_loss': 5,
    },
)
