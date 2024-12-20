# Coworking Space Service Extension
The Coworking Space Service is a set of APIs that enables users to request one-time tokens and administrators to authorize access to a coworking space. This service follows a microservice pattern and the APIs are split into distinct services that can be deployed and managed independently of one another.

For this project, you are a DevOps engineer who will be collaborating with a team that is building an API for business analysts. The API provides business analysts basic analytics data on user activity in the service. The application they provide you functions as expected locally and you are expected to help build a pipeline to deploy it in Kubernetes.

## Getting Started

### Dependencies
#### Local Environment
1. Python Environment - run Python 3.6+ applications and install Python dependencies via `pip`
2. Docker CLI - build and run Docker images locally
3. `kubectl` - run commands against a Kubernetes cluster
4. `helm` - apply Helm Charts to a Kubernetes cluster

#### Remote Resources
1. AWS CodeBuild - build Docker images remotely
2. AWS ECR - host Docker images
3. Kubernetes Environment with AWS EKS - run applications in k8s
4. AWS CloudWatch - monitor activity and logs in EKS
5. GitHub - pull and clone code

### Setup
#### 1. Configure a Database
Set up a Postgres database using a Helm Chart.

1. Set up Bitnami Repo
```bash
helm repo add <REPO_NAME> https://charts.bitnami.com/bitnami
```

2. Install PostgreSQL Helm Chart
```
helm install <SERVICE_NAME> <REPO_NAME>/postgresql
```

This should set up a Postgre deployment at `<SERVICE_NAME>-postgresql.default.svc.cluster.local` in your Kubernetes cluster. You can verify it by running `kubectl svc`

By default, it will create a username `postgres`. The password can be retrieved with the following command:
```bash
export POSTGRES_PASSWORD=$(kubectl get secret --namespace default <SERVICE_NAME>-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d)

echo $POSTGRES_PASSWORD
```

<sup><sub>* The instructions are adapted from [Bitnami's PostgreSQL Helm Chart](https://artifacthub.io/packages/helm/bitnami/postgresql).</sub></sup>

3. Test Database Connection
The database is accessible within the cluster. This means that when you will have some issues connecting to it via your local environment. You can either connect to a pod that has access to the cluster _or_ connect remotely via [`Port Forwarding`](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/)

* Connecting Via Port Forwarding
```bash
kubectl port-forward --namespace default svc/<SERVICE_NAME>-postgresql 5432:5432 &
    PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U postgres -d postgres -p 5432
```

* Connecting Via a Pod
```bash
kubectl exec -it <POD_NAME> bash
PGPASSWORD="<PASSWORD HERE>" psql postgres://postgres@<SERVICE_NAME>:5432/postgres -c <COMMAND_HERE>
```

4. Run Seed Files
We will need to run the seed files in `db/` in order to create the tables and populate them with data.

```bash
kubectl port-forward --namespace default svc/<SERVICE_NAME>-postgresql 5432:5432 &
    PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U postgres -d postgres -p 5432 < <FILE_NAME.sql>
```

### 2. Running the Analytics Application Locally
In the `analytics/` directory:

1. Install dependencies
```bash
pip install -r requirements.txt
```
2. Run the application (see below regarding environment variables)
```bash
<ENV_VARS> python app.py
```

There are multiple ways to set environment variables in a command. They can be set per session by running `export KEY=VAL` in the command line or they can be prepended into your command.

* `DB_USERNAME`
* `DB_PASSWORD`
* `DB_HOST` (defaults to `127.0.0.1`)
* `DB_PORT` (defaults to `5432`)
* `DB_NAME` (defaults to `postgres`)

If we set the environment variables by prepending them, it would look like the following:
```bash
DB_USERNAME=username_here DB_PASSWORD=password_here python app.py
```
The benefit here is that it's explicitly set. However, note that the `DB_PASSWORD` value is now recorded in the session's history in plaintext. There are several ways to work around this including setting environment variables in a file and sourcing them in a terminal session.

3. Verifying The Application
* Generate report for check-ins grouped by dates
`curl <BASE_URL>/api/reports/daily_usage`

* Generate report for check-ins grouped by users
`curl <BASE_URL>/api/reports/user_visits`

## Project Instructions
1. Set up a Postgres database with a Helm Chart
2. Create a `Dockerfile` for the Python application. Use a base image that is Python-based.
3. Write a simple build pipeline with AWS CodeBuild to build and push a Docker image into AWS ECR
4. Create a service and deployment using Kubernetes configuration files to deploy the application
5. Check AWS CloudWatch for application logs

### Deliverables
1. `Dockerfile`
2. Screenshot of AWS CodeBuild pipeline
3. Screenshot of AWS ECR repository for the application's repository
4. Screenshot of `kubectl get svc`
5. Screenshot of `kubectl get pods`
6. Screenshot of `kubectl describe svc <DATABASE_SERVICE_NAME>`
7. Screenshot of `kubectl describe deployment <SERVICE_NAME>`
8. All Kubernetes config files used for deployment (ie YAML files)
9. Screenshot of AWS CloudWatch logs for the application
10. `README.md` file in your solution that serves as documentation for your user to detail how your deployment process works and how the user can deploy changes. The details should not simply rehash what you have done on a step by step basis. Instead, it should help an experienced software developer understand the technologies and tools in the build and deploy process as well as provide them insight into how they would release new builds.


### Stand Out Suggestions
Please provide up to 3 sentences for each suggestion. Additional content in your submission from the standout suggestions do _not_ impact the length of your total submission.
1. Specify reasonable Memory and CPU allocation in the Kubernetes deployment configuration
2. In your README, specify what AWS instance type would be best used for the application? Why?
3. In your README, provide your thoughts on how we can save on costs?

### Best Practices
* Dockerfile uses an appropriate base image for the application being deployed. Complex commands in the Dockerfile include a comment describing what it is doing.
* The Docker images use semantic versioning with three numbers separated by dots, e.g. `1.2.1` and  versioning is visible in the  screenshot. See [Semantic Versioning](https://semver.org/) for more details.

### setup start project:
1. Create cluster:
   1. `eksctl create cluster --name namht4-cluster-1 --region us-east-1 --nodegroup-name namht4-nodes-1 --node-type t3.small --nodes 2 --nodes-min 2 --nodes-max 3
      `
   2. `aws eks update-kubeconfig --region us-east-1 --name namht4-cluster-1`
2. Create ECR: `aws ecr create-repository --repository-name namht4-repo-github --region us-east-1`
3. install helm bitnami: 
   1. `helm repo add bitnami https://charts.bitnami.com/bitnami`
   2. `helm repo update`
4. install PostgresSQL: `helm install prj3 bitnami/postgresql --set primary.persistence.enabled=false`
5. Forward port database:
   1. `kubectl get svc`
   2. `kubectl port-forward --namespace default svc/namhtpsqlproject3-postgresql 5434:5432 &`
   3. `export POSTGRES_PASSWORD=$(kubectl get secret --namespace default <SERVICE_NAME>-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d)`
   4. `echo $POSTGRES_PASSWORD`
   5. `PGPASSWORD="$POSTGRES_PASSWORD" psql -U postgres -d postgres -h 127.0.0.1 -a -f db/1_create_tables.sql`
   6. `PGPASSWORD="$POSTGRES_PASSWORD" psql -U postgres -d postgres -h 127.0.0.1 -a -f db/2_seed_users.sql`
   7. `PGPASSWORD="$POSTGRES_PASSWORD" psql -U postgres -d postgres -h 127.0.0.1 -a -f db/3_seed_tokens.sql`
6. commit code and Build code
7. copy image at ERC
8. deploy project: 
   1. run: `cd/deployment`
   2. run: `kubectl apply -f .`
   3. run export host: `kubectl expose deployment coworking --type=LoadBalancer --name=coworking-ep-new --port=5153 --target-port=5153
      ` 
## Setup CloudWatch
1. update role EKS cluster:
    - Go to EKS and copy the role name
    - run `aws iam attach-role-policy \
      --role-name eksctl-namht4-cluster-1-nodegroup--NodeInstanceRole-sjIib9wfZJsn \
      --policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy`
2. create trigger CloudWatch
  - run `aws eks create-addon --addon-name amazon-cloudwatch-observability --cluster-name namht4-cluster-1`

### **Note: All images related to APIs, logs, and commands are located in the "image" folder.
1. API user_visits: http://a36e6ad31f6904f1a9bb15b761b39efb-2045902427.us-east-1.elb.amazonaws.com:5153/api/reports/user_visits
2. API daily_usage: http://a36e6ad31f6904f1a9bb15b761b39efb-2045902427.us-east-1.elb.amazonaws.com:5153/api/reports/daily_usage
3. API readiness_check: http://a36e6ad31f6904f1a9bb15b761b39efb-2045902427.us-east-1.elb.amazonaws.com:5153/readiness_check
4. API health_check: http://a36e6ad31f6904f1a9bb15b761b39efb-2045902427.us-east-1.elb.amazonaws.com:5153/health_check
**