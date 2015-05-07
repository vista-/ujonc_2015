# Docker module creation

## What is this?

A few small Python scripts that have no extra dependencies (except for docker) with which you can build and start module infrastructure in an environment closely matching the actual production environment.

Also, quite a few examples are included to get you started.

##Contact
Kalman Tarnay <kalman.tarnay@avatao.com>

##Prerequisite:
Fairly recent (>= 1.2.0) version of docker. Download and install the most recent version from docker.io:

    curl -sSL https://get.docker.io/ubuntu/ | sudo sh

Optionally add yourself to the "docker" group so that you will be able run the scripts without root. **Don't forget to logout, and login for the changes to take effect. Please note, that the docker group is root-equivalent.**

    sudo gpasswd -a ${USER} docker

##Architecture
###Containers
2 containers for a module per user:

- the module accessible to the end-user (Solvable from here on)
- the solution checker linked to the other (Solution checker from here on)

###Types
####Sshd type module
End-user can login using ssh as the "user" user, and then do his thing to get the job done.
####Web type module
End-user can access a http server, and then do his thing to get the job done.

###Solution checking
Avatao platform calls into the solution checker via http with the (optional) flag that user submitted. You will be able test locally with following command:

    curl -X POST -H "Content-Type: application/json" -d '{"solution":"User provided input/flag"}' 127.0.0.1:5555/secret
    {
      "solved": false,
      "message": "an optional message to be returned to the user"
    }
    
The "secret" part of the url is provided to the solution checker via the SECRET environment variable. It is set to "secret" by the scripts.

##Examples
###kalmi_rm
User can login using ssh. The /home/user directory is shared between the two containers (triggered by the VOLUME directive in the solvable's Dockerfile). The user has to delete a file. The solution checker checks for the lack of presence of the file.

###kalmi_flagserver
User can login using ssh. A http server is autostarted on the solvable as an other user. The /var/flag directory is (autocreated and) shared between the two containers (triggered by the VOLUME directive in the solvable's Dockerfile). Before the webserver is started on the solvable, a /var/flag/flag.txt file is created containing a random value. The solution checker checks if the submitted solution matches the one in /var/flag/flag.txt.

###kalmi_nc
User can login using ssh. User has to start a tcp server on port 8080, which is exposed to the solution checker (triggered by the EXPOSED directive in the solvable's Dockerfile). The solution checker connects to solvable:8080 to see if anything is listening there. The domain "solvable" is present in /etc/hosts and points to the solvable.

###kalmi_shellshock
User can login using ssh. There is a flag.txt in the user's home, but it is not readable by the user. There is a setuid binary in the user's home that runs a bash script as an other user that has permission to read the file. The user does not have write permission to the bash file. The user has to acquire the flag by exploiting bash. The solution checker only checks the flag. The Dockerfile installs an old version of bash that is susceptible to shellshock.

###kalmi_web
The user can only access a webserver that is running on the solvable, and has to acquire a flag. The /var/flag directory is (autocreated and) shared between the two containers (triggered by the VOLUME directive in the solvable's Dockerfile). Before the webserver is started on the solvable, a /var/flag/flag.txt file is created containing a random value. The solution checker checks if the submitted solution matches the one in /var/flag/flag.txt.

###balidani_*
User can login using ssh. He needs to fix exploitable services. The solution checker scripts check whether the services are still vulnerable. The solution checker script should return a friendly message if the service is not running. The solution checker scripts are not very reliable at the moment.

##Build
Run the to following to build/rebuild images:

    python build.py
    
Only the first build is slow.

Later you can refence images with the directory's name they were in.
If you modify any file in those directories, you need to rebuild, before starting them.

Also, can you use it like this to only rebuild some images:

    python build.py modules/kalmi_nc_checker modules/kalmi_flagserver_checker

##Run
Run the following to start an sshd type built solvable and solution checker pair:

    python start_sshd_package.py <name_of_solvable> <name_of_solution_checker>
    
Run the following to start an web type built solvable and solution checker pair:

    python start_web_package.py <name_of_solvable> <name_of_solution_checker>

For example, to start one of the sample solvable and solution checker pairs:

    python start_sshd_package.py kalmi_rm_solvable kalmi_rm_checker
    python start_sshd_package.py kalmi_flagserver_solvable kalmi_flagserver_checker
    python start_sshd_package.py kalmi_nc_solvable kalmi_nc_checker
    python start_web_package.py kalmi_web_solvable kalmi_web_checker
    ...

##Troubleshooting
###I'm getting port already taken errors when starting

Please don't try to run more than solvable-checker pair.

If that's not the case, then something got stuck somewhere, and can kill all docker containers using:

docker kill $(docker ps -q)

If you get a usage text about docker kill, that means there were no running containers.

###Solvable starts, but connection attempts fail with:

    ssh_exchange_identification: Connection closed by remote host
    
You put a blocking command in start.sh, and thus sshd was never started. Fix the offending command, and rebuild.

This weird behaviout is observed because docker accepts connection attempts to published ports no matter what, but then resets them if the published port isn't really listening.

###I need to enter the container to look at something without triggering start.sh

Just do a build of the container, and grab the hash at the end, and:

    docker run --rm -t -i 6ae8863c8a84

Alternatively you can use its full name:
    
    docker run --rm -t -i docker-registry.avatao.com:5000/kalmi_flagserver_solvable
    
The container will get removed, when you exit it.

###I need to enter a running container as root to figure something out

If sshd's non-root login is not enough for you. You can grab docker-enter from https://github.com/jpetazzo/nsenter

To use docker-enter, you will need to find the running containers name, you can do this by running:

    docker ps

and look at NAMES column. It should be in the following format: kalmi_flagserver_checker1412322907

    sudo docker-enter kalmi_flagserver_checker1412323413

###Etc
kalman.tarnay@avatao.com