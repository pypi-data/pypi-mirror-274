def liblib():


    print("""
    
OA INSTALLATION


yum install java-1.8.0-openjdk.x86_64 -y
yum install java-1.8.0-openjdk-devel.x86_64 -y


java -version


mkdir /usr/local/maven && cd /usr/local/maven


wget https://ligj008.obs.cn-southwest-2.myhuaweicloud.com/apache-maven-3.6.3-bin.tar.gz


tar -zxvf apache-maven-3.6.3-bin.tar.gz



vim /etc/profile



MAVEN_HOME=/usr/local/maven/apache-maven-3.6.3
export PATH=$PATH:$MAVEN_HOME/bin
export MAVEN_HOME


source /etc/profile


mvn -v 


rpm -e --nodeps mariadb-libs-5.5.68-1.el7.x86_64

rpm -ivh http://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm


yum -y install mysql-server --nogpgcheck

systemctl start mysqld.service


cat /var/log/mysqld.log | grep password


mysql -uroot -pyG3fLX?lcYqG


ALTER USER 'root'@'localhost' IDENTIFIED BY 'Huawei@2024';

grant all privileges on *.* to 'root'@'%' identified by 'Huawei@2024';

flush privileges;

create database oasys;

show databases;


cd /root
yum install git -y


git clone https://gitee.com/nanchengfeinan/oa_system.git


mysql -uroot -pHuawei@2024

USE oasys;

source /root/oa_system/oasys.sql;

show tables;

vim /root/oa_system/src/main/resources/application.properties


mkdir /root/file
mkdir /root/images
mkdir /root/attachment


cp /root/oa_system/static/image/oasys.jpg /root/images/


ll -r /root


cd /root/oa_system

mvn install

java -jar target/oasys.jar





######AUTOMATIC MOUNTING

yum install nfs-utils

8d828423-c9c5-442a-9127-639f0efd66dc.sfsturbo.internal:/      /root/file    nfs   vers=3,nolock    0 0




AS POLICY
for i in seq 1 4; do cat /dev/urandom | md5sum & done



vim /etc/init.d/oasys.sh

#######Script file##########


#!/bin/bash
sleep 10
nohup java -jar /root/oa_system/target/oasys.jar >> /var/log/oasys.log 2>&1 &


cp /etc/rc.d/rc.local /etc/rc.d/rc.local.bp
echo "/etc/rc.d/init.d/oasys.sh" >> /etc/rc.d/rc.local
chmod 755 /etc/rc.d/rc.local
chmod +x /etc/init.d/oasys.sh


reboot


tail -f /var/log/oasys.log


#######Containerizing the OA System#####
yum install docker -y
systemctl start docker; systemctl enable docker
mkdir oa_build
cd oa_build
cp /root/oa_system/target/oasys.jar /root/oa_build
chmod 777 oasys.jar


vim oa_run.sh

#########Script######
#!/bin/bash
nohup java -jar /usr/local/oasys.jar >/var/log/oasys.log 2>&1 &
while true; do
	sleep 1
done



chmod +x oa_run.sh


#####Dockerfile ##############


FROM docker.io/adoptopenjdk/openjdk8:latest
WORKDIR /root
COPY oasys.jar /usr/local/oasys.jar
RUN mkdir /root/file /root/images /root/attachment
COPY oa_run.sh /usr/local/oa_run.sh
CMD ["sh","/usr/local/oa_run.sh"]
    
    """)