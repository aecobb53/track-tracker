# track-trackerdocker compose --file docker-compose-deploy.yml down
docker compose build
docker compose --file docker-compose-deploy.yml up -d
