## Based on:
https://github.com/bangkit-pukulrata/machine-learning/tree/main/model <br>
https://github.com/tantowjy/news-classification/blob/main/website/main.py

## Dataset
Dataset LLM: https://www.kaggle.com/datasets/iqbalmaulana/indonesian-news-dataset
<br>
Dataset NER: https://github.com/yohanesgultom/nlp-experiments/blob/master/data/ner/training_data.txt <br>

# TALAS API Documentation

## Overview
TALAS adalah sistem berbasis API untuk menganalisis berita menggunakan model pembelajaran mesin, termasuk analisis bias, deteksi hoaks, deteksi ideologi, pengelompokan, dan entitas bernama. API ini dibangun dengan layanan Google Cloud Platform (GCP) menggunakan **App Engine** untuk komputasi, **Cloud SQL (MySQL)** untuk penyimpanan data pengguna, dan model pembelajaran mesin (supervised & unsupervised learning).

## Routes.py Endpoint Production\machine-learning\app\routes.py
### 1. **Bias Detection Endpoint**
- **URL**: `/bias`
- **Method**: POST
- **Description**: Processes text to determine the bias of a news article.
- **Request**:
  ```json
  {
      "content": "string" // Content of the news article
  }
  ```
- **Response**:
  ```json
  {
      "bias": 0 // Not bias or Bias (0 or 1)
  }
  ```

---

### 2. **Hoax Detection Endpoint**
- **URL**: `/hoax`
- **Method**: POST
- **Description**: Processes text to determine if the article contains hoaxes.
- **Request**:
  ```json
  {
      "content": "string" // Content of the news article
  }
  ```
- **Response**:
  ```json
  {
      "hoax": "float" // Hoax probability (0 to 1)
  }
  ```

---

### 3. **Ideology Detection Endpoint**
- **URL**: `/ideology`
- **Method**: POST
- **Description**: Processes text to determine the ideology of a news article.
- **Request**:
  ```json
  {
      "content": "string" // Content of the news article
  }
  ```
- **Response**:
  ```json
  {
      "ideology": 0 // 0 or 1, "liberal" or "conservative"
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
- **Description**: Mencari cluster mayoritas dari kumpulan artikel berita.
- **Request**:
  ```json
  [
      {
          "title": "string", // Judul artikel
          "content": "string", // Isi artikel
      },
      {
          "title": "string", // Judul artikel
          "content": "string", // Isi artikel
      },
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
      },
      {
          "title": "string", // Judul artikel
          "content": "string", // Isi artikel
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
- **URL**: `/summary`
- **Method**: POST
- **Description**: Membuat dua ringkasan (liberal dan konservatif) dari kumpulan artikel berita.
- **Request**:
  ```json
  [
      {
          "title": "string", // Judul artikel
          "content": "string", // Isi artikel
      },
      {
          "title": "string", // Judul artikel
          "content": "string", // Isi artikel
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

### 4. **Generate Analysis Endpoint**
- **URL**: `/analyze`
- **Method**: POST
- **Description**: Menghasilkan analisis perbandingan perspektif liberal dan konservatif.
- **Request**:
  ```json
  [
      {
          "title": "string", // Judul artikel
          "content": "string", // Isi artikel
      },
      {
          "title": "string", // Judul artikel
          "content": "string", // Isi artikel
      }
  ]
  ```
- **Response**:
  ```json
  {
      "analyze": "string" // Analisis dari dua perspektif berbeda
  }
  ```

---

### 5. **Clean Text Endpoint**
- **URL**: `/cleaned`
- **Method**: POST
- **Description**: Membersihkan teks berita dengan menghapus stopwords dan melakukan stemming.
- **Request**:
  ```json
  {
      "content": "string" // atau ["string", "string"] untuk multiple teks
  }
  ```
- **Response**:
  ```json
  {
      "cleaned": "string" // atau ["string", "string"] jika input adalah array
  }
  ```

---

### 6. **Separate Articles Endpoint**
- **URL**: `/separate`
- **Method**: POST
- **Description**: Memisahkan artikel berdasarkan kesamaan konten menggunakan similaritas embedding.
- **Request**:
  ```json
  [
      {
          "title": "string",
          "content": "string",
      },
      {
          "title": "string",
          "content": "string",
      },
      {
          "title": "string",
          "content": "string",
      },
      {
          "title": "string",
          "content": "string",
      }
  ]
  ```
- **Response**:
  ```json
  {
      "separate": [0, 1, 0, 1] // Berita pada indeks 0 dan 2 mirip, dan diberi kode kelompok "0"
  }
  ```

---

### 7. Process All Articles
- **URL**: `/process-all`
- **Method**: POST
- **Description**: Process input text articles to group, generate titles, clusters/categories, summaries, and bias analysis for each group

#### Request Body
```json
[
  {
    "title": "string",
    "content": "string",
  },
  {
    "title": "string",
    "content": "string",
  }
]
```

#### Response Body
```json
[
  {
    "title": "Generated Group Title",
    "modeCluster": "Cluster/Category Name",
    "summary_liberalism": "Liberal perspective summary",
    "summary_conservative": "Conservative perspective summary",
    "analyze": "Bias and content analysis details"
  }
]
```

---

### 8. **Antipode Articles Endpoint**
- **URL**: `/antipode`
- **Method**: POST
- **Description**: Menemukan artikel dengan sudut pandang yang berlawanan dari artikel yang diberikan.
- **Request**:
  ```json
  {
      "article": {
          "title": "string",
          "content": "string",
      },
      "df": [
          {
              "title": "string",
              "content": "string"
          }
      ]
  }
  ```
- **Response**:
  ```json
  ["Judul Artikel 1", "Judul Artikel 2"] // Judul artikel dengan sudut pandang berlawanan
  ```

---

## Named Entity Recognition (NER)
### 1. **NER API Endpoint**
- **URL**: `/ner`
- **Method**: POST
- **Description**: Mendeteksi entitas bernama dalam teks menggunakan model NER.
- **Request**:
  ```json
  [
      {
          "content": "string" // Teks yang akan dianalisis
      }
  ]
  ```
- **Response**:
  ```json
  [
      [
          {"word": "entity", "tag": "B-PER"}
      ]
  ] // Daftar entitas yang terdeteksi untuk setiap teks
  ```

---

### 2. **Top Keywords Endpoint**
- **URL**: `/top_keywords`
- **Method**: POST
- **Description**: Menemukan kata kunci yang paling sering muncul dari beberapa artikel (kata kunci dideteksi dari NER)
- **Request**:
  ```json
  [
      {
          "keyword": ["string", "string"]
      }
  ]
  ```
- **Response**:
  ```json
  [
      ["keyword1", 10],
      ["keyword2", 7]
  ] // Pasangan kata kunci dan jumlah kemunculan
  ```

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
```

## Database Endpoints Production\machine-learning\app\db.py

### 1. **Fetch Users**
- **URL**: `/users`
- **Method**: GET
- **Description**: Fetches a list of MySQL users.
- **Response**:
  ```json
  [
      {
          "user": "string",
          "host": "string"
      }
  ]
  ```

---

### 2. **Fetch News**
- **URL**: `/news`
- **Method**: GET
- **Description**: Fetches a list of news articles from the database.
- **Response**:
  ```json
  {
      "success": true,
      "data": [
          {
              "id": "integer",
              "title": "string",
              "source": "string",
              "url": "string",
              "image": "string",
              "content": "string",
              "embedding": "string",
              "cleaned": "string",
              "title_index": "integer",
              "cluster": "integer",
              "bias": "integer",
              "hoax": "float",
              "ideology": "integer"
          }
      ]
  }
  ```

---

### 3. **Test Database Connection**
- **URL**: `/test-connection`
- **Method**: GET
- **Description**: Tests the connection to the database and retrieves the list of tables.
- **Response**:
  ```json
  {
      "success": true,
      "tables": [
          {"Tables_in_news": "string"}
      ]
  }
  ```

---

### 4. **News Page**
- **URL**: `/news_page`
- **Method**: GET
- **Description**: Fetches news articles with optional date filtering and renders them in an HTML page.
- **Query Parameters**:
  - `start_date`: Start date for filtering (optional).
  - `end_date`: End date for filtering (optional).
- **Response**: Renders an HTML page with news articles.

---

### 5. **News Article**
- **URL**: `/news_article`
- **Method**: GET
- **Description**: Fetches details of a specific news article and renders it in an HTML page.
- **Query Parameters**:
  - `title_index`: The index of the article to fetch.
- **Response**: Renders an HTML page with the article details.

---

### 6. **Insert News Page**
- **URL**: `/insert_news_page`
- **Method**: GET
- **Description**: Renders a page for inserting news articles.
- **Response**: Renders an HTML page for inserting news.

---

### 7. **Insert Title**
- **URL**: `/insert-title`
- **Method**: POST
- **Description**: Inserts a new title into the database.
- **Request**:
  ```json
  {
      "title": "string",
      "cluster": "string",
      "image": "string",
      "date": "string",
      "summary_liberalism": "string",
      "summary_conservative": "string",
      "analysis": "string"
  }
  ```
- **Response**:
  ```json
  {
      "success": true,
      "message": "Article inserted successfully",
      "title": {
          "title": "string",
          "cluster": "string",
          "image": "string",
          "date": "string",
          "title_index": "integer"
      }
  }
  ```

---

### 8. **Insert Article**
- **URL**: `/insert-article`
- **Method**: POST
- **Description**: Inserts a new article into the database.
- **Request**:
  ```json
  {
      "title": "string",
      "source": "string",
      "url": "string",
      "image": "string",
      "date": "string",
      "content": "string"
  }
  ```
- **Response**:
  ```json
  {
      "success": true,
      "message": "Article inserted successfully",
      "article": {
          "id": "integer",
          "title": "string",
          "source": "string",
          "url": "string",
          "image": "string",
          "date": "string"
      }
  }
  ```
