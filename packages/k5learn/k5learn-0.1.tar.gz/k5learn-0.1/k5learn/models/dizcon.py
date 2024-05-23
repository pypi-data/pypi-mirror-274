def dizcon():


    print("""
    
    DISCUZ_CONTAINERIZATION

# Install Docker
curl -fsSL get.docker.com -o get-docker.sh
ls
bash get-docker.sh
systemctl start docker
docker version

# Compile a Dockerfile. 
In the Discuz installation directory, create a Dockerfile and write the Discuz installation
procedure into a Dockerfile based on the Docker compilation specifications. The following
is an example: 

FROM centos:7.6.1810
RUN yum install -y httpd php php-fpm php-server php-mysql
COPY ./DiscuzENGUTF8.zip /root/
RUN yum -y install zip unzip && unzip /root/DiscuzENGUTF8.zip
COPY DiscuzENGUTF8 /var/www/html/
RUN chmod -R 777 /var/www/html
ADD httpd-foreground /httpd-foreground
RUN chmod -v +x /httpd-foreground
CMD ["/httpd-foreground"]


####httpd-foreground is the script used to start the httpd service upon system startup.
In Docker, systemctl cannot be used to start services


#!/bin/bash
set -e
rm -f /usr/local/apache2/logs/httpd.pid
exec httpd -DFOREGROUND


#Create an image.
Ensure that the following files are in the same directory
chmod +x httpd-foreground
ll


docker build -t dis11 .


#### 
Wait until the image is created. If the image fails to be created, make modifications as
prompted.
Run the docker images command to view the created image
    
    """)