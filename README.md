1. adding ingress controller:
`kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.2/deploy/static/provider/cloud/deploy.yaml`

2. adding secret:
`kubectl apply -f secret.yaml`

3. adding configMap:
`kubectl apply -f configMap.yaml`

4. creating ingress:
`kubectl apply -f ingress.yaml`

5. deploy:
`kubectl apply -f deploy.yaml`

6. check login IP:
`kubectl get svc -n ingress-nginx`  ####maybe use hostname later

7. login:
`http://<EXTERNAL-IP>/auth`

`username: admin`
`password: 3495admin`

