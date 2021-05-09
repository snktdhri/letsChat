# letsChat
This is chat application which 
    1. Uses Flask & SocketIO & python3 to provide realtime chat functionality over sockets 
    1. User can join chat rooms by doing GET /chat?username=username&root=room_id
    2. Maintains chat in redis DB and load when user refreshes or joins back
    3. Enable ssh by using lets encrypt & nginx as proxy server


# Run below commands to setup env
# Replace the installation commands as per os flavour, below commands work for rpm based os's
$ sudo yum update -y
$ sudo yum install -y python34
$ sudo yum install python34-devel


$ wget -O /tmp/epel.rpm –nv https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
$ sudo yum install -y /tmp/epel.rpm
$ sudo yum install redis -y --nogpgcheck
$ sudo yum install redis -y
$ sudo service restart nginx
$ sudo yum install nginx -y


#Copy project files under directory you want, lets call it APP_DIR

APP_DIR
    - app.py
    - redis_utils.py
    - requirements.txt
    - restart.sh
    - templates
        - index.html
        - chat.html

# Start the app
$ cd APP_DIR
$ sudo chmod 777 restart.sh
$ ./restart.sh

# Enable ssl
Install ssh key by using lets encrypt
$ wget https://dl.eff.org/certbot-auto
$ chmod a+x ./certbot-auto
$ ./certbot-auto certonly --nginx --debug -d <server.com>

edit config/nginx.conf to replace ssl keys & server name & copy to /etc/nginx/nginx.conf 
$ sudo service restart nginx

# you should be able to start join chat rooms using
for room #root_id_identifier1
https://server.com/chat?username=User1&room=root_id_identifier1 
https://server.com/chat?username=User2&room=root_id_identifier1 


for room #root_id_identifier2
https://server.com/chat?username=User3&room=root_id_identifier2
https://server.com/chat?username=User2&room=root_id_identifier2 

