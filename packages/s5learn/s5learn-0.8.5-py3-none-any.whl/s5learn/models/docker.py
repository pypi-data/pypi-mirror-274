def docker():


    print("""
    
    #DOCKER

Docker is a platform that enables developers to build, ship, and run applications inside containers. Here's a comprehensive list of Docker commands along with their descriptions:

##SIMPLE WAY TO INSTALLING DOCKER 


METHOD 1
## Log in to the ECS and install Docker. 
yum install docker 
systemctl enable docker; systemctl start docker




METHOD 2
# Run the following command to install the yum unit:
yum install -y yum-utils

#Run the following command to add the yum source: 
yum-config-manager --add-repo
https://download.docker.com/linux/centos/docker-ce.repo

# Run the following command to install Docker:
yum install docker-ce docker-ce-cli containerd.io

# Run the following command to start Docker: 
systemctl start docker





### Docker CLI Commands


#### General Commands

- **`docker --version`**: Display the Docker version installed on your system.
- **`docker --help`**: Get help about Docker commands.




#### Container Lifecycle

- **`docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`**: Run a command in a new container.
- **`docker start [OPTIONS] CONTAINER`**: Start one or more stopped containers.
- **`docker stop [OPTIONS] CONTAINER`**: Stop one or more running containers.
- **`docker restart [OPTIONS] CONTAINER`**: Restart one or more containers.
- **`docker pause CONTAINER`**: Pause all processes within one or more containers.
- **`docker unpause CONTAINER`**: Unpause all processes within one or more containers.
- **`docker kill [OPTIONS] CONTAINER`**: Kill one or more running containers.
- **`docker rm [OPTIONS] CONTAINER`**: Remove one or more containers.
- **`docker create [OPTIONS] IMAGE [COMMAND] [ARG...]`**: Create a new container without starting it.
- **`docker exec [OPTIONS] CONTAINER COMMAND [ARG...]`**: Run a command in a running container.




#### Container Information

- **`docker ps [OPTIONS]`**: List containers.
- **`docker inspect [OPTIONS] NAME|ID [NAME|ID...]`**: Return low-level information on Docker objects.
- **`docker logs [OPTIONS] CONTAINER`**: Fetch the logs of a container.
- **`docker events [OPTIONS]`**: Get real-time events from the server.
- **`docker top CONTAINER [ps OPTIONS]`**: Display the running processes of a container.
- **`docker stats [OPTIONS] [CONTAINER...]`**: Display a live stream of container(s) resource usage statistics.
- **`docker diff CONTAINER`**: Inspect changes to files or directories on a container’s filesystem.



#### Container Management

- **`docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-`**: Copy files/folders between a container and the local filesystem.
- **`docker rename CONTAINER NEW_NAME`**: Rename a container.
- **`docker update [OPTIONS] CONTAINER [CONTAINER...]`**: Update configuration of one or more containers.




#### Image Management

- **`docker build [OPTIONS] PATH | URL | -`**: Build an image from a Dockerfile.
- **`docker pull [OPTIONS] NAME[:TAG|@DIGEST]`**: Pull an image or a repository from a registry.
- **`docker push [OPTIONS] NAME[:TAG]`**: Push an image or a repository to a registry.
- **`docker images [OPTIONS] [REPOSITORY[:TAG]]`**: List images.
- **`docker rmi [OPTIONS] IMAGE [IMAGE...]`**: Remove one or more images.
- **`docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]`**: Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE.
- **`docker save [OPTIONS] IMAGE [IMAGE...]`**: Save one or more images to a tar archive (streamed to STDOUT by default).
- **`docker load [OPTIONS]`**: Load an image from a tar archive or STDIN.
- **`docker import [OPTIONS] file|URL|- [REPOSITORY[:TAG]]`**: Import the contents from a tarball to create a filesystem image.



#### Network Management

- **`docker network create [OPTIONS] NETWORK`**: Create a network.
- **`docker network connect [OPTIONS] NETWORK CONTAINER`**: Connect a container to a network.
- **`docker network disconnect [OPTIONS] NETWORK CONTAINER`**: Disconnect a container from a network.
- **`docker network ls [OPTIONS]`**: List networks.
- **`docker network inspect [OPTIONS] NETWORK [NETWORK...]`**: Display detailed information on one or more networks.
- **`docker network rm NETWORK [NETWORK...]`**: Remove one or more networks.



#### Volume Management

- **`docker volume create [OPTIONS] [VOLUME]`**: Create a volume.
- **`docker volume inspect [OPTIONS] VOLUME [VOLUME...]`**: Display detailed information on one or more volumes.
- **`docker volume ls [OPTIONS]`**: List volumes.
- **`docker volume rm VOLUME [VOLUME...]`**: Remove one or more volumes.
- **`docker volume prune [OPTIONS]`**: Remove all unused local volumes.



#### Swarm Management

- **`docker swarm init [OPTIONS]`**: Initialize a swarm.
- **`docker swarm join [OPTIONS] HOST:PORT`**: Join a swarm as a node and/or manager.
- **`docker swarm leave [OPTIONS]`**: Leave the swarm.
- **`docker swarm update [OPTIONS]`**: Update the swarm.




#### Service Management

- **`docker service create [OPTIONS] IMAGE [COMMAND] [ARG...]`**: Create a new service.
- **`docker service inspect [OPTIONS] SERVICE [SERVICE...]`**: Display detailed information on one or more services.
- **`docker service ls [OPTIONS]`**: List services.
- **`docker service ps [OPTIONS] SERVICE [SERVICE...]`**: List the tasks of one or more services.
- **`docker service rm SERVICE [SERVICE...]`**: Remove one or more services.
- **`docker service scale SERVICE=REPLICAS [SERVICE=REPLICAS...]`**: Scale one or multiple replicated services.
- **`docker service update [OPTIONS] SERVICE`**: Update a service.



#### Node Management

- **`docker node ls [OPTIONS]`**: List nodes in the swarm.
- **`docker node inspect [OPTIONS] self|NODE [NODE...]`**: Display detailed information on one or more nodes.
- **`docker node rm [OPTIONS] NODE [NODE...]`**: Remove one or more nodes from the swarm.
- **`docker node update [OPTIONS] NODE`**: Update a node.



#### Stack Management

- **`docker stack deploy [OPTIONS] STACK`**: Deploy a new stack or update an existing stack.
- **`docker stack ls [OPTIONS]`**: List stacks.
- **`docker stack ps [OPTIONS] STACK [STACK...]`**: List the tasks in one or more stacks.
- **`docker stack rm [OPTIONS] STACK [STACK...]`**: Remove one or more stacks.
- **`docker stack services [OPTIONS] STACK [STACK...]`**: List the services in one or more stacks.



#### Secret Management

- **`docker secret create [OPTIONS] SECRET file|-`**: Create a secret from a file or STDIN as content.
- **`docker secret inspect [OPTIONS] SECRET [SECRET...]`**: Display detailed information on one or more secrets.
- **`docker secret ls [OPTIONS]`**: List secrets.
- **`docker secret rm SECRET [SECRET...]`**: Remove one or more secrets.


#### Config Management

- **`docker config create [OPTIONS] CONFIG file|-`**: Create a config from a file or STDIN as content.
- **`docker config inspect [OPTIONS] CONFIG [CONFIG...]`**: Display detailed information on one or more configs.
- **`docker config ls [OPTIONS]`**: List configs.
- **`docker config rm CONFIG [CONFIG...]`**: Remove one or more configs.



### Additional Commands

- **`docker login [OPTIONS] [SERVER]`**: Log in to a Docker registry.
- **`docker logout [OPTIONS] [SERVER]`**: Log out from a Docker registry.
- **`docker search [OPTIONS] TERM`**: Search the Docker Hub for images.
- **`docker info [OPTIONS]`**: Display system-wide information.
- **`docker system df [OPTIONS]`**: Show Docker disk usage.
- **`docker system prune [OPTIONS]`**: Remove unused data.
- **`docker system events [OPTIONS]`**: Get real-time events from the server.
- **`docker system info [OPTIONS]`**: Display system-wide information.
- **`docker system df [OPTIONS]`**: Show Docker disk usage.
- **`docker builder prune [OPTIONS]`**: Remove all unused build cache.

These commands cover a wide range of functionalities within Docker, allowing you to manage containers, images, networks, and more effectively.
    
    """)