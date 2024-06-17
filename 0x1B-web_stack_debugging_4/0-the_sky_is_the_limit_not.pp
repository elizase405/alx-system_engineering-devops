 custom resource to ensure a file has specific content
define ensure_content($content) {
  file { $name:
    ensure  => file,
    content => $content,
  }
}

# Apply file descriptor limits for the nginx user
ensure_content { '/etc/security/limits.d/nginx.conf':
  content => @("EOF")
    nginx soft nofile 65536
    nginx hard nofile 65536
    | EOF
}

# Ensure pam_limits.so is included in common-session and common-session-noninteractive
augeas { 'pam_limits_common-session':
  context => '/files/etc/pam.d/common-session',
  changes => 'ins 01 session before last; set 01/session/type required; set 01/session/module pam_limits.so',
  onlyif  => 'match session[. = "required" and module = "pam_limits.so"] size == 0',
  require => File['/etc/security/limits.d/nginx.conf'],
}

augeas { 'pam_limits_common-session-noninteractive':
  context => '/files/etc/pam.d/common-session-noninteractive',
  changes => 'ins 01 session before last; set 01/session/type required; set 01/session/module pam_limits.so',
  onlyif  => 'match session[. = "required" and module = "pam_limits.so"] size == 0',
  require => File['/etc/security/limits.d/nginx.conf'],
}

# Define the correct nginx configuration content
$nginx_conf_content = @("EOF")
user  nginx;
worker_processes  auto;
worker_rlimit_nofile 65536;

events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '\$remote_addr - \$remote_user [\$time_local] "\$request" '
                      '\$status \$body_bytes_sent "\$http_referer" '
                      '"\$http_user_agent" "\$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
| EOF

# Ensure the nginx configuration file has the correct content
ensure_content { '/etc/nginx/nginx.conf':
  content => $nginx_conf_content,
  notify  => Exec['nginx_reload'],
}

# Define the exec resource to reload nginx
exec { 'nginx_reload':
  command     => 'nginx -s reload',
  refreshonly => true,
}

# Ensure the nginx service is running
service { 'nginx':
  ensure     => running,
  enable     => true,
  subscribe  => File['/etc/nginx/nginx.conf'],
  require    => Package['nginx'],
}

# Ensure nginx is installed
package { 'nginx':
  ensure => installed,
}

