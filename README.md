# CI/CD with GitOps (GitHub Actions and ArgoCD)

## Architecture


## Tech Stack
* GitHub, Amazon EC2, Cloud9, Python, Streamlit, Docker, Docker Hub, Kubernetes, Minikube, GitHub Actions, ArgoCD 

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

11. (Optional) Use Kustomize Package Manager

```sh
# For Kustomize (Package Manager)
mkdir -p kustomize/base
mkdir -p kustomize/overlay

# same as deployment.yaml
touch kustomize/base/deployment.yaml

# kustomize/base/kustomization.yaml
touch kustomize/base/kustomizaton.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml

# kustomize/overlay/kustomizaton.yaml
touch kustomize/overlay/kustomizaton.yaml
# kustomize/overlaykustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../base

# Apply
kubectl kustomize kustomize/overlay | jubectl apply -f -
```
12. GitHub Actions

```sh
# GitHub Actions For Building Dockerfile from GitHub Repository and Puching Image to Docker Hub
# Setup Secrets (Actions)
# DOCKER_APP_REPO: mattregojos/streamlit-app
# DOCKER_HUB_USERNAME: mattregojos
# DOCKER_HUB_PASSWORD: <my password in Docker Hub>
# GH_PAT: <Create Token>
# Add a file: .github/workflows/main.yaml
name: Build and Push Docker Image
```

```sh
on:
    push:
        branches:
            - main
	paths:
	    - 'Application/**'
    pull_request:
        branches:
            - main
	paths:
	    - 'Application/**'
	    
jobs:
    build-and-push:
	runs-on: ubuntu-latest
        
        steps:
        - name: Checkout repository
          uses: actions/checkout@v2
	  with:
	      token: ${{ secrets.GH_PAT }}
          
        - name: Log in to Docker Hub
          uses: docker/login-action@v1
          with:
              username: ${{ secrets.DOCKER_HUB_USERNAME }}
              password: ${{ secrets.DOCKER_HUB_PASSWORD }}
        
        - name: Build and push Docker image
          uses: docker/build-push-action@v2
          with:
              context: Application # Application Folder (Use . if not in folder)
              push: ${{ github.event_name != 'pull_request' }}
              tags: |
                ${{ secrets.DOCKER_APP_REPO }}:${{ github.sha }}
                ${{ secrets.DOCKER_APP_REPO }}:latest

        - name: Edit Deployment/deployment.yaml
	  run: |
	     sed -i 's|image:.*|image: ${{ secrets.DOCKER_APP_REPO }}:${{ github.sha }}|' Deployment/deployment.yaml

	- name: Configure Git
          run: |
            git config --global user.email "matt"
            git config --global user.name "mregojos"
        
        - name: Commit and push changes
          run: |
            git add Deployment/deployment.yaml
            git commit -m "Update Deployment/deployment.yaml with new image tag"
            git push

```

```sh
# Git File System
#.github/workflows/main.yaml
# Aplication/<files here>
# Deployment/<files here>
# Change CD PATH from ./ to Deployment

# GitHub Actions to edit Deployment.yaml from GitHub Repository
# Add step to edit Deployment.yaml from the same GitHub Repository (only use sed)
```

13. For GitHub Webhooks 

```sh
# For GitHub Action
# Github Webhook IP for security Group

# In Amazon EC2 security group
# Change the security group
# Add Ingress
# Source: 140.82.112.0/20
# Type: Custom TCP
# Port 8080

# Go to GitHub Repo and add webhooks
# Webhooks
# https://<ip-address>:8080/api/webhook
# SSL Verification: Disable
# Create WebHooks

# Try to change the deployment.yaml (change replicas to 3)
# See the ArgoCD Web UI App (It's changed)
```











