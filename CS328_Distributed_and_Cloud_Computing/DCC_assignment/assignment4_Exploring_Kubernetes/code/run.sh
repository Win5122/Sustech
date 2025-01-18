# overall
kind get clusters
kubectl config get-contexts
kubectl config use-context #add the context name
kubectl get pods -o wide

# t0
# t0-1
docker build -t flask-app:1.0.0 .
kind create cluster --name t0 --config kind-config.yaml
kubectl config use-context kind-t0
kind load docker-image flask-app:1.0.0 --name t0
kubectl apply -f t0.yaml
kubectl get pods -o wide
kubectl get svc
docker exec -it t0-control-plane /bin/bash
curl # add the http address
# t0-2
docker build -t flask-app:1.0.1 .
kind load docker-image flask-app:1.0.1 --name t0
kubectl apply -f t0.yaml
kubectl get pods -o wide
kubectl get svc
docker exec -it t0-control-plane /bin/bash
curl # add the http address

# t1
kind create cluster --name t1 --config kind-config.yaml
kubectl config use-context kind-t1
kind load docker-image flask-app:1.0.1 --name t1
kubectl apply -f t1.yaml
kubectl get pods -o wide
kubectl get svc
docker exec -it t1-control-plane /bin/bash
curl # add the http address
