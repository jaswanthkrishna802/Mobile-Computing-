# Evidence Summary — Assignment 3

## Q1: Wireless mobility
`results/q1_handoff_trace.csv` records signal-strength samples for AP1 and AP2 and shows the active access point changing from AP1 to AP2 when the handoff condition is met.

## Q2: Mobile IP
`results/q2_mobile_ip_trace.txt` records a worked registration and packet-tunnelling example. It shows a Home Agent binding a home address to a Care-of Address and forwarding an encapsulated packet.

## Q5: DSDV-style routing
`results/q5_dsdv_trace.txt` shows a route-table update after a link failure. The receiving node accepts a route advertisement with a newer destination sequence number.

## Q6: AODV-style routing
`results/q6_aodv_trace.txt` shows an RREQ being forwarded through intermediate nodes, an RREP returning along the reverse path, and a route being installed.

## Q7: Emergency network performance
`results/q7_performance.csv` contains illustrative scenario rows and calculated Packet Delivery Ratio and Routing Overhead Ratio. The data demonstrates the calculations only; it is not output from a packet-level simulator or physical experiment.

## Reproducibility
Run `python run_all.py` from the repository root to regenerate the output files.
