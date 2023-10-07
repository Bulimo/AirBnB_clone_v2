# Ensure Nginx is installed
package { 'nginx':
    ensure => installed,
}

# Create the /data/ folder
file { '/data':
    ensure  => directory,
    owner   => 'ubuntu',
    group   => 'ubuntu',
    recurse => true,
}

# Create the folder /data/web_static/ if it doesn’t already exist
file { '/data/web_static':
    ensure  => directory,
    owner   => 'ubuntu',
    group   => 'ubuntu',
    recurse => true,
}

# Create the folder /data/web_static/releases/ if it doesn’t already exist
file { '/data/web_static/releases':
    ensure  => directory,
    owner   => 'ubuntu',
    group   => 'ubuntu',
    recurse => true,
}

# Create the folder /data/web_static/shared/ if it doesn’t already exist
file { '/data/web_static/shared':
    ensure  => directory,
    owner   => 'ubuntu',
    group   => 'ubuntu',
    recurse => true,
}

# Create the folder /data/web_static/releases/test/ if it doesn’t already exi
file { '/data/web_static/releases/test':
    ensure  => directory,
    owner   => 'ubuntu',
    group   => 'ubuntu',
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
    owner   => 'ubuntu',
    group   => 'ubuntu',
}

# Ensure the symbolic link is created
file { '/data/web_static/current':
    ensure => link,
    target => '/data/web_static/releases/test',
    owner  => 'ubuntu',
    group  => 'ubuntu',
}

# Update Nginx configuration to serve the content
file_line { 'my_web_page':
    ensure => present,
    path   => '/etc/nginx/sites-available/default',
    line   => "
        location /hbnb_static {
		alias /data/web_static/current/;
	}",
    after  => 'add_header',
    notify => Service['nginx'],
}

# Ensure Nginx service is running and configured
service { 'nginx':
    ensure  => running,
    enable  => true,
    require => [Package['nginx'], File['/etc/nginx/sites-available/default']],
}

# Notify the service to restart when the Nginx config changes
file { '/etc/nginx/sites-available/default':
    notify => Service['nginx'],
}
