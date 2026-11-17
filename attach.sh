dirname=$(basename "$PWD" | tr "[:upper:]" "[:lower:]")
container_name=${dirname}_dev

docker exec -it ${container_name} bash