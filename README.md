# 📦 Inventory Manager – Serverless AWS Application

A modern **Inventory Management Web Application** built with **HTML, CSS, and Vanilla JavaScript**, powered by a fully **serverless backend on AWS**.

This project demonstrates how to build and deploy a production-style CRUD application using **Amazon API Gateway** and **AWS Lambda** without managing any servers.

---

## 🚀 Features

- ➕ Add new inventory items  
- ✏️ Edit existing items (inline update)  
- 🗑 Delete items  
- 📤 Import inventory via CSV  
- ⬇️ Export inventory as CSV  
- 📱 Responsive UI design  
- ☁️ Fully serverless backend  

---

## 🏗️ Architecture Overview

This project uses the following AWS services:

- Amazon Web Services (AWS)
- Amazon API Gateway
- AWS Lambda

### Backend API

All routes are integrated with a single Lambda function:

---

## 🔌 API Endpoints

| Method | Route | Description |
|--------|--------|-------------|
| GET | /items | Get all inventory items |
| POST | /items | Create new item |
| PATCH | /items/{id} | Update existing item |
| DELETE | /items/{id} | Delete item |
| POST | /import | Import CSV file |
| GET | /export | Export CSV file |

All routes are integrated with AWS Lambda via API Gateway.

---

## 🖥️ Frontend

The frontend is a single-page application built using:

- HTML5  
- CSS3  
- Vanilla JavaScript (Fetch API)  

The frontend communicates with the backend using:

---

## 📂 CSV Import / Export

### Import
- Accepts `.csv` files
- Sends raw CSV text to `/import`
- Backend processes and stores items

### Export
- Calls `/export`
- Downloads generated CSV file from server

---

## ☁️ Serverless Design

This application follows serverless best practices:

- No EC2 servers
- No infrastructure management
- Scalable Lambda backend
- Managed API routing
- Pay-per-use pricing model

---

## 🎯 Learning Objectives

This project demonstrates:

- Building REST APIs using API Gateway
- Lambda integration (Payload Format Version 2.0)
- CRUD operations in serverless environments
- Handling file uploads (CSV import)
- Returning binary/blob responses (CSV export)
- Frontend-backend integration
- Deploying APIs in us-east-1 (N. Virginia)


---

## 📦 How to Run Locally

1. Clone the repository
2. Update the `API_BASE` URL if needed
3. Open `index.html` in your browser

---

## 🔐 Deployment Region

US East (N. Virginia) – us-east-1

---

## 🧠 Author

Khalid
