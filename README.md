# CI/CD with GitOps (GitHub Actions and ArgoCD)

## Architecture


## Tech Stack
* GitHub, Amazon EC2, Python, Streamlit, Docker, Docker Hub, Kubernetes, Minikube, GitHub Actions, ArgoCD 

## Objective
* To containerize the web app and push it to docker repository
* To deploy the containerized web app using container orchestration
* To build CI/CD Pipelines


## Tasks
1. Web Application
* The app is a simple data analysis web app
* App Code Source: [Link](https://github.com/mregojos/data-analysis-app)

2. Provision Amazon EC2 on Cloud9
* I will be using Amazon EC2 Ubuntu Linux
* Spec: t3.medium, 4GB RAM, 2CPUs, 30 GB RAM

4. Install Miinikube and Kubectl
* Minikube is used to create a cluster on a local computer. It is also used for development purposes only.

```sh
# Install Kubernetes and Minikube
# kubectl-minikube.sh
# chmod +x kubectl-minikube.sh
# ./kubectl-minikube.sh

# Update System
sudo apt-get update

# Install kubectl
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl

# Make it executable and move it to a system path
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl

# Install minikube
# Download
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

# Make it executable and move it to a system path
chmod +x minikube
sudo mv minikube /usr/local/bin/

# minikube start [--driver=docker]
# minikube status
# kubectl cluster-info
# kubectl get nodes
```

5. Test the app locally

```sh
docker build -t streamlit-app .
docker run --name streamlit-app -p 8501:8501 streamlit-app
docker images

# For interactive terminal
docker exec -it streamlit-app sh

# Check the app
# http://<ip address>:8501
```

6. Push the image to Docker Hub Registry

```sh
# To push the image to docker hub
# build the image first
# docker logout if docker login doesn't work
# docker logout
docker login
# Login your credentials
docker build -t streamlit-app .
docker tag streamlit-app <Docker Hub ID>/streamlit-app:latest
docker push <Docker Hub ID>/streamlit-app:latest

# Don't forget to logout if you are done with the terminal
# docker logout 
```

7. Start Minikube

```sh
minikube start
```

8. Create a deployment.yaml file
[deployment.yaml](https://github.com/Mregojos/CI-CD-with-GitOps/blob/main/Deployment/deployment.yaml)


9. Starts



