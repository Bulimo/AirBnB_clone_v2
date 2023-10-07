# define nginx config file
$nginx_config = @(''')
# Default server configuration
#
server {
	listen 80 default_server;
	listen [::]:80 default_server;

	# SSL configuration
	#
	# listen 443 ssl default_server;
	# listen [::]:443 ssl default_server;
	#
	# Note: You should disable gzip for SSL traffic.

	root /var/www/html;

	# Add index.php to the list if you are using PHP
	index index.html index.htm index.nginx-debian.html;

	server_name _;

    add_header X-Served-By 343103-web-02;

    location /hbnb_static {
		alias /data/web_static/current;
        index index.html index.htm;
	}

	location /redirect_me {
		return 301 https://www.youtube.com;
	}

	location / {

		error_page 404 /404.html;
		# First attempt to serve request as file, then
		# as directory, then fall back to displaying a 404.
		try_files $uri $uri/ =404;
	}
}
'''

# Ensure Nginx is installed
package { 'nginx':
    ensure => installed,
}

# Create the /data/ folder
file { '/data':
    ensure  => directory,
}

# Create the folder /data/web_static/ if it doesn’t already exist
file { '/data/web_static':
    ensure  => directory,
}

# Create the folder /data/web_static/releases/ if it doesn’t already exist
file { '/data/web_static/releases':
    ensure  => directory,
}

# Create the folder /data/web_static/shared/ if it doesn’t already exist
file { '/data/web_static/shared':
    ensure  => directory,
}

# Create the folder /data/web_static/releases/test/ if it doesn’t already exi
file { '/data/web_static/releases/test':
    ensure  => directory,
}

# Create a test HTML file
file { '/data/web_static/releases/test/index.html':
    ensure  => file,
    content => "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
",
}

# Ensure the symbolic link is created
file { '/data/web_static/current':
    ensure => link,
    target => '/data/web_static/releases/test',
}

# Set ownership of /data/ directory
exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/',
}

# Create initial default page and error page configs
file { '/var/www':
  ensure => 'directory',
}

file { '/var/www/html':
  ensure => 'directory',
}

# Create default index.html and 404.html pages
file { '/var/www/html/index.html':
  ensure  => file,
  content => "Holberton School\n",
}

file { '/var/www/html/404.html':
  ensure  => file,
  content => "Ceci n'est pas une page\n",
}

# Update Nginx configuration to serve the content
file { '/etc/nginx/sites-available/default':
    ensure  => file,
    content => $nginx_config,
    notify  => Exec['nginx restart'],
}

# Ensure Nginx service is running and configured
exec { 'nginx restart':
    path        => '/etc/init.d/',
    refreshonly => true,  # Only trigger the exec if notified
    subscribe   => File['/etc/nginx/sites-available/default'],  # Replace with an appropriate file or resource
}

