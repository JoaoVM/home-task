# Home Task Helm Chart

### Note
Please note that to deploy this package of apps you need to have helm installed.
Also, make sure you have a connection to your Kubernetes Cluster.
You can use minikube or other Kubernetes virtualization to install.

## Helm charts
 - general-chart
    - home-task
    - kube-prometheus-stack
    - loki-stack
    - opentelemetry-collector
    - tempo
    - uptime-kuma

## Installation
To install the helm chart all you need is to change directory to ```deployment``` and run the following command:
```
helm upgrade --install home-task general-chart -f general-chart/values.yaml --namespace revolut --create-namespace
```
If everything is ok you should get the same result as the following image:
 ![Deploy Command Line](../docs/images/deploy-heml-chart.jpg?raw=true "Deploy Command Line")

 And them, if you use Openlens your pods should be like this:
 ![OpenLens Status](../docs/images/openlens-heml-chart.jpg?raw=true "OpenLens Status")


#### general-chart
The General Helm Chart is an umbrella chart, which means that within the main chart, there are other charts that will be installed with the main chart.
The general chart is dependent on the charts that are part of the main chart.

#### home-task
This chart is responsible for the deployment of the created app. That chart will install the statefulset, service, and pod disruption budget.
By default, it will install 3 replicas, and the update strategy will be a rolling update with a maximum unavailable of 25%, and only 1 pod is allowed to be unavailable at the same time.
This will allow us to ensure that we don't have downtime during the new deployments and updates to the current deployment.


#### kube-prometheus-stack
This is a well-known helm chart. Inside it, there are tools such grafana, prometheus, alertmanager, kube-state-metrics, prometheus-node-exporter and thanos.
In this case, I choose to not install Thanos, since it's just a small piece, however, using a different approach we should definitely use Thanos, which will allow for reducing costs of the storage, for example, by using S3 to store metrics instead of putting all the metrics into an Elastic Block Storage and Persistent Volume. Also, it's safer than storing in a Persistent Volume with the risk of deleting data, and avoiding mistakes.

#### loki-stack
Loki is a lightweight log aggregator that collects logs from various sources and aggregates them into a centralized location for easy analysis and troubleshooting.
With Loki stack is also installed fluent bit, which is a lightweight log collector, and can be configured to collect from multiple sources and also send logs to multiple targets, including Loki.
Similar to the Thanos, logs can be stored in a separate ObjectStore, that will be used instead of the default Persistent Volumes and Elastic Block Storage.

#### opentelemetry-collector
OpenTelemetry is a tool that offers the availability for collecting observability data from applications and infrastructure. It simplifies the process of instrumenting applications and allows for aggregation, transformation, and export of telemetry data to various destinations.
This can be used for collecting traces and also is very useful to inject auto instrumentation into applications that are not ready for tracing.

#### tempo
Grafana Tempo is a distributed tracing backend. The purpose is to store and retrieve data traces for observability. Tempo integrates well with other observability tools like OpenTelemetry and can handle large volumes of traces for analysis and visualization.
Then as a data source of Grafana, it can be used to visualize and analyze traces for app requests and responses

#### uptime-kuma
Uptime Kuma is a monitoring solution for websites. It allows you to monitor the uptime and performance of your websites or APIs from various locations around the world.
Uptime Kuma provides a user-friendly dashboard where you can view the status of your websites, receive alerts in case of downtime or performance issues, and analyze historical data. It also supports integrations with messaging platforms like Microsoft Teams, allowing you to receive notifications directly in your communication channels.