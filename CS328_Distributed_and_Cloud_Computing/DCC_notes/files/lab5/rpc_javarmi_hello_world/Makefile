SHELL := /bin/bash

bin_folder=bin/

setup-java:
	apt install -y default-jdk

build-src:
	javac -d ${bin_folder} protocol/AssistantService.java server/AssistantServer.java client/Client.java

run-registry:
	cd ${bin_folder}; rmiregistry 1099

run-server:
	java -cp ${bin_folder} server.AssistantServer

run-client:
	java -cp ${bin_folder} client.Client
