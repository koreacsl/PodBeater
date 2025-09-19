#!/bin/bash

# Define the docker services with images and versions
declare -A docker_services


docker_services=(
    [traefik]="3.1 3.0 2.11 2.10 2.8"
    [nginx]="1.26.1 latest 1.27.1 1.26 1.27.3"
    [tomcat]="11.0.1 10.1.33 9.0.97 9.0.96 10.1.31"
    [redis]="7.4.2 7.4 7.2 6.2 7.0"
    [mongo]="8.0 7.0.15 8.0.3 6.0.19 6.0"
    [wordpress]="php8.3 php8.2 php8.1 apache 6.7.1-php8.3"
    [alpine]="3.20 3.19 3.18 3.17 3.16"
    [busybox]="1.37 1.36 1.35 1.34 1.33"
    [python]="3.13.0 3.13 3.12.7 3.12"
    [registry]="2.8.3 2.8 2.8.2 2.8.1 2.7"
    [httpd]="2.4.62 2.4 2.4.61 2.4.60 2.4.59"
    [memcached]="1.6.32 1.6 1.6.30 1.6.29 1.6.28"
    [golang]="1.23.3 1.23 1.22.9 1.22 1.23.2"
    [node]="18.20.5 20.18.1 23.3 23.3.0"
    [rabbitmq]="4.0 4.0.5 3.13.7 3.12.14 4.0.3"
    [openjdk]="24-oracle 24 23-jdk 23"
    [sonarqube]="9.9.7-enterprise 10.7-enterprise 10.8-developer 9.9.7-developer"
    [ruby]="3.3.6 3.3 3.2.6 3.2 3.1.6"
    [maven]="3.9.9 3.8 3.9.8 3.9.6 3.8.8"
    [caddy]="builder 2.9 2.8.4 2.8 2.8.1"
    [eclipse-mosquitto]="2.0.20 2.0.19 2.0.18 2.0.17 2.0.16"
    [vault]="1.12.7 1.11.11 1.12.5 1.13.2 1.13.3"
    [dart]="3.7.1 3.7 3.7.0 3.6.2 3.6"
    [matoma]="5.2.2 5.2 5.2.1 5.1.2 5.0.3"
    [telegraf]="1.33.3 1.33 1.33.2 1.32 1.30"
)


# Registry URL, replace <LOCAL_REGISTRY> with the IP or hostname of your local registry server
registry_url="<LOCAL_REGISTRY>:5000"

# Iterate through services and versions
for service in "${!docker_services[@]}"; do
  image_prefix=${service}
  versions=${docker_services[$service]}
  for version in $versions; do
    echo "Processing $image_prefix:$version..."

    # Pull the image
    podman pull docker.io/library/$image_prefix:$version

    # Tag the image for the private registry
    podman tag docker.io/library/$image_prefix:$version $registry_url/$image_prefix:$version

    # Push the image to the private registry
    podman push $registry_url/$image_prefix:$version --tls-verify=false

    if [ $? -eq 0 ]; then
      echo "$image_prefix:$version successfully pushed to $registry_url."
    else
      echo "Failed to push $image_prefix:$version to $registry_url."
    fi
  done
done
