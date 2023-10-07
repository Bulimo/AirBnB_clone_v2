#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

WEB_STATIC="location /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}"

#install nginx if not yet installed
sudo apt-get update > /dev/null 2>&1
sudo apt-get -y install nginx > /dev/null

# Create the folders /data/web_static/ if it doesn’t already exist
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

# Create a fake HTML file /data/web_static/releases/test/index.html
if [ -L "/data/web_static/current" ];
then
    sudo rm -f /data/web_static/current
fi
echo "<html>
    <head>
    </head>
    <body>
        Holberton School
    </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

#Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder. 
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Grant ownership of the /data/ folder to the ubuntu user AND group. This should be recursive
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
sudo sed -i "0,/location/s|location|$WEB_STATIC\n\t&|" /etc/nginx/sites-available/default
# Restart Nginx to apply the changes
sudo service nginx restart > /dev/null
