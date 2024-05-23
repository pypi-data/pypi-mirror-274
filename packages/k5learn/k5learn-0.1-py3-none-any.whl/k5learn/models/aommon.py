def aommon():


    print("""
    
    AOM MONITORING


#Install UniAgent
Log in to the AOM 2.0 console.

On the menu bar, choose Collection Management.

In the navigation tree on the left, choose UniAgent > VM Access. On the displayed page, click Install UniAgent . Then, choose Manual.


#INSTALL APPLICATION 
Log in to the ECS, run the following command to install JRE, and press Enter:

yum -y install jre


Run the following command to install the vmall application, enter the command, and press Enter:

mkdir -p /root/testdemo
cd /root/testdemo
curl -l http://demos.obs.myhwclouds.com/demo_install.sh > demo_install.sh && bash demo_install.sh



Run the following command to start the application, enter the command, and press Enter:
bash start_apminside.sh


Run the following command to check whether the process is started:
ps -ef |grep java



#HOW TO ACCESS YOUR APPLICATION ON APM

Go to the APM 2.0 console. 
Click Using Application Performance Management.

Click System Management > Access Keys. Record AK/SK.

We will use them in the next step.


######  Install JavaAgent
On the AOM 2.0 console.

Link

Click Monitoring Center > Access Center > Java.



After installation on the server


Modify the parameters in the start.sh script to ensure that the application is monitored by the APM.

Enter the following command and press Enter to open the start.sh file:
vim start.sh


Add the following four lines of code to the location shown in the following figure:


-javaagent:/root/testdemo/apm-javaagent/apm-javaagent.jar=appName=vmall-dao-service,business=vmall1
-javaagent:/root/testdemo/apm-javaagent/apm-javaagent.jar=appName=vmall-apigw-service,business=vmall1
-javaagent:/root/testdemo/apm-javaagent/apm-javaagent.jar=appName=vmall-user-service,business=vmall1
-javaagent:/root/testdemo/apm-javaagent/apm-javaagent.jar=appName=vmall-product-service,business=vmall1


START APPLICATION
./start.sh

check whether the application is started
ps -ef|grep java


Return to the AOM console and refresh the page. As shown in the following figure, the four sub-services of the Vmall store have been associated with the Vmall.


Add Dashboard
Click Monitoring Center and Add Dashboard.

Dashboard name: vmall
bind to application: vmall1
add group: vmall

#Add Graph
Graph name: CPU Status

Metric Name

Host/Infrastructure > aom_node_cpu_usage
scope: hostname: "ecs-vmall"

Click Add to Dashboard 




Adding Another Graph to AOM Dashboard
Click Add Graph


Set the Graph Name to Component Status. and click System Graphs > Component Status.


Select the application, select the four components under the application, and click to switch to the graph mode.

Click Add to Dashboard
Click Save
    
    """)