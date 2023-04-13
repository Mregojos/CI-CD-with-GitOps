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


9. Starts Kubernetes (local without ArgoCD)

```sh
# Start minikube if not started yet
minikube start

kubectl apply -f deployment.yaml
kubectl get deployments
kubectl get services

kubectl get pods
kubectl get nodes
kubectl get all

minikube service streamlit-app-service --url
kubectl get nodes -o wide
minikube ip

minikube stop
minikube delete

# Port Forwarding use the Docker Port, this will work in codespace
# kubectl port-forward deployment/streamlit-app 8501:8501

# Port Forwarding use the Docker Port, this will work in Cloud9
kubectl port-forward deployment/streamlit-app 8501:8501 --address 0.0.0.0

# Minikube service <service name>
minikube service <service name>

# To create namespace
kubectl create namespace <name space>
# -n <namespace>

# To delete deployments and services
kubectl delete deployment <deployment name>
kubectl delete service <service name>

# To watch it
watch kubectl get all
```

10. Use ArgoCD for Continuous Delivery

```sh
# Scripts for ArgoCD

# Start minikube
# minikube start 

# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Verify the ArgoCD pods
kubectl get pods -n argocd

# Use port-forward to make it works in Cloud9
kubectl port-forward svc/argocd-server -n argocd 8080:443 --address 0.0.0.0

# Open web browser
<localhost | ip address>:8080 

# Login
Username: admin
Password: argocd-server-xxxxx-xxxx (ArgoCD Server Pod)
# or
ARGOCD_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
echo $ARGOCD_PASSWORD 

# Create namespace for streamlit-app
kubectl create namespace streamlit-app
# watch
watch kubectl get all -n streamlit-app

# In web UI
# New App button
    # Application Name: streamlit-app
    # Project: default
    # Sync Policy: Automatic
    # Repository: Git repository
    # Revision: Git branch, tag, commit 
    # Path: Where Kubernetes manifests are stored (./) but if I use Deployment folder (Deployment)
    # Destination Cluster URL: https://kubernetes.default.svc
		# Namespace: streamlit-app
		# [Cluster: minikube]
# Create

# View in App web UI
# Check the namespace streamlit-app
kubectl get all -n streamlit-app

# Port Forwarding for the App, use the Docker Port, this will work in Cloud9
kubectl port-forward deployment/streamlit-app 8501:8501 -n streamlit-app --address 0.0.0.0
# Open Browser <localhost | ip address>:8501

---
# To delete ArgoCD 
kubectl delete -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```


