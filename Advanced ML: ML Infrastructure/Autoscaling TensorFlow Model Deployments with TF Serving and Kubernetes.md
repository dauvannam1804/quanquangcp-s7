# Autoscaling TensorFlow Model Deployments with TF Serving and Kubernetes

**Experiment Type:** Lab  
**Duration:** 1 hour 30 minutes  
**Credits:** 5  
**Level:** Intermediate  
**ID:** GSP777  

---

## Overview
Serving deep learning models is challenging because models are large (gigabytes of memory) and compute-intensive (a few concurrent requests can fully utilize a CPU/GPU).  
Automatic horizontal scaling is a key strategy to build scalable and reliable infrastructures for deep learning model serving.

In this lab, you will use **TensorFlow Serving** and **Google Kubernetes Engine (GKE)** to configure a high-performance, autoscalable serving system for TensorFlow models.

---

## Objectives
You will learn to:

- Configure a GKE cluster with an autoscaling node pool.  
- Deploy TensorFlow Serving in an autoscalable configuration.  
- Monitor serving performance and resource utilization.  

---

## Prerequisites
You should understand:

- How to save and load TensorFlow models.  
- Basic Kubernetes concepts and architecture.  

Recommended resources:  
- [Using the SavedModel format](https://www.tensorflow.org/guide/saved_model)  
- [Kubernetes Overview](https://kubernetes.io/docs/concepts/overview/)  

---

## Lab Scenario
You will deploy the **ResNet101** model using TensorFlow Serving on GKE.  
- TensorFlow Serving provides flexible, high-performance serving for ML models in production.  
- It integrates seamlessly with TensorFlow models but can serve other formats.  
- You’ll use **Horizontal Pod Autoscaler (HPA)** to scale pods based on CPU utilization and **Cluster Autoscaler** to scale nodes automatically.  
- Load testing will be performed with **Locust**.  

---

## Tasks Summary
1. Create a GKE cluster with autoscaling enabled.  
2. Deploy the pretrained ResNet101 model using TensorFlow Serving.  
3. Configure Horizontal Pod Autoscaler.  
4. Install Locust.  
5. Load the ResNet101 model.  
6. Monitor the deployment.  

---

## Setup and Requirements
- Use Chrome in Incognito mode (recommended).  
- Labs are timed, cannot be paused.  
- You will receive temporary student credentials—**do not use your personal Google Cloud account**.  
- Cloud Shell will be used for command execution.  

---

## Lab Tasks

### Task 1. Get Lab Files
```bash
cd
SRC_REPO=https://github.com/GoogleCloudPlatform/mlops-on-gcp
kpt pkg get $SRC_REPO/workshops/mlep-qwiklabs/tfserving-gke-autoscaling tfserving-gke
cd tfserving-gke
```

### Task 2. Create a GKE Cluster
```bash
gcloud config set compute/zone ZONE
PROJECT_ID=$(gcloud config get-value project)
CLUSTER_NAME=cluster-1

gcloud beta container clusters create $CLUSTER_NAME   --cluster-version=latest   --machine-type=e2-standard-4   --enable-autoscaling   --min-nodes=1   --max-nodes=3   --num-nodes=1
```

Get cluster credentials:
```bash
gcloud container clusters get-credentials $CLUSTER_NAME
```

### Task 3. Deploy ResNet101
Create a bucket and copy the pretrained model:
```bash
export MODEL_BUCKET=${PROJECT_ID}-bucket
gsutil mb gs://${MODEL_BUCKET}
gsutil cp -r gs://spls/gsp777/resnet_101 gs://${MODEL_BUCKET}
```

### Task 4. Create ConfigMap
```bash
echo $MODEL_BUCKET
sed -i "s/your-bucket-name/$MODEL_BUCKET/g" tf-serving/configmap.yaml
kubectl apply -f tf-serving/configmap.yaml
```

### Task 5. Create TensorFlow Serving Deployment
```bash
kubectl apply -f tf-serving/deployment.yaml
kubectl get deployments
```

### Task 6. Expose Deployment
```bash
kubectl apply -f tf-serving/service.yaml
kubectl get svc image-classifier
```

### Task 7. Configure Horizontal Pod Autoscaler
```bash
kubectl autoscale deployment image-classifier   --cpu-percent=60   --min=1   --max=4

kubectl get hpa
```

### Task 8. Test the Model
```bash
EXTERNAL_IP=[YOUR_SERVICE_IP]
curl -d @locust/request-body.json   -X POST http://${EXTERNAL_IP}:8501/v1/models/image_classifier:predict
```

### Task 9. Install Locust
```bash
pip3 install locust==1.4.1
export PATH=~/.local/bin:$PATH
locust -V
```

### Task 10. Start Load Test
```bash
cd locust
locust -f tasks.py   --headless   --host http://${EXTERNAL_IP}:8501
```

### Task 11. Monitor Load Test
- Monitor **CPU utilization** and **replica count** in GKE dashboard.  
- Observe how autoscaling increases pods and nodes with load.  
- Verify scaling down after the test finishes.  

### Task 12. Stop Load Test
Press `Ctrl+C` in Cloud Shell to stop Locust.

---

## Congratulations 🎉
You deployed and autoscaled TensorFlow Serving with GKE for the ResNet101 model, and tested it with Locust.

---

**Last Updated:** November 07, 2024  
**Last Tested:** November 07, 2024  
**Copyright 2025 Google LLC**
