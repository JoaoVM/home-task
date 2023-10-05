# Home Task Application Diagrams

### Note
Please note that all the diagrams were built taking into consideration a deployment on AWS.
However, I've also used other tools before deploying taking into consideration the costs and performance of the solution.

## Diagrams
 - Infrastructure Deployment
 - CI Diagram
 - CD Diagram
 - Observability Diagram

#### Infrastructure Deployment
Please take into account that I've used Github to write the Terraform solution and used Github Actions to deploy the Terraform code into AWS.
Basically, after writing the terraform code using AWS Terraform modules the solution will be deployed using GitHub actions. During the process of the deployment, Checkov will scan the terraform code and collect all the vulnerabilities, and export a SARIF file with the vulnerabilities.
After that, the terraform will be deployed to AWS.

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

It's not visible on the diagram but regarding the Network all the security groups, route tables, elastic ips, roles, and policies are also created.
Regarding the EKS cluster, Node groups with proper tolerations and taints are created also autoscaling groups.
All the resources are created with tags by default.

Please check the diagram for more information.
  ![Infrastructure Diagram](../docs/images/Revolut%20Infrastructure%20Diagram.png?raw=true "Infrastructure Diagram")


#### CI Diagram
On the Continuous Integration diagram, the starting point for continuous integration is the development cycle. 
After that, the code will be committed to GitHub and will automatically trigger an action to check what I call the "Validation Box". On this, it will run the Oawsp Dependency Checker, and Unit Testing and it will be scanned by Sonarqube. If everything is working and it should, the pipeline will automatically trigger the next step, which is docker build and tag.

Then the docker images will be pushed to the Image Registry repository, and in this case should be AWS ECR on AWS.
Inside AWS ECR it will run vulnerability checking, I'm using the default vulnerability scanner for AWS ECR but we can also add other scanners like Trivy to check the vulnerabilities.
If everything is working properly, the process is finished, otherwise, the process needs to be restarted to code refactoring to fix the vulnerabilities.


Please check the diagram for more information.
  ![CI Diagram](../docs/images/Revolut%20CI%20Diagram.png?raw=true "CI Diagram")


#### CD Diagram
On Continuous Deployment diagram is also the development cycle, but this time development of helm charts and also ansible playbooks and roles.
When it's done, helm charts and Ansible playbooks will be committed to Git Hub and will automatically start the deployment process.
Helm charts will pushed to the AWS ECR Register to be used later in the deployment process.

During the deployment process ArgoCD, which is installed into the EKS Cluster will be responsible for monitoring and synchronizing the differences between what exiting cluster and the changes that were made.
By using ArgoCD, we can ensure that we are running the latest versions and that ArgoCD manages the deployment process without downtime.

Please check the diagram for more information.
  ![CD Diagram](../docs/images/Revolut%20CD%20Diagram.png?raw=true "CD Diagram")


#### Observability Diagram
In a scenario where we create a complete solution to observability, we should consider the following diagram.
First divide and create the namespaces for each purpose. 
This process should have started with terraform, creating namespaces and node groups for each purpose.

For example, create a namespace for logs, and create a node group with proper tolerations and taints.
When deploying the helm charts for Fluentbit and Loki make sure that they will be deployed using the tolerations and taints for the nodegroup.
This will ensure that node group resources are reserved to run those tools and our cluster is not a mess of nodes, namespaces, and pods. This will also ensure that we will not accidentally lose the capacity of the cluster resources because the plan was done specifically for that purpose, using Fluent bit and Loki with those resources and limits.

So basically we want to deploy the different tools with different purposes on different nodes and namespaces. The logs namespaces are reserved for Loki and Fluentbit. Metrics are reserved for Thanos, Prometheus, and the complete stack of Prometheus. Monitoring is reserved for Grafana, Uptime Kuma, and Alertmanager. And of course, tracing for OpenTelemetry and Tempo.

So, Fluentbit will collect logs from the home task and send them to log aggregator Loki, which will be used to visualize the logs into Grafana.
Then Prometheus Node Exporter, Kube state metrics will collect metrics from nodes and pods and will be scraped by Prometheus, which will use remote write to send metrics to Thanos receiver. Then Thanos will store the metrics on an objectstore like S3 Bucket and when the metrics are needed on Grafana a request using Thanos Querier will collect metrics on the objectstore.

Using Thanos the rules for alerts are not stored anymore on Prometheus, now they are stored on Thanos Ruler.
AlertManager will use those rules to send alerts to the predefined services, like email, teams, slack, etc.
We also can check our endpoints using Uptime Kuma, which will provide data about the endpoints, certificates, and latency. This can also be visible on Grafana with the Uptime Kuma metrics endpoint enabled.

Finally, using OpenTelemetry we can trace requests and responses from the server, to do that automatically we need to provide OpenTelemetry with Auto Instrumentation enabled. This will inject OpenTelemetry SDK into the application and configure the application to send spans to the OpenTelemetry collector.
Then with Tempo, traces are stored from the different applications into a single point and then ready to be visualized with Grafana.

Please check the diagram for more information.
  ![Observability Diagram](../docs/images/Revolut%20Observability%20Diagram.png?raw=true "Observability Diagram")



