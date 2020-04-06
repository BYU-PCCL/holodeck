docker login -u holodeck

# build the different images. default and dexterity depend on base
docker build -t pccl/holodeck:base -f ./Dockerfile ..
docker build -t pccl/holodeck:default-worlds -f ./Dockerfile_default_worlds ..
docker build -t pccl/holodeck:dexterity -f ./Dockerfile_dexterity ..

docker push pccl/holodeck:base
docker push pccl/holodeck:default-worlds
docker push pccl/holodeck:dexterity

