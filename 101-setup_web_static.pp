# Define a class for the web server setup
class web_static {
  
  # Ensure the nginx package is installed and the service is running
  package { 'nginx':
    ensure => installed,
    before => Service['nginx'],
  }

  service { 'nginx':
    ensure => running,
    enable => true,
  }

  # Ensure the directories are created
  file { '/data':
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755',
  }

  file { '/data/web_static':
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755',
    require => File['/data'],
  }

  file { '/data/web_static/shared':
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755',
    require => File['/data/web_static'],
  }

  file { '/data/web_static/releases':
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755',
    require => File['/data/web_static'],
  }

  file { '/data/web_static/releases/test':
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755',
    require => File['/data/web_static/releases'],
  }

  # Create the index.html file with the specified content
  file { '/data/web_static/releases/test/index.html':
    ensure  => file,
    content => 'Holberton School',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    mode    => '0644',
    require => File['/data/web_static/releases/test'],
  }

  # Create a symbolic link
  file { '/data/web_static/current':
    ensure => link,
    target => '/data/web_static/releases/test',
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755',
    require => File['/data/web_static/releases/test/index.html'],
  }

  # Update the Nginx configuration
  file_line { 'nginx_hbnb_static':
    path  => '/etc/nginx/sites-available/default',
    line  => 'location /hbnb_static { alias /data/web_static/current/; }',
    after => 'server_name _;',
    require => Package['nginx'],
    notify => Service['nginx'],
  }
}

# Include the web_static class to apply the configuration
include web_static

