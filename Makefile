# Makefile para gestionar los servicios de Docker

# Comando base de docker-compose
DOCKER_COMPOSE = docker-compose

# Subir el servicio de clientes
clientes-up:
	@echo "Iniciando el servicio clientes..."
	$(DOCKER_COMPOSE) --profile clientes up -d

# Detener el servicio de clientes
clientes-down:
	@echo "Deteniendo el servicio clientes..."
	$(DOCKER_COMPOSE) --profile clientes down

# Reiniciar el servicio de clientes
clientes-restart:
	@echo "Reiniciando el servicio clientes..."
	$(DOCKER_COMPOSE) --profile clientes restart
