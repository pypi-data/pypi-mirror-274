def logaom():


    print("""
    
    LOG COLLECTION ON AOM

When a host system is abnormal, its logs will contain many errors. To identify an
exception in a timely manner, you can use AOM to count the number of errors in logs
and set alarm rules.


Step 1: In the navigation pane, choose Log > Log Dumps. Then, click Add Log Dump in the
upper right corner

Step 2 Add a log dump:
 Dump File Format: Custom file
 Dump Mode: Periodic dump
 Log Type: System
 Cluster Name: Custom Cluster
 Host: 192.168.3.219 (private IP address of the test ECS)
 Log Group: syslog
 Target OBS Bucket: test-aom-hcip (created during preparation) 


    
    """)