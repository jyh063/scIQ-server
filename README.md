# scIQ-Server

Steps to make updates:

1. ssh to the remote server: 

    ssh -i "*********-server-kpn.pem" ec2-user@************.us-west-1.compute.amazonaws.com
    
2. upload the most recent code by scp or git pull

3. Copy the latest source files to the ~/flask/ directory

4. go to ~/flask/ directory:

    cd ~/flask/

5. enter the virtual environment:

    . venv/bin/activate
    
6. stop the currently running app in supervisor:

    supervisorctl stop flask_app
    
7. restart the app:

    supervisorctl start flask_app


Other actions:

- Stop Nginx Server:

    sudo service nginx stop

- Start Nginx Server:

    sudo service nginx start
    
 - Start supervisor:
 
    cd ~/flask/
    
    . venv/bin/activate
    
    supervisord -c supervisord.conf
    
 - Stop Elasticsearch
 
    sudo service elasticsearch stop
    
 - Start Elasticsearch
 
    sudo service elasticsearch start
