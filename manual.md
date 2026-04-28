
# Deploy Uptime Kuma

## Prerequisites

- [CLI access](cli-kubeconfig.md) configured — `kubectl` working against your project

Verify your setup:

```bash
# Confirm you're connected to the right project
kube-dc ns
```

---

## Step 1: Create a TLS Certificate Issuer

Before deploying, set up a Let's Encrypt issuer so your app gets a free HTTPS certificate automatically.

```bash
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: letsencrypt
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-account-key
    solvers:
    - http01:
        gatewayHTTPRoute:
          parentRefs:
          - group: gateway.networking.k8s.io
            kind: Gateway
            name: eg
            namespace: envoy-gateway-system
EOF
```

:::note One-time setup
You only need to create the Issuer once per project. All services in the project can reuse it.
:::

---

## Step 2: Configure deployment

```bash
cat <<EOF | kubectl apply -f - 
apiVersion: apps/v1
kind: Deployment
metadata:
  name: uptime-kuma
spec:
  replicas: 1
  selector:
    matchLabels:
      app: uptime-kuma
  template:
    metadata:
      labels:
        app: uptime-kuma
    spec:
      securityContext:
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
      containers:
        - name: uptime-kuma
          image: louislam/uptime-kuma:2-slim-rootless
          env:
            - name: UPTIME_KUMA_BASE_URL
              # Replace with your actual Kube-DC URL
              value: "https://uptime-kuma-service-{your-namespace}.apps.kube-dc.com"
          ports:
            - containerPort: 3001
          volumeMounts:
            - name: kuma-data
              mountPath: /app/data
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
      volumes:
        - name: kuma-data
          persistentVolumeClaim:
            claimName: uptime-kuma-pvc

```

# Step 3: Create PVC

```bash
cat <<EOF | kubectl apply -f - 

apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: uptime-kuma-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi # Configure desired size here 
```

# Step 4: Configure Load-balancer service

```bash
cat <<EOF | kubectl apply -f - 

apiVersion: v1
kind: Service
metadata:
  name: my-app
  annotations:
    service.nlb.kube-dc.com/expose-route: "https"
spec:
  type: LoadBalancer
  selector:
    app: uptime-kuma # Must match the label in your Deployment
  ports:
    - name: http
      port: 80 
      targetPort: 3001 # IMPORTANT: Must be 3001 for Uptime Kuma
      protocol: TCP
```

# Step 5: Verify

```bash
# Check assigned hostname
kubectl get svc my-app -n my-project -o jsonpath='{.metadata.annotations.service\.nlb\.kube-dc\.com/route-hostname-status}'
# Output: my-app-my-project.stage.kube-dc.com

# Check certificate status
kubectl get certificate -n my-project

# Test access
curl https://my-app-my-project.stage.kube-dc.com
```

# Step 6: Configure uptime-kuma

In browser, open `my-app-my-project.stage.kube-dc.com`.
Select *SQLite*.
Create username and password.
Access the dashboard and add desired websites.
