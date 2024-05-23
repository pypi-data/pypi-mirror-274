def opcart():

    print("""
    
    OPENCART INSTALLATION

# Run the following commands to install the HTTP, PHP, and OpenCart eCommerce
websites:

	yum install -y httpd
	systemctl start httpd
	systemctl enable httpd
	rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
	rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm


# Find the webtatic.repo file and change the file to the image content
	Remove comment form the baseurl and add comment in the mirrorlist

# INSTALL PHP, RESTART HTTPD, DONWLOAD OPENCART, UNZIP, COPY AND GRANT PERMISSION

yum -y install php72w php72w-pdo php72w-mysqlnd php72w-opcache php72w-xml php72w-gd
php72w-mcrypt php72w-devel php72w-intl php72w-mbstring php72w-bcmath php72w-json php72wiconv

systemctl restart httpd

wget https://www.opencart.cn/download/12

unzip 12

cp upload/* /var/www/html/ -rf

chmod -R 777 /var/www/html


    
    """)