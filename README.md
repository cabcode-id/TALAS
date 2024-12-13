Based on:
https://github.com/bangkit-pukulrata/machine-learning/tree/main/model
https://github.com/tantowjy/news-classification/blob/main/website/main.py

Dataset LLM: 
https://www.kaggle.com/datasets/iqbalmaulana/indonesian-news-dataset

# TALAS API Documentation

## Overview
TALAS adalah sistem berbasis API untuk menganalisis berita menggunakan model pembelajaran mesin, termasuk analisis bias, deteksi hoaks, deteksi ideologi, pengelompokan, dan entitas bernama. API ini dibangun dengan layanan Google Cloud Platform (GCP) menggunakan **App Engine** untuk komputasi, **Cloud SQL (MySQL)** untuk penyimpanan data pengguna, dan model pembelajaran mesin (supervised & unsupervised learning).

## Endpoints
### 1. **Bias Detection Endpoint**
- **URL**: `/bias`
- **Method**: POST
- **Description**: Memproses teks untuk menentukan bias artikel berita.
- **Request**:
  ```json
  {
      "content": "string" // Isi artikel berita
  }
  ```
- **Response**:
  ```json
  {
      "bias": 0 // Kategori bias (0 atau 1)
  }
  ```

---

### 2. **Hoax Detection Endpoint**
- **URL**: `/hoax`
- **Method**: POST
- **Description**: Memproses teks untuk menentukan apakah artikel tersebut mengandung hoaks.
- **Request**:
  ```json
  {
      "content": "string" // Isi artikel berita
  }
  ```
- **Response**:
  ```json
  {
      "hoax": 0.85 // Tingkat hoaks (0 hingga 1)
  }
  ```

---

### 3. **Ideology Detection Endpoint**
- **URL**: `/ideology`
- **Method**: POST
- **Description**: Memproses teks untuk menentukan ideologi artikel berita.
- **Request**:
  ```json
  {
      "content": "string" // Isi artikel berita
  }
  ```
- **Response**:
  ```json
  {
      "ideology": 1 // Ideologi artikel (0 = konservatif, 1 = liberal)
  }
  ```

---

## Unsupervised Learning Models
### 1. **Cluster Endpoint**
- **URL**: `/cluster`
- **Method**: POST
- **Description**: Mengelompokkan teks ke dalam cluster tertentu berdasarkan isinya.
- **Request**:
  ```json
  {
      "content": "string" // Isi artikel berita
  }
  ```
- **Response**:
  ```json
  {
      "cluster": 3 // Cluster artikel (0-7)
  }
  ```

---

### 2. **Generate Mode Cluster**
- **URL**: `/modeCluster`
- **Method**: POST
- **Description**: Mencari cluster yang paling umum dari kumpulan artikel berita.
- **Request**:
  ```json
  [
      {
          "title": "string", // Judul artikel
          "content": "string", // Isi artikel
          "embedding": [0.1, 0.2] // Representasi embedding
      }
  ]
  ```
- **Response**:
  ```json
  {
      "modeCluster": 2 // Cluster yang paling umum
  }
  ```

---

## Large Language Model (LLM)
### 1. **Generate Embedding Endpoint**
- **URL**: `/embedding`
- **Method**: POST
- **Description**: Menghasilkan embedding untuk teks yang diberikan.
- **Request**:
  ```json
  [
      {
          "title": "string", // Judul artikel
          "content": "string" // Isi artikel
      }
  ]
  ```
- **Response**:
  ```json
  {
      "embedding": [[0.1, 0.2]] // Daftar embedding
  }
  ```

---

### 2. **Generate Title Endpoint**
- **URL**: `/title`
- **Method**: POST
- **Description**: Menghasilkan judul dari kumpulan artikel berita.
- **Request**:
  ```json
  [
      {
          "title": "string", // Judul artikel
          "content": "string", // Isi artikel
          "embedding": [0.1, 0.2] // Representasi embedding
      }
  ]
  ```
- **Response**:
  ```json
  {
      "title": "Generated Title" // Judul yang dihasilkan
  }
  ```

---

### 3. **Generate Summary Endpoint**
- **URL**: `/summarize`
- **Method**: POST
- **Description**: Membuat dua ringkasan (liberal dan konservatif) dari kumpulan artikel berita.
- **Request**:
  ```json
  [
      {
          "title": "string", // Judul artikel
          "content": "string", // Isi artikel
          "embedding": [0.1, 0.2] // Representasi embedding
      }
  ]
  ```
- **Response**:
  ```json
  {
      "summary_liberalism": "string", // Ringkasan liberal
      "summary_conservative": "string" // Ringkasan konservatif
  }
  ```

---

## Named Entity Recognition (NER)
### 1. **Main NER Page**
- **URL**: `/`
- **Method**: GET
- **Description**: Menampilkan halaman utama untuk input artikel dan analisis NER.
- **Response**:
  - 200 OK: Menampilkan halaman `ner_home.html`.

---

### 2. **Text Processing**
- **URL**: `/process`
- **Method**: POST
- **Description**: Memproses teks menggunakan model spaCy untuk mendeteksi entitas.
- **Request**:
  - Form Data:
    ```
    input_data: "string" // Artikel atau teks untuk dianalisis
    ```
- **Response**:
  - 200 OK: Mengembalikan hasil analisis entitas dalam format HTML.

---

## Authentication
### 1. **Login**
- **URL**: `/process-login`
- **Method**: POST
- **Request Body**:
  ```json
  {
      "email": "string",
      "password": "string"
  }
  ```
- **Response**:
  ```json
  {
      "auth": true,
      "token": "string"
  }
  ```

---

### 2. **Register**
- **URL**: `/process-regist`
- **Method**: POST
- **Request Body**:
  ```json
  {
      "username": "string",
      "email": "string",
      "password": "string"
  }
  ```
- **Response**:
  - 200 OK:
    ```json
    {
        "message": "Data berhasil disimpan"
    }
    ```
  - 500 Internal Server Error:
    ```json
    {
        "message": "Terjadi kesalahan"
    }
    ```

## News Endpoints

### 1. Fetch News List
- **URL**: `/article/news`
- **Method**: GET
- **Description**: Retrieve a list of news articles

#### Responses
- **200 OK**
  ```json
  {
    "message": "Data fetched successfully",
    "data": []
  }
  ```
- **500 Internal Server Error**
  ```json
  {
    "message": "Internal server error"
  }
  ```

### 2. Get News Content
- **URL**: `/article/:title`
- **Method**: GET
- **Description**: Retrieve content for a specific news article

#### Responses
- **200 OK**
  ```json
  {
    "message": "Content fetched successfully",
    "data": []
  }
  ```
- **500 Internal Server Error**
  ```json
  {
    "message": "Internal server error"
  }
  ```

## Crawler Endpoints

### 1. Run General Crawler
- **URL**: `https://talas24.et.r.appspot.com/api/crawler/general`
- **Method**: GET
- **Description**: Run general crawler to update news data in the database

#### Response
```json
{
  "message": "News updated successfully from general crawler"
}
