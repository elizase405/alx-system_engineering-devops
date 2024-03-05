# setup ssh config file to allow for connecting to server without password

file {'/etc/ssh/ssh_config':
ensure   => present,
content   => "PasswordAuthentication no\nIdentityFile ~/.ssh/school",
}
