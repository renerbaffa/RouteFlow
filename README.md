# RouteFlow with Database in cluster mode

- Introduction
- What's new
- Installation
- Known Issues or Bugs
- Licensing/legal
- Feedback


# Introduction
This is a version of RouteFlow project managed by CPqD with better support to scalability through a DB in cluster mode. RouteFlow is an open source project to provide virtualized IP routing services over OpenFlow enabled hardware.

Minimum Requirements: 
* CouchBase 2.0.1 or newer

Recommended Requirements:
* CouchBase 2.0.1

Source: https://github.com/renerbaffa/RouteFlow


# What's New

This release sees some significant advances in the RouteFlow project. 
Notable changes are:

- Couchbase as new DBMS.
- Support for use RouteFlow with the BD in cluster mode.
- Improved scalability of RouteFlow.


# Installation

## Manual Installation

1. Download and install Couchbase Server <http://www.couchbase.com/download> on main server. 

2. Start Couchbase Server, create a bucket with desired configurations.

3. Install Couchbase Server on others servers and choose [Join Cluster Now]. Set the following data: [user], [password] and [host ip address]. If you have any questions, you can follow this manual: <http://www.couchbase.com/docs/couchbase-manual-1.8/couchbase-getting-started-setup.html>

4. Access Couchbase’s administration, go to [Server Nodes] and click [Rebalance] to optimize all servers. More information are available in: <<http://www.couchbase.com/docs/couchbase-manual-2.0/couchbase-admin-tasks-addremove-rebalance.html>>

5. Setup the file [***] with following data: ip host, with the list of all servers in cluster mode.


## Auto Installation

1. Run script [couchbase-server.sh] to install Couchbase server. 

2. Run script [couchbase-dev.sh] to install Development libraries.


# Known Issues or Bugs




# Licensing/Legal

This version is released under the Apache License, Version 2.0.
The License can be found here: http://www.apache.org/licenses/LICENSE-2.0


# Feedback

If you find a problem, obsolete or improper code or such, please let us know by contacting us.
Suggestions and corrections are welcome.  Below are contacts of the authors of this project.

- Danilo Pinto da Silva ( *danilo.silva (at) dc.ufscar.br* )
- Denis Wilson de Souza Oliveira ( *denis.oliveira (at) dc.ufscar.br* )
- Eloisa Cristina Silva Santos ( *eloisa.santos (at) dc.ufscar.br* )
- Rener Baffa da Silva ( *rener.silva (at) dc.ufscar.br* )
- Vinícius Afonso Raimundo Ferreira ( *vinicius.ferreira (at) dc.ufscar.br* )
