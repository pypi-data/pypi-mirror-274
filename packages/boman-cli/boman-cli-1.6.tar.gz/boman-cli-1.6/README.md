# Introduction 
Boman CLI is a Orchestration script written in python to run security scans on the customer's local or CI/CD environment and upload the results to Boman.ai SaaS server.


# Installation

` pip install boman-cli`

# Getting Started

###  For help

` boman-cli -h` 

### To test the boman cli server

` boman-cli -a test-saas`


### To test the boman configuration written in boman.yaml file

` boman-cli -a test-yaml`

### To run the scan 

` boman-cli -a run`

### To run the scan on specific Boman SaaS URL (On prem)

` boman-cli -a run -u {URL}`


### To fail build on high/medium/low finding is detected

`boman-cli -a run -fb {severity}`

Severity can be high, medium or low.

Example: boman-cli -a run -fb high


### To custom change the boman.yaml file, pass the custom file name as input for -config argument

`boman-cli -a run -config <custom_boman_yaml_file_name_here>`

Example: boman-cli -a run -config ./customboman.yaml


### To inject custom zap auth session script file, pass the custom file name as input for -zap_session_script argument

`boman-cli -a run -zap_session_script <custom_session_script_file_name_here>`

Example: boman-cli -a run -zap_session_script ./session.js




# Error codes & meannings

0  : Successfull scan
1  : Server/SaaS error
2  : Auth error
3  : Docker/System error
4  : Misconfig error




### Release Note:


### V1.6:

    - Zap Authenticated scan 
    - Fetch Git details
    - custom boman.yaml and zap session script load option

Released on: 20 May 2024




