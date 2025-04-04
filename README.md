1. adding ingress controller:
`kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.2/deploy/static/provider/cloud/deploy.yaml`

2. adding namespace: 
`kubectl apply -f n.yaml`

3. adding secret:
`kubectl apply -f secret.yaml`

4. adding configMap:
`kubectl apply -f configMap.yaml`

5. creating ingress:
`kubectl apply -f ingress.yaml`

6. deploy:
`kubectl apply -f deploy.yaml`

7. check login IP:
`kubectl get svc -n ingress-nginx`  ####maybe use hostname later

8. login:
`http://<EXTERNAL-IP>/auth`

`username: admin`
`password: 3495admin`

9.  test with test pod:  
  1). `kubectl run --rm -it apache-bench --image httpd -- bash`
  
  2). `echo '{"student_id": "1001", "subject": "Mathematics", "grade": 85, "receive_time": "2025-01-08T09:12:33.00111"}' > data.json`
  
  3). `ab -n 500 -c 100 -p data.json -T "application/json" http://storage:5020/submit_grade`
