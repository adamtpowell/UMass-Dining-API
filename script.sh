sudo debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password password password'
sudo debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password_again password password'
sudo apt-get -y install mysql-server