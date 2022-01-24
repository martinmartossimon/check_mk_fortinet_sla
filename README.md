# check_mk_fortinet_sla
Check_MK pluging for monitoring Fortinet SLAs Parameters: LinkName, LinkState, LinkPacketLoss, LinkLatency


# Metrics collected.
This plugins parses the next OIDs from Fortinet snmp service and configures it on check_mk

sample snmpwalk:
 .1.3.6.1.4.1.12356.101.4.9.2.1.14.X 	LinkName    		LinkName (Str)
 .1.3.6.1.4.1.12356.101.4.9.2.1.4.X 	[0, 1]    		LinkState (int)
 .1.3.6.1.4.1.12356.101.4.9.2.1.9.X 	1.000 - 100.000 	LinkPacketLoss (Percent)
 .1.3.6.1.4.1.12356.101.4.9.2.1.5.X    0.000 - 123.251		LinkLatency (ms)


You can configure throught WATO paramas like:
Example of default params discovery:
{
        'warning_upper': 150,  #Latency Warning
        'critical_upper': 200, #Latency Critical
        'packet_loss': 5, #Max PacketLoss Percentage
}

# Screenshoots:
![Services](https://github.com/martinmartossimon/check_mk_fortinet_sla/blob/main/images/services_view.png)
![WATO](https://github.com/martinmartossimon/check_mk_fortinet_sla/blob/main/images/wato_setup.png)
![graphs](https://github.com/martinmartossimon/check_mk_fortinet_sla/blob/main/images/graphs.png)
