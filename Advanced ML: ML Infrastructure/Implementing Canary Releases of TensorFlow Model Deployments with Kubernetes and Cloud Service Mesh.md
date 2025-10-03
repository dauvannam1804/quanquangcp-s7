# Implementing Canary Releases of TensorFlow Model Deployments with Kubernetes and Cloud Service Mesh

**Experiment**: Lab  
**Schedule**: 1 hour 30 minutes  
**Credits**: 5  
**Level**: Intermediate  
**Lab ID**: GSP778  

---

## Overview
Istio is an open source framework for connecting, securing, and managing microservices, including services running on Kubernetes Engine. It lets you create a mesh of deployed services with load balancing, service-to-service authentication, monitoring, and more, without requiring any changes in service code.

Cloud Service Mesh (ASM) is powered by Istio. With Cloud Service Mesh, you get an Anthos tested, fully supported, distribution of Istio, letting you create and deploy a service mesh with Anthos GKE, whether your cluster is operating in Google Cloud or on-premises.

This lab shows you how to use Cloud Service Mesh on Google Kubernetes Engine (GKE) and TensorFlow Serving to create canary deployments of TensorFlow machine learning models.

---

## What you'll learn
In this lab, you will learn how to:

- Provision a cluster on Google Kubernetes Engine (GKE)  
- Install and configure Cloud Service Mesh  
- Create a canary release of a TensorFlow model deployment  
- Configure various traffic splitting strategies  

---

## Prerequisites
To successfully complete the lab you need to have:

- Solid understanding of how to save and load TensorFlow models  
- Basic familiarity with Kubernetes and Istio concepts and architecture  

Recommended resources:  

- [Using the SavedModel format](https://www.tensorflow.org/guide/saved_model)  
- [Kubernetes Overview](https://kubernetes.io/docs/concepts/overview/)  
- [Istio Concepts](https://istio.io/latest/docs/concepts/)  
- [Cloud Service Mesh (ASM)](https://cloud.google.com/service-mesh)  

---

## Lab scenario
In the lab, you will deploy two versions of the ResNet model using a canary release strategy.  

- **ResNet50** → simulated production model  
- **ResNet101** → new canary release  

Istio will be used to configure traffic splitting between both deployments. Both models will be exposed through the same endpoint.

---

## Summary of tasks
1. Provision a cluster on Google Kubernetes Engine (GKE)  
2. Install and configure Cloud Service Mesh  
3. Deploy ResNet models using TensorFlow Serving  
4. Configure Istio Ingress gateway  
5. Configure Istio virtual services and destination rules  
6. Configure weight-based routing  
7. Configure content-based routing  

---

## Setup and requirements
- Access via Chrome (Incognito recommended)  
- Use only the provided student account (not personal Google Cloud account)  
- Labs are timed and cannot be paused  

---

## Lab instructions

### Task 1. Set up your project
```bash
cd
SRC_REPO=https://github.com/GoogleCloudPlatform/mlops-on-gcp
kpt pkg get $SRC_REPO/workshops/mlep-qwiklabs/tfserving-canary-gke tfserving-canary

export PROJECT_ID=$(gcloud config get-value project)
export PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
export CLUSTER_NAME=cluster-1
export CLUSTER_ZONE=ZONE
export WORKLOAD_POOL=${PROJECT_ID}.svc.id.goog
export MESH_ID="proj-${PROJECT_NUMBER}"
```

### Task 2. Set up your GKE cluster
```bash
gcloud config set compute/zone ${CLUSTER_ZONE}
gcloud beta container clusters create ${CLUSTER_NAME}   --machine-type=e2-standard-4   --num-nodes=5   --workload-pool=${WORKLOAD_POOL}   --logging=SYSTEM,WORKLOAD   --monitoring=SYSTEM   --subnetwork=default   --release-channel=stable   --labels mesh_id=${MESH_ID}

kubectl create clusterrolebinding cluster-admin-binding   --clusterrole=cluster-admin   --user=$(whoami)@qwiklabs.net
```

### Task 3. Install Cloud Service Mesh
```bash
curl https://storage.googleapis.com/csm-artifacts/asm/asmcli_1.15 > asmcli
chmod +x asmcli

./asmcli install   --project_id $PROJECT_ID   --cluster_name $CLUSTER_NAME   --cluster_location $CLUSTER_ZONE   --fleet_id $PROJECT_ID   --output_dir ./asm_output   --enable_all   --option legacy-default-ingressgateway   --ca mesh_ca   --enable_gcp_components
```

---

## Task 4. Enable sidecar injection
```bash
kubectl label namespace default istio-injection=enabled
```

---

## Task 5. Deploy ResNet50 ConfigMap
```bash
kubectl apply -f tfserving-canary/resnet50-configmap.yaml
```

---

## Task 6. Deploy ResNet50 with TensorFlow Serving
```bash
kubectl apply -f tfserving-canary/resnet50-deployment.yaml
```

---

## Task 7. Expose ResNet50 as a Kubernetes Service
```bash
kubectl apply -f tfserving-canary/resnet50-service.yaml
```

---

## Task 8. Install Istio Ingress Gateway
```bash
kubectl apply -f tfserving-canary/ingress-gateway.yaml
```

Check gateway URL:
```bash
export GATEWAY_URL=$(kubectl get svc istio-ingressgateway -n istio-system   -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo $GATEWAY_URL
```

---

## Task 9. Test access to ResNet50
```bash
curl -d @tfserving-canary/payloads/request-body.json   -X POST http://$GATEWAY_URL/v1/models/image_classifier:predict
```

---

## Task 10. Deploy ResNet101 (Canary release)
```bash
kubectl apply -f tfserving-canary/resnet101-configmap.yaml
kubectl apply -f tfserving-canary/resnet101-deployment.yaml
kubectl apply -f tfserving-canary/resnet101-service.yaml
```

---

## Task 11. Configure weighted load balancing (70/30 split)
```bash
kubectl apply -f tfserving-canary/virtualservice-7030.yaml
```

Test again:
```bash
for i in {1..10}; do
  curl -d @tfserving-canary/payloads/request-body.json     -X POST http://$GATEWAY_URL/v1/models/image_classifier:predict
  echo -e "\n---"
done
```

---

## References
- [Google Cloud Qwiklabs](https://www.cloudskillsboost.google/)  
- [TensorFlow Serving](https://www.tensorflow.org/tfx/guide/serving)  
- [Istio Traffic Management](https://istio.io/latest/docs/tasks/traffic-management/)  
