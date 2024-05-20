def micro():


    print("""
    
    #MICROSERVICE APPLICATION DEPLOYMENT (WEATHER) 

# INSTALLATION STEPS

Deploying a Microservice (Weather)
- Create an AK/SK 
- Create a VPC e.g vpc-servicestage(192.168.0.0/16) subnet-servicestage(192.168.20.0/24)
- Create a CCE Cluster 
- Create a CCE Node 
- Create an Environment in ServiceStage e.g test-env
	# Select the created vpc
	# Environment type: Kurbnetes 

- Add basic resource using the created environment 
	# Bind a CCE Cluster
	# Bind a CSE Engine


- Create an Application under Application Management 
	# Name: e.g weathermap


- Creating a Secret 
#Encode the AK/SK obtained using Base64. In the local Linux environment.
Command:  
	#echo –n ‘access key’ | base64
	# echo –n ‘secret key’ | base64

- Create a Secret under the ServiceStage > CCE > Secrets
	# Creation Mode: Visualization
	# Under Secret data: Add data 
		- cse_credentials_accessKey: Encoded AK
		- cse_credentials_secretKey: Encoded SK


- Preparing the Weather Forecast Source Mode (OPTIONAL)
	#Github Setup 
	- Login to Github 
	- Create new repository e.g hcip 
	- Import Code (Url: https://github.com/servicestage-demo/weathermap.git)
	- Begin Import 
	- View the imported files on hcip repository


- Setting GitHub Repository Authorization (Optional)
# You will use this repository for authorization to build and deploy microservices.

Log in to ServiceStage, choose Continuous Delivery > Repository Authorization, and
click Create Authorization.


- Creating an Organization
Login in to ServiceStage > Deployment Source Management > Organization > Create organization 


############Building a Microservice

(Creating a Build Job of Backend Applications)

- Create Source Code under Continuous Delivery > Build > Create Source code 
	#Select Custom 
	#Compile and Archive the (weather, weather-beta, forecast and fusionweather) 
	# then build.


(Creating a Build Job of Front End Applications)

- Create Source Code under Continuous Delivery > Build > Create Source code 
	# Select Docker 
	# Compile and Archive the (weathermapweb) then build 




##############Deploying a Microservice

(Creating and Deploying a backend application components) 

- Create Component under Application Management > Application List 
	# Create three Component eg. Weather, forecast and fusionweather 
		
		##component name
		## Advanced Settings: Add Environment Variable
			- MOCK_ENABLED: false
			- servicecomb_credentials_accessKey: using secret
			- servicecomb_credentials_secretKey: using secret



(Creating and Deploying a frontend application components) 

- Create Component under Application Management > Application List 
	# Create Component eg.weathermapweb
	# Listening port: 8080



- Go to Cloud Service Engines > Microservice Catalog > Microservice List  to check the running microservice 

#Setting the Access Mode
	- Under Application List choose the created application e.g weathermap
	- Click on weathermapweb 
	- Click on Acccess Mode on the left and Add Service 
		Set the parameters as follows:
			#Service Name: weathermapweb
			#Access Mode: Public network access
			#Access Type: Elastic IP address
			#Service Affinity: Cluster level
			#Port Mapping: TCP | 3000 | Automatically generated



    
    """)