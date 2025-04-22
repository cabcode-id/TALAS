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

### Unsupervised Learning Models
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
          "embedding": numpy array 
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
          "embedding": numpy array 
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
          "embedding": numpy array 
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
          "embedding": numpy array 
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
          "embedding": numpy array 
      },
      {
          "title": "string",
          "content": "string",
          "embedding": numpy array 
      },
      {
          "title": "string",
          "content": "string",
          "embedding": numpy array 
      },
      {
          "title": "string",
          "content": "string",
          "embedding": numpy array 
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

### 7. **Process All Articles**
- **URL**: `/process-all`
- **Method**: POST
- **Description**: Process input text articles to group, generate titles, clusters/categories, summaries, and bias analysis for each group
- **Request | If past already embedded article, please pass "embedding" too.**
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
- **Response | Warning: Does not return embedding of each news content. If used on existing already embedded articles, please pass the embedding too.**
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
- **Request | Pass embedding if available.**:
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

### Named Entity Recognition (NER)
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
## Database Endpoints Production\machine-learning\app\db.py

### 1. **Get Clusters**
- **URL**: `/get-clusters`
- **Method**: GET
- **Description**: Returns the mapping of cluster IDs to human-readable category names.
- **Response**:
  ```json
  {
      "success": true,
      "clusters": {
          "0": "Korupsi",
          "1": "Pemerintahan",
          "2": "Kejahatan",
          "3": "Transportasi",
          "4": "Bisnis",
          "5": "Agama", 
          "6": "Finance",
          "7": "Politik"
      }
  }
  ```

---

### 2. **Fetch Users**
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

### 3. **Fetch News**
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

### 4. **Test Database Connection**
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

### 5. **News Page**
- **URL**: `/news_page`
- **Method**: GET
- **Description**: Fetches news articles with optional date filtering and renders them in an HTML page.
- **Query Parameters**:
  - `start_date`: Start date for filtering (optional).
  - `end_date`: End date for filtering (optional).
- **Response**: Renders an HTML page with news articles.

---

### 6. **News Article**
- **URL**: `/news_article`
- **Method**: GET
- **Description**: Fetches details of a specific news article and renders it in an HTML page.
- **Query Parameters**:
  - `title_index`: The index of the article to fetch.
- **Response**: Renders an HTML page with the article details.

---

### 7. **Insert News Page**
- **URL**: `/insert_news_page`
- **Method**: GET
- **Description**: Renders a page for inserting news articles.
- **Response**: Renders an HTML page for inserting news.

---

### 8. **Insert Title**
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

### 9. **Insert Article**
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

---

### 10. **Run Web Crawlers**
- **URL**: `/run-crawlers`
- **Method**: POST
- **Description**: Runs web crawlers to collect news articles from various sources and stores them in the database.
- **Request**:
  ```json
  {
      "optional_parameters": "value" // Optional parameters for crawler configuration
  }
  ```
- **Response**:
  ```json
  {
      "success": true,
      "message": "Crawlers executed and data inserted successfully",
      "total_results": 25,
      "inserted_count": 22
  }
  ```

---

### 11. **Update Articles**
- **URL**: `/update-articles`
- **Method**: GET
- **Description**: Processes articles with null embeddings by generating embeddings, cluster assignments, bias, hoax, and ideology classifications.
- **Response**:
  ```json
  {
      "success": true,
      "message": "Successfully processed 15 articles",
      "total_articles": 15
  }
  ```

---

### 12. **Group Articles**
- **URL**: `/group-articles`
- **Method**: GET, POST
- **Description**: Groups articles with NULL title_index by using the /separate endpoint to identify similar articles.
- **Response**:
  ```json
  {
      "success": true,
      "message": "Successfully grouped 30 articles into 8 clusters",
      "articles_count": 30,
      "clusters_count": 8
  }
  ```

---

### 13. **Process Articles**
- **URL**: `/process-articles`
- **Method**: GET, POST
- **Description**: Processes article groups by generating titles, summaries, analysis, and setting images for each group in the title table.
- **Response**:
  ```json
  {
      "success": true,
      "message": "Successfully processed 8 article groups",
      "total_groups": 10,
      "processed_groups": 8
  }
  ```

---

### 14. **Count Side**
- **URL**: `/count-side`
- **Method**: GET
- **Description**: Counts the number of articles categorized as liberal, conservative, or neutral for a given title index.
- **Query Parameters**:
  - `title_index`: The index of the title to fetch articles for.
- **Response**:
  ```json
  {
      "success": true,
      "counts": {
          "liberal": 10,
          "conservative": 5,
          "neutral": 3
      },
      "total": 18
  }
  ```

---

### 15. **Top News**
- **URL**: `/top-news`
- **Method**: GET
- **Description**: Fetches the top news articles based on the number of articles in each group for the current day.
- **Query Parameters**:
  - `limit`: The maximum number of top news groups to fetch (default is 5).
- **Response**:
  ```json
  {
      "success": true,
      "data": [
          {
              "title_index": 1,
              "title": "Top News Title",
              "image": "image_url",
              "all_summary": "Summary of the news",
              "article_count": 10,
              "counts": {
                  "liberal": 5,
                  "conservative": 3,
                  "neutral": 2
              }
          },
          {
              "title_index": 2,
              "title": "Another Top News Title",
              "image": "image_url",
              "all_summary": "Summary of the news",
              "article_count": 8,
              "counts": {
                  "liberal": 4,
                  "conservative": 2,
                  "neutral": 2
              }
          }
      ]
  }
  ```

---

### 16. **Get Cluster News**
- **URL**: `/get-cluster-news`
- **Method**: GET
- **Description**: Fetches news articles belonging to a specific cluster with detailed information.
- **Query Parameters**:
  - `cluster`: The cluster ID to fetch news for.
- **Response**:
  ```json
  {
      "success": true,
      "data": [
          {
              "title_index": 1,
              "title": "Article Title",
              "date": "2025-01-04",
              "all_summary": "Summary of the article content",
              "image": "image_url"
          },
          {
              "title_index": 2,
              "title": "Another Article Title",
              "date": "2025-01-04",
              "all_summary": "Summary of another article content",
              "image": "another_image_url"
          }
      ],
      "total": 2
  }
  ```

---

### 17. **Get News**
- **URL**: `/get-news`
- **Method**: GET
- **Description**: Fetches the latest news articles for the current day with their title, image, date, title_index, cluster, and political distribution counts.
- **Response**:
  ```json
  {
      "success": true,
      "data": [
          {
              "title": "News Article Title",
              "image": "image_url",
              "date": "2025-01-05",
              "all_summary": "News summary",
              "title_index": 123,
              "cluster": 4,
              "counts": {
                  "liberal": 5,
                  "conservative": 3,
                  "neutral": 2
              }
          }
      ],
      "total": 1
  }
  ```

---

### 18. **Get News Detail**
- **URL**: `/get-news-detail`
- **Method**: GET
- **Description**: Fetches detailed information about a specific news article group including its title, cluster, image, date, summary, analysis, and all related articles.
- **Query Parameters**:
  - `title_index`: The index of the news title to fetch details for.
- **Response**:
  ```json
  {
      "success": true,
      "title": "News Article Title",
      "cluster": 4,
      "image": "image_url",
      "date": "2025-01-05",
      "all_summary": "Comprehensive summary of the news topic",
      "analysis": "Detailed analysis of the news from different perspectives",
      "articles": [
          {
              "title": "Related Article Title",
              "url": "article_url",
              "source": "News Source",
              "date": "2025-01-05",
              "bias": 0.42,
              "hoax": 0.12,
              "ideology": 0.65
          }
      ]
  }
  ```

---

### 19. **Search Title**
- **URL**: `/search-title`
- **Method**: GET
- **Description**: Searches for news articles whose titles contain the specified query string.
- **Query Parameters**:
  - `query`: The search term to look for in news titles.
- **Response**:
  ```json
  {
      "success": true,
      "data": [
          {
              "title_index": 123,
              "title": "News Article Title Containing Search Term",
              "date": "2025-01-05",
              "all_summary": "Summary of the article content",
              "image": "image_url"
          }
      ],
      "total": 1
  }
  ```

---
