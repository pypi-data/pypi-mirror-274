def appscript():


    print("""
    
    APPLICATION STARTUP SCRIPT SAMPLE

#!bin/bash
export JAVA_HOME=/usr/lib/jvm/java-1.8.0.382.b05-1.el7_9.x86_64/jre/bin
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH


sleep 10
nohup java -jar /root/IMSystem/target/demo-0.0.1-SNAPSHOT.jar >> /var/log/application.log
&
    
    """)