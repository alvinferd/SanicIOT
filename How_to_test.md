# Konfigurasi testing server
## Instalasi dan konfigurasi
$ apt install siege -y
$ curl http://128.199.179.194:6969/dump.sql -o dump.sql
$ nano /root/.siege/siege.conf 		#set limit = 1023
$ ulimit -n 10000
$ echo 1024 65535 > /proc/sys/net/ipv4/ip_local_port_range
$ sudo apt install postgresql postgresql-contrib -y
$ apt install httpie -y


## Running siege
$ screen -R run_siege 		#(Ctrl+A+D for minimize terminal window, screen -x run_siege for accessing back, only need to create the screen once)
##Run the script and save output to file:
	- $ ./siege.sh 2>&1 | tee sanicbasicauth_res.txt
	- (Optional) : Ctrl+a+d to back to the main terminal window.
	- # After running the script we can close our connection to the SSH and the backscreen will keep running on the background
Repeat order for every need.


# Konfigurasi apps server sanic
## Instalasi
$ curl http://128.199.179.194:6969/dump.sql -o dump.sql
$ ulimit -n 10000
$ apt install python3-pip -y
$ pip3 install sanic
$ pip3 install asyncpg
$ git clone https://github.com/alvinferd/SanicIOT.git
$ sudo apt install postgresql postgresql-contrib -y
$ sudo systemctl start postgresql.service


### change password postgres
$ sudo -i -u postgres
$ psql
\password postgres; -> ganti pass
exit #2 times back to root user

### Change postgre config
$ find / -name "pg_hba.conf" ## ex : /etc/postgresql/14/main/pg_hba.conf
$ nano /etc/postgresql/14/main/pg_hba.conf
tambahin di akhir baris :
```
host    all             all              0.0.0.0/0                       md5
host    all             all              ::/0                            md5
```
##Dan edit peer jadi md5 di localhost connection
$ find / -name "postgresql.conf" ## ex : /etc/postgresql/14/main/postgresql.conf
$ nano /etc/postgresql/14/main/postgresql.conf	##listen_addresses = 'localhost' -> listen_addresses = '*'
$ sudo service postgresql restart


### Set up database
$ psql -U postgres -d postgres -f dump.sql
$ sudo service postgresql restart


## Running apps
Create back screen terminal :
	$ screen -R run_sanic 		#(Ctrl+A+D for minimize terminal window, screen -x run_sanic for accessing back,only need to create the screen once)
Run the server application :
	$ python3 server.py
	- (Optional) : Ctrl+a+d to back to the main terminal window.
	# After running the application we can close our connection to the SSH and the backscreen will keep running on the background