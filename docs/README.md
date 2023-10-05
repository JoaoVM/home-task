# Home Task Application Diagrams

### Note
Please note that all the diagrams were builted taking in consideration a deploy on AWS.
However, I've also used other tools before deploy taking in consideration costs and performance of the solution. 

## Functions
 - Infrastructure Deployment
 - CI Diagram
 - CD Diagram
 - Observability Diagram

#### Infrastructure Deployment
Please take into account that I've used Github to write the Terraform solution and used Github Actions to deploy the Terraform code into AWS.
Basically after write the terraform code using AWS Terraform modules the solution will be deployed using github actions. During the process of the deployment Checkov will scan the terraform code and collect all the vulnerabilities and export a SARIF file with the vulnerabilities.
After that the terraform will be deployed to AWS.

The deployment contain the following resources:
  - 1 VPC
  - 3 Public Subnets
  - 3 Private Subnets
  - 3 NAT Gateway
  - 1 Internet Gateway
  - 1 Ingress LoadBalancing
  - 1 EKS Cluster
  - Auto Scaling Groups
  - Node Groups

It's not visible on the diagram but regarding Network all the security groups, route tables, elastic ips, roles and policies are also created.
Regarding EKS cluster, Nodegroups with tolaretions and taints are created and also autoscaling groups.
All the resource are created with tags by default.

Please check the diagram for more information.
  ![Infrastructure Diagram](../docs/images/Revolut%20Infrastructure%20Diagram.png?raw=true "Infrastructure Diagram")


#### CI Diagram

Please check the diagram for more information.
  ![CI Diagram](../docs/images/Revolut%20CI%20Diagram.png?raw=true "CI Diagram")


#### CD Diagram

Please check the diagram for more information.
  ![CD Diagram](../docs/images/Revolut%20CD%20Diagram.png?raw=true "CD Diagram")


#### Observability Diagram

Please check the diagram for more information.
  ![Observability Diagram](../docs/images/Revolut%20Observability%20Diagram.png?raw=true "Observability Diagram")



