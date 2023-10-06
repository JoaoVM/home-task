# Home Task

## Requirements
- Design and code a simple "Hello World" application that exposes the following
HTTP-based APIs.
- Saves/updates the given user’s name and date of birth in the database.
- Returns hello birthday message for the given user
- Use database or storage
- Produce a system diagram of your solution deployed
- Write configuration scripts for building and no-downtime production deployment of
this application.
- The solution must have tests, runnable locally, and deployable to the cloud.
- Keeping in mind aspects that an SRE would have to consider.


## Folder Structure
 - app (Python code with Dockerfile and docker-compose file)
 - deployment (Helm Charts to be deployed)
 - docs (Images and diagram and screenshots of the app running)

 

## Installation Requirements
Before start deploying the app please make sure that you have the following tools installed.

#### Install Docker
- Linux
```bash
  yum install docker -y
```
- Mac
```bash
  brew install docker
```
    
#### Install Colima
If you don't want to install docker on Mac, alternatively you can use Colima
- Mac
```bash
  brew install colima
```


#### Install Python
- Linux
```bash
  yum install python -y
```
- Mac
```bash
  brew install python
```

#### Install Helm
- Linux
```bash
  sudo curl -fsSL -o /etc/yum.repos.d/helm.repo https://baltocdn.com/helm/stable/rpm/helm.repo
  sudo yum install helm
```

- Mac
```bash
  brew install helm
```

#### Install Kubectl
- Linux
```bash
  sudo yum install kubernetes-client -y
```

- Mac
```bash
  brew install kubectl
```

#### Install Minikube (Only if you will run this app locally)
- Linux
```bash
    #install hypervisor to run on your machine
    sudo yum install epel-release -y
    sudo yum install qemu-kvm libvirt libvirt-python libguestfs-tools virt-install -y
    sudo systemctl start libvirtd
    sudo systemctl enable libvirtd
    sudo systemctl status libvirtd

    #download and install minikube
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube

    #start minikube
    minikube start --memory 4096 --cpus 2 --vm-driver=kvm2
```

- Mac
```bash
  brew install minikube

  #start minikube
  minikube start --memory 4096 --cpus 2 --driver=qemu2
```

#### Install Thunder Client or Postman (I'm using Thunder Client extension on VSCode, it's up to you)
You can find the collection for thunder client with name ```thunder-collection_home-task.json``` inside "app" folder.
Don't forget to change ports if needed.