# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dvandenb <dvandenb@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/03/08 12:20:28 by pudry             #+#    #+#              #
#    Updated: 2024/03/08 14:56:05 by dvandenb         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


DOCKER_COMPOSE = docker-compose.yml
NAME = transcendence
PROJECT = test

all: build_docker stop run build_server 

NewMember:
	python3 ./$(PROJECT)/manage.py startapp $(name)

build_docker:
	docker pull postgres

build_server:
	./init_server.zsh

run:
	docker compose -f  ${DOCKER_COMPOSE} -p ${NAME} up --detach

stop:
	docker compose -f ${DOCKER_COMPOSE} -p ${NAME} down

delete:
	-docker stop $$(docker ps -qa)
	-docker rm $$(docker ps -qa)
	-docker rmi -f $$(docker images -qa);
	-docker volume rm $$(docker volume ls -q);
	-docker network rm $$(docker network ls -q) 2>/dev/null

fclean: stop delete

re: fclean all
