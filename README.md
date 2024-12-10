# Licenta
My thesis work



**#Steps
Scalable Media Streaming Platform with CI/CD and Resilience to Congestion**

---

### **Phase 1: Planning and Foundations (January)**

#### **1. Project Scope and Design**
- Define the project goals:
  - Build a lightweight media streaming application.
  - Dockerize the application for portability.
  - Deploy it to Kubernetes (AWS EKS).
  - Integrate CI/CD for automated deployments.
  - Implement congestion simulation and mitigation.
  - Secure the platform (e.g., TLS, IAM roles).
- Write a short system architecture diagram:
  - Components: User interface (frontend), media server (backend), AWS S3 (storage), Kubernetes (deployment).

#### **2. Learn the Tools and Tech Stack**
- **AWS**: Set up an AWS account and explore the free tier.
  - Focus on: EC2 (compute), S3 (storage), IAM (security), and EKS (Kubernetes).
- **Docker**:
  - Learn to write Dockerfiles and use Docker Compose.
  - Containerize a simple app (e.g., a “Hello World” app).
- **Kubernetes**:
  - Set up a local Kubernetes cluster using Minikube or Kind.
  - Learn core concepts: pods, deployments, services.
- **CI/CD**:
  - Familiarize yourself with GitHub Actions or Jenkins.
  - Build a basic pipeline to automate builds and tests.

#### **Deliverables by January-End**:
1. A clear project plan with milestones and architecture diagram.
2. Basic proficiency in Docker, Kubernetes, AWS, and CI/CD tools.

---

### **Phase 2: Build the Core Application (February)**

#### **1. Develop the Streaming Application**
- **Backend**:
  - Build a simple Python or Node.js server to handle file uploads/downloads (media files).
  - Use AWS S3 to store and retrieve media files.
- **Frontend**:
  - Create a basic web interface for users to upload and play media files (HTML/CSS/JavaScript or React).
- **Testing Locally**:
  - Run the application locally and ensure the backend can serve files to the frontend.

#### **2. Containerize the Application**
- Write a **Dockerfile** for both the backend and frontend.
- Use Docker Compose to orchestrate the services locally.

#### **Deliverables by February-End**:
1. A fully functional local streaming application.
2. Dockerized versions of the backend and frontend services.

---

### **Phase 3: Deploy to Kubernetes (March)**

#### **1. Set Up Kubernetes Environment**
- Use **AWS EKS** for a production-grade Kubernetes cluster.
- Create Kubernetes YAML files for:
  - **Deployments**: Backend and frontend.
  - **Services**: Expose the backend and frontend via NodePort or LoadBalancer.
  - **ConfigMaps/Secrets**: Manage environment variables and sensitive data.
  
#### **2. Configure AWS Services**
- Set up **S3 buckets** for media storage and configure public access (if needed).
- Create an **IAM role** for your application to securely access the S3 bucket.

#### **3. Test the Application on Kubernetes**
- Deploy the Dockerized app to EKS.
- Test functionality (uploading, streaming) in the cloud environment.
- Use **kubectl** to monitor pods and troubleshoot issues.

#### **Deliverables by March-End**:
1. Streaming app running on Kubernetes (AWS EKS).
2. Kubernetes manifests (YAML files) for deployments and services.
3. AWS resources (S3, IAM roles) properly integrated.

---

### **Phase 4: Add CI/CD and Optimize for Congestion (April)**

#### **1. Implement CI/CD Pipeline**
- Use **GitHub Actions** or **Jenkins** to:
  - Build and test Docker images automatically on code commits.
  - Push images to a container registry (Docker Hub or AWS ECR).
  - Deploy updated images to Kubernetes automatically.
- Add automated unit tests for the backend.

#### **2. Simulate and Handle Congestion**
- Use **Apache JMeter** or **Locust** to simulate heavy traffic.
- Monitor resource usage with **AWS CloudWatch** or **Kubernetes metrics server**.
- Optimize the system:
  - Use Kubernetes **Horizontal Pod Autoscaler** to scale pods dynamically.
  - Configure **AWS ELB (Elastic Load Balancer)** for better traffic distribution.

#### **Deliverables by April-End**:
1. CI/CD pipeline operational (code → Docker image → deployment).
2. System optimized for traffic (autoscaling, load balancing).
3. Congestion simulations documented with metrics and results.

---

### **Phase 5: Finalize and Document (May)**

#### **1. Security Enhancements**
- Secure communication:
  - Use **HTTPS** with TLS (e.g., Let’s Encrypt for certificates).
  - Ensure AWS S3 access is encrypted and authenticated.
- Harden the infrastructure:
  - Use IAM policies with least privilege for AWS services.
  - Scan Docker images for vulnerabilities (e.g., **Trivy**).

#### **2. Write the Thesis**
- **Structure**:
  1. **Introduction**:
     - Problem statement (scalability, congestion management).
     - Objectives and relevance (DevOps practices, cloud technologies).
  2. **Literature Review**:
     - Discuss related work in scalable streaming systems and DevOps.
  3. **Implementation**:
     - Explain architecture, tools used (Docker, Kubernetes, AWS).
     - Detail CI/CD pipeline, congestion simulation, and security measures.
  4. **Results**:
     - Metrics from congestion tests.
     - Screenshots of deployments, CI/CD pipeline, and AWS configurations.
  5. **Conclusion**:
     - Lessons learned, challenges faced, and future improvements.
- Include visuals like architecture diagrams, Kubernetes YAML snippets, and test results.

#### **3. Prepare for the Demo**
- Deploy the final version of the application.
- Create a script to demonstrate:
  - CI/CD pipeline triggering on code changes.
  - Scaling pods under traffic.
  - Secure file uploads and downloads.

#### **Deliverables by May-End**:
1. Completed thesis document (~50-70 pages).
2. Fully functioning demo of the streaming platform.
3. Presentation slides with visuals and key insights.

---

### **Key Success Factors**
1. **Stay on Schedule**: Allocate ~10-15 hours per week 
2. **Iterate Early**: Test components 
3. **Seek Feedback**: Regularly update
4. **Use Free Resources**: Stick to the AWS free tier and local tools (e.g., Minikube) 

