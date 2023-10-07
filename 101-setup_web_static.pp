# Ensure Nginx is installed
package { 'nginx':
    ensure => installed,
}

# Create the /data/ folder
file { '/data':
    ensure  => directory,
    recurse => true,
}

# Create the folder /data/web_static/ if it doesn’t already exist
file { '/data/web_static':
    ensure  => directory,
    recurse => true,
}

# Create the folder /data/web_static/releases/ if it doesn’t already exist
file { '/data/web_static/releases':
    ensure  => directory,
    recurse => true,
}

# Create the folder /data/web_static/shared/ if it doesn’t already exist
file { '/data/web_static/shared':
    ensure  => directory,
    recurse => true,
}

# Create the folder /data/web_static/releases/test/ if it doesn’t already exi
file { '/data/web_static/releases/test':
    ensure  => directory,
    recurse => true,
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

# Update Nginx configuration to serve the content
file_line { 'my_web_page':
    ensure => present,
    path   => '/etc/nginx/sites-available/default',
    line   => "
        location /hbnb_static {
		alias /data/web_static/current;
                index index.html index.htm;
	}",
    after  => 'add_header',
    notify => Exec['nginx restart'],
}

# Ensure Nginx service is running and configured
exec { 'nginx restart':
    path        => '/etc/init.d/',
    refreshonly => true,  # Only trigger the exec if notified
    subscribe   => File['/etc/nginx/sites-available/default'],  # Replace with an appropriate file or resource
}

# Notify the service to restart when the Nginx config changes
file { '/etc/nginx/sites-available/default':
    notify => Exec['nginx restart'],
}
