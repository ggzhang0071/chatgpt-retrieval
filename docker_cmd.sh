docker_image="guihua_gpt"
cd docker
sudo docker build -t $docker_image .

sudo  docker run   --privileged=true   --workdir /git --name "guihua_chatgpt" -e DISPLAY --ipc=host -d \
--rm -p 4000:4000 -v /localhome/local-vili/git/chatgpt-retrieval:/git/guihua_gpt  $docker_image

sudo docker exec -it guihua_chatgpt /bin/bash

#sudo docker stop guihua_gpt
