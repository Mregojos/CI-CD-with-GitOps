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

```

5. Test the app locally
``sh

``

6. Push the image to Docker Hub Registry
``sh

```

7. Start Minikube
```sh

```

8. Create a deployment.yaml file
[deployment.yaml](https://github.com/Mregojos/CI-CD-with-GitOps/blob/main/Deployment/deployment.yaml)






