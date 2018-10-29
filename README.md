# Log-Analysis
## Table of Contents

* [Instructions](#instructions)
* [Contributing](#contributing)

## Instructions

1. About the project

The project uses python3 and postgresql to implement log analysis tool.


2. Prerequisites

- python3
- VirtualBox 
- Vagrant
- Database `news` to be built inside the virtual machine (VM)
- SQL file `newsdata.sql` to be used in loading data into `news` database

3. How to run the project

- run `vagrant up`
- run `vagrant ssh`
- run `cd /vagrant`
- run `psql -d news -f newsdata.sql` to connect to `news` database and insert data
- run `\q` to quit from sql mode
- run `pip3 install psycopg2` to install psycopg2 module
- run `python3 log_analysis.py` to run the application
- the application should create a new text file inside the shared folder of the VM 


## Contributing

This project is built in the fulfillment of Udacity Full Stack Nano Degree requirement, pull requests will not be merged to this project.

