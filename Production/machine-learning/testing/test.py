import json
import mysql.connector
import sys
import os
import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# Get the parent directory of the current script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.routes import app

stopword_factory = StopWordRemoverFactory()
stopword = stopword_factory.create_stop_word_remover()
stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

def sanitize(text):
    text = str(text)

    # change text to lowercase
    text = text.lower()

    # remove hyperlinks
    text =re.sub(r'https?:\/\/.*[\r\n]*', '', text)

    # remove hashtag and username
    text = re.sub(r'(@\w+|#\w+)', '', text)

    # remove character other than a-z A-Z and 0-9
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)

    # replace new line '\n' with space
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\t', ' ', text)

    # removing more than one space
    text = re.sub(r'\s{2,}', ' ', text)

    # remove stopword with sastrawi library
    text = stopword.remove(text)

    # do stemming with sastrawi library
    text = stemmer.stem(text)

    return text

# Endpoints: cluster, bias, hoax, ideology, title, modeCluster, analyze
# For cluster, bias, hoax, ideology, 'article' variable must only have 1 article, with 'content'.
# For title, modeCluster, analyze, separate, embedding, cleaned, 'article' variable should have multiple articles with 'content', preferably with 'embedding'
def test_endpoint(endpoint, article):
    if isinstance(article, list):
        sanitized_data = [
            {**item, "content": sanitize(item["content"])} for item in article
        ]
    else:
        sanitized_data = {**article, "content": sanitize(article["content"])}

    with app.test_client() as client:
        response = client.post(
            f'/{endpoint}',
            data=json.dumps(sanitized_data), 
            content_type='application/json'
        )
        return response.json

# Special Endpoints (summary, antipode)
def test_summary_endpoint(test_data):
    """Test the /summary endpoint."""
    with app.test_client() as client:
        response = client.post(
            '/summary',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        return response.json['summary_liberalism'], response.json['summary_conservative']

# Test the /run-crawlers endpoint with an empty JSON request
def test_run_crawlers():
    with app.app_context():
        with app.test_client() as client:
            response = client.post(
                '/run-crawlers',
                data=json.dumps({}), 
                content_type='application/json'
            )
            return response.json

# Test the /update-articles endpoint
def test_update_articles():
    with app.app_context():
        with app.test_client() as client:
            response = client.get('/update-articles')
            return response.json

# Test the /group-articles endpoint
def test_group_articles():
    with app.app_context():
        with app.test_client() as client:
            response = client.get('/group-articles')
            return response.json

# Test the /process-articles endpoint
def test_process_articles():
    with app.app_context():
        with app.test_client() as client:
            response = client.get('/process-articles')
            return response.json

# Test the /count-side endpoint
def test_count_side(title_index):
    with app.app_context():
        with app.test_client() as client:
            response = client.get(f'/count-side?title_index={title_index}')
            return response.json

# Test the /top-news endpoint
def test_top_news(limit):
    with app.app_context():
        with app.test_client() as client:
            response = client.get(f'/top-news?limit={limit}')
            return response.json

def test_get_cluster_news(cluster):
    with app.app_context():
        with app.test_client() as client:
            response = client.get(f'/get-cluster-news?cluster={cluster}')
            return response.json
        
def test_search_title(query):
    with app.app_context():
        with app.test_client() as client:
            response = client.get(f'/search-title?query={query}')
            return response.json

def test_getner():
    with app.app_context():
        with app.test_client() as client:
            response = client.get('/getner')
            return response.json
        
def test_getnews():
    with app.app_context():
        with app.test_client() as client:
            response = client.get('/get-news')
            return response.json

def test_getnewsdetail():
    with app.app_context():
        with app.test_client() as client:
            response = client.get('/get-news-detail?title_index=76')
            return response.json
# =============================================================================================

def FetchDbToJson(db_config):
    mydb = mysql.connector.connect(**db_config)
    mycursor = mydb.cursor(dictionary=True)

    # Select all columns except 'date'
    sql = """
    SELECT id, title, source, url, image, content, embedding, cleaned, title_index, 
           cluster, bias, hoax, ideology 
    FROM articles
    """
    mycursor.execute(sql)
    articles = mycursor.fetchall()

    mycursor.close()
    mydb.close()
    return articles

def GetEmbedding(data, db_config):
    with app.test_client() as client:
        # Call the /embedding endpoint
        response = client.post(
            '/embedding',
            data=json.dumps(data),
            content_type='application/json'
        )

        # Validate response
        if response.status_code != 200:
            print(f"Error while calling /embedding endpoint: {response.json}")
            return

        embeddings = response.json.get("embedding", [])
        if not embeddings:
            print("No embeddings returned from /embedding.")
            return

    # Update the database with embeddings
    mydb = mysql.connector.connect(**db_config)
    mycursor = mydb.cursor()

    update_query = "UPDATE articles SET embedding = %s WHERE id = %s"
    for article, embedding in zip(data, embeddings):
        embedding_json = json.dumps(embedding)
        mycursor.execute(update_query, (embedding_json, article["id"]))

    mydb.commit()
    mycursor.close()
    mydb.close()

    print(f"Updated {len(data)} articles with embeddings.")

# Kelompokkan data ke title_index (Artikel yang ceritanya sama = 1 List)
def GrouptoDB(test_data, db_config):
    clusters_data = test_endpoint('separate', test_data)
    print("Clusters Data:", clusters_data)

    # Artikel" dikasih title_index, kemudian di tabel 'title' generate index agar bisa idiinsert summary, judul, analysis, dll. 
    if clusters_data:
        updateTitleTableandTitle_Index(db_config, clusters_data)

def updateTitleTableandTitle_Index(db_config, clusters):
    try:
        # Connect to the database
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()

        # Ensure the clusters match the number of rows in the articles table
        sql_fetch_ids = "SELECT id FROM articles ORDER BY id ASC"
        mycursor.execute(sql_fetch_ids)
        article_ids = [row[0] for row in mycursor.fetchall()]

        if len(clusters) != len(article_ids):
            raise ValueError("The number of clusters does not match the number of articles in the database.")

        # Update the title_index column for each article
        update_query = "UPDATE articles SET title_index = %s WHERE id = %s"
        update_data = [(cluster, article_id) for cluster, article_id in zip(clusters, article_ids)]
        mycursor.executemany(update_query, update_data)

        # Extract unique title_index values from the clusters
        unique_title_indices = set(clusters)

        # Fetch existing title_index values from the title table
        sql_fetch_title_indices = "SELECT title_index FROM title"
        mycursor.execute(sql_fetch_title_indices)
        existing_title_indices = {row[0] for row in mycursor.fetchall()}

        # Determine new title_index values to insert
        new_title_indices = unique_title_indices - existing_title_indices

        # Insert new rows into the title table
        if new_title_indices:
            insert_query = "INSERT INTO title (title_index) VALUES (%s)"
            insert_data = [(index,) for index in new_title_indices]
            mycursor.executemany(insert_query, insert_data)

        # Commit the transaction
        mydb.commit()
        print(f"Successfully updated {mycursor.rowcount} rows in articles and added {len(new_title_indices)} new rows to the title table.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'mycursor' in locals() and mycursor:
            mycursor.close()
        if 'mydb' in locals() and mydb:
            mydb.close()

def grouparticlesByTitleIndex(articles):
    grouped = {}
    for article in articles:
        index = article['title_index']
        if index not in grouped:
            grouped[index] = []
        grouped[index].append(article)
    return grouped

def ProcessArticle(articles):
    grouped_articles = grouparticlesByTitleIndex(articles) # Kelompokkan artikel berdasarkan title_index

    for title_index, group in grouped_articles.items():
        title = test_endpoint('title', group)

        mode_cluster = test_endpoint('modeCluster', group)

        summary_liberalism, summary_conservative = test_summary_endpoint(group)

        analysis = test_endpoint('analyze', group)

        updateTitleTable(title_index, title, mode_cluster, summary_liberalism, summary_conservative, analysis, db_config)

def updateTitleTable(title_index, title, mode_cluster, summary_liberalism, summary_conservative, analysis, db_config):
    mydb = mysql.connector.connect(**db_config)
    mycursor = mydb.cursor()

    sql = """
    UPDATE title 
    SET title = %s, cluster = %s, summary_liberalism = %s, 
        summary_conservative = %s, analysis = %s 
    WHERE title_index = %s
    """
    val = (title, mode_cluster, summary_liberalism, summary_conservative, analysis, title_index)
    mycursor.execute(sql, val)
    mydb.commit()

    mycursor.close()
    mydb.close()

def RunModelandUpdateDB(test_data, db_config):
    # Connect to the database
    mydb = mysql.connector.connect(**db_config)
    mycursor = mydb.cursor()

    # SQL queries to update each field in the database
    update_queries = {
        'cluster': "UPDATE articles SET cluster = %s WHERE id = %s",
        'bias': "UPDATE articles SET bias = %s WHERE id = %s",
        'hoax': "UPDATE articles SET hoax = %s WHERE id = %s",
        'ideology': "UPDATE articles SET ideology = %s WHERE id = %s",
        'cleaned': "UPDATE articles SET cleaned = %s WHERE id = %s",
    }

    # Iterate through each article in test_data
    for article in test_data:
        article_id = article['id']

        # Run each endpoint and retrieve the result
        cluster_result = test_endpoint('cluster', article)
        bias_result = test_endpoint('bias', article)
        hoax_result = test_endpoint('hoax', article)
        cleaned_result = test_endpoint('cleaned', article)
        cleaned_article = {'content': cleaned_result}
        ideology_result = test_endpoint('ideology', cleaned_article)

        # Update the database for each field
        mycursor.execute(update_queries['cluster'], (cluster_result, article_id))
        mycursor.execute(update_queries['bias'], (bias_result, article_id))
        mycursor.execute(update_queries['hoax'], (hoax_result, article_id))
        mycursor.execute(update_queries['ideology'], (ideology_result, article_id))
        mycursor.execute(update_queries['cleaned'], (cleaned_result, article_id))

    # Commit the changes and close the connection
    mydb.commit()
    mycursor.close()
    mydb.close()

    print("Successfully updated all articles with results from endpoints.")

# =============================================================================================
# MAIN CODE
# =============================================================================================

# Konfigurasi Database
db_config = {
    "host": "localhost",
    "user": "root",
    "database": "news"
}

# # Tarik data dari database, simpan dalam bentuk python object
# test_data = FetchDbToJson(db_config) 

# # Jalankan model bias, hoax, bersihin, ideologi, untuk masing" artikel, kemudian update ke database.
# RunModelandUpdateDB(test_data, db_config) 
# # GetEmbedding(test_data, db_config)

# # Kelompokkan data ke title_index (Artikel yang ceritanya sama = 1 List), update ke database
# # Outputnya [  [1,2,3], [4,5,6] ], dimana 1 2 3 adalah artikel yang ceritanya sama, 4 5 6 adalah artikel yang ceritanya sama
# GrouptoDB(test_data, db_config)gro

# # Embedding, hoax, dll sudah dapat, jadi ditarik lagi dari db
# articles = FetchDbToJson(db_config)

# # Proses data yang sudah dikelompokkan, generate title, modeCluster, summary, analysis, update ke database
# ProcessArticle(articles)

# =============================================================================================
# TEST CODE
# =============================================================================================
    
# Contoh endpoint untuk 1 artikel aja
# test_data = {
#     'content': "Menteri Koordinator Bidang Kemaritiman dan Investasi (Menko Marves) Luhut Binsar Panjaitan menargetkan Indonesia mampu memproduksi sendiri baterai lithium  untuk menunjang  kendaraan listrik di dalam negeri. Bahan baku baterai lithium itu nantinyaberasal dari Indonesia yakni nikel. Target itu juga telah disampaikan di depan para pimpinan pebisnis di Indonesia dan Asia yang hadir dalam acara DBS Asian Insights Forum 2023, Rabu (15\/3) lalu. Saya sampaikan bahwa pada tahun 2025, kami akan mampu memproduksi baterai lithium sendiri. Sehingga kita akan menjadi produsen baterai lithium terbesar ketiga di dunia pada tahun 2027 atau 2028 nanti. ' So, don't look down on Indonesia ' kata Luhut dalam unggahan di Instagram @ luhut.pandjaitan , Sabtu (18\/3). Luhut mengatakan target tersebut bukan sekedar angan-angan belaka, melainkan data menunjukkan bahwa ada investasi senilai US$31,9 miliar atau setara Rp490,4 triliun (asumsi kurs Rp15.375 per dolar AS) untuk pengembangan supply chain industri baterai di Indonesia hingga tahun 2026. [Gambas:Instagram] Indonesia, lanjut Luhut, juga telah menarik investasi asing langsung sebesar US$45,6 miliar atau setara Rp701,1 triliun tahun lalu, yang kemudian menurutnya merupakan rekor tertinggi baru sejak tahun 2000. Belum lagi nilai ekspor industri nikel kami mencapai US$33,8miliar pada tahun 2022, di mana US$ 14,3 miliar dihasilkan dari ekspor besi dan baja,\" kata dia. Luhut menilai 'keberhasilan' itu terwujud lantaran keteguhan Presiden Joko Widodo untuk tetap melanjutkan kebijakan hilirisasi industri dalam mengolah bahan baku di dalam negeri untuk nilai tambah yang lebih tinggi. Lebih lanjut, Luhut mengaku data-data tersebut sudah ia sampaikan juga kepada IMF yang bertandang ke kantornya beberapa waktu lalu. Luhut pun mengatakan kepada mereka, untuk saat ini, Indonesia sudah bisa mengekspor besi dan baja, bukan bijih nikel lagi. Luhut juga menargetkan Indonesia akan melakukan ekspor timah, bauksit, tembaga, dan bahan baku lainnya. Ia menginginkan agar perubahan besar ini harus dilihat oleh negara-negara maju. \" This is their problem . Selalu melihat negara berkembang seperti Indonesia adalah negara yang mereka tahu dua puluh atau lima belas tahun yang lalu. Dengan memberlakukan larangan ekspor nikel, kita mempunyai kekuatan untuk menghasilkan energi hijau yang sudah kita cita-citakan sejak lama, jelasnya. Luhut pun meminta agar seluruh masyarakat Indonesia berbangga hati. Kendati demikian, ia juga mewanti-wanti bahwa Indonesia tidak melawan negara manapun, melainkan justru bersahabat dengan siapa saja. Indonesia menurutnya terbuka dan mempersilakan negara-negara lain untuk berinvestasi serta membangun industri pengolahan pertambangan di dalam negeri. \"Dengan catatan bahwa kami juga punya aturan main atau regulasi yang harus mereka penuhi. Menjadi negara maju adalah hak setiap negara, kewajiban kita adalah memperjuangkannya, ujar Luhut. [Gambas:Video CNN]"
# }

# print(test_endpoint('cluster', test_data))
# print(test_endpoint('bias', test_data))
# print(test_endpoint('hoax', test_data))
# print(test_endpoint('ideology', test_data))
# print(test_endpoint('cleaned', test_data))

# # Test the run-crawlers endpoint
# print("Testing run-crawlers endpoint:")
# print(test_run_crawlers())

# # Test article-update
# print("Testing article-update endpoint:")
# print(test_update_articles())

# # Test group-articles endpoint
# print("Testing group-articles endpoint:")
# print(test_group_articles())

# # Test process-articles endpoint
# print("Testing process-articles endpoint:")
# print(test_process_articles())

# # Test count-side endpoint with a sample title_index (replace '1' with an actual title_index if needed)
# print("Testing count-side endpoint:")
# print(test_count_side(21))

# # Test top-news endpoint
# print("Testing top-news endpoint:")
# print(test_top_news(3))

# Test get-cluster-news endpoint with a sample cluster (replace '1' with an actual cluster if needed)
# print("Testing get-cluster-news endpoint:")
# print(test_get_cluster_news(2))

# Test search-title endpoint with a sample query (replace 'sample' with an actual query if needed)
# print("Testing search-title endpoint:")
# print(test_search_title('Pemprov'))

# Test getner endpoint
# print("Testing getner endpoint")
# print(test_getner())

# Test get-news endpoint
# print("Testing get-news endpoint")
# print(test_getnews())

# Test get-news endpoint
# print("Testing get-news endpoint")
# print(test_getnewsdetail())

# print(test_endpoint('title', test_data)) 
# print(test_endpoint('modeCluster', test_data))
# print(test_endpoint('analyze', test_data))
# print(test_endpoint('separate', test_data))
# print(test_endpoint('embedding', test_data))
# print(test_summary_endpoint(test_data))

# def test_process_all_endpoint(test_data):
#     with app.test_client() as client:
#         response = client.post(
#             '/process-all',
#             data=json.dumps(test_data), 
#             content_type='application/json'
#         )
#         return response.json
    
# print(test_process_all_endpoint(test_data))

# antipode_data = {
#   "article": {
#         'content': "Menteri Koordinator Bidang Kemaritiman dan Investasi (Menko Marves) Luhut Binsar Panjaitan menargetkan Indonesia mampu memproduksi sendiri baterai lithium  untuk menunjang  kendaraan listrik di dalam negeri. Bahan baku baterai lithium itu nantinyaberasal dari Indonesia yakni nikel. Target itu juga telah disampaikan di depan para pimpinan pebisnis di Indonesia dan Asia yang hadir dalam acara DBS Asian Insights Forum 2023, Rabu (15\/3) lalu. Saya sampaikan bahwa pada tahun 2025, kami akan mampu memproduksi baterai lithium sendiri. Sehingga kita akan menjadi produsen baterai lithium terbesar ketiga di dunia pada tahun 2027 atau 2028 nanti. ' So, don't look down on Indonesia ' kata Luhut dalam unggahan di Instagram @ luhut.pandjaitan , Sabtu (18\/3). Luhut mengatakan target tersebut bukan sekedar angan-angan belaka, melainkan data menunjukkan bahwa ada investasi senilai US$31,9 miliar atau setara Rp490,4 triliun (asumsi kurs Rp15.375 per dolar AS) untuk pengembangan supply chain industri baterai di Indonesia hingga tahun 2026. [Gambas:Instagram] Indonesia, lanjut Luhut, juga telah menarik investasi asing langsung sebesar US$45,6 miliar atau setara Rp701,1 triliun tahun lalu, yang kemudian menurutnya merupakan rekor tertinggi baru sejak tahun 2000. Belum lagi nilai ekspor industri nikel kami mencapai US$33,8miliar pada tahun 2022, di mana US$ 14,3 miliar dihasilkan dari ekspor besi dan baja,\" kata dia. Luhut menilai 'keberhasilan' itu terwujud lantaran keteguhan Presiden Joko Widodo untuk tetap melanjutkan kebijakan hilirisasi industri dalam mengolah bahan baku di dalam negeri untuk nilai tambah yang lebih tinggi. Lebih lanjut, Luhut mengaku data-data tersebut sudah ia sampaikan juga kepada IMF yang bertandang ke kantornya beberapa waktu lalu. Luhut pun mengatakan kepada mereka, untuk saat ini, Indonesia sudah bisa mengekspor besi dan baja, bukan bijih nikel lagi. Luhut juga menargetkan Indonesia akan melakukan ekspor timah, bauksit, tembaga, dan bahan baku lainnya. Ia menginginkan agar perubahan besar ini harus dilihat oleh negara-negara maju. \" This is their problem . Selalu melihat negara berkembang seperti Indonesia adalah negara yang mereka tahu dua puluh atau lima belas tahun yang lalu. Dengan memberlakukan larangan ekspor nikel, kita mempunyai kekuatan untuk menghasilkan energi hijau yang sudah kita cita-citakan sejak lama, jelasnya. Luhut pun meminta agar seluruh masyarakat Indonesia berbangga hati. Kendati demikian, ia juga mewanti-wanti bahwa Indonesia tidak melawan negara manapun, melainkan justru bersahabat dengan siapa saja. Indonesia menurutnya terbuka dan mempersilakan negara-negara lain untuk berinvestasi serta membangun industri pengolahan pertambangan di dalam negeri. \"Dengan catatan bahwa kami juga punya aturan main atau regulasi yang harus mereka penuhi. Menjadi negara maju adalah hak setiap negara, kewajiban kita adalah memperjuangkannya, ujar Luhut. [Gambas:Video CNN]"
#   },
#   "df": test_data
# }

# print(test_endpoint('antipode', antipode_data))

# if __name__ == '__main__':
#     test_data = [
#         {
#             "content": "Menteri Koordinator Bidang Kemaritiman dan Investasi (Menko Marves) Luhut Binsar Pandjaitan menghadiri forum investasi di Jakarta."
#         },
#         {
#             "content": "Presiden Joko Widodo meresmikan proyek infrastruktur baru di ibu kota negara."
#         },
#         {
#             "content": "Pemerintah mengumumkan kebijakan baru terkait subsidi energi untuk masyarakat."
#         }
#     ]

#     def test_ner_endpoint(test_data):
#         with app.test_client() as client:
#             response = client.post(
#                 '/ner',
#                 data=json.dumps(test_data), 
#                 content_type='application/json'
#             )
#             return response.json

#     print(test_ner_endpoint(test_data))


# test_data = [
#     {
#         "keyword": ['Marves', 'Luhut Binsar Pandjaitan', 'forum investasi', 'Jakarta'],
#     },
#     {
#         "keyword": ['Marves', 'proyek infrastruktur', 'ibu kota negara'],
#     },
#     {
#         "keyword": ['Pemerintah', 'forum investasi', 'subsidi energi', 'masyarakat'],
#     },
# ]

# def test_top_keywords_endpoint(test_data):
#     with app.test_client() as client:
#         response = client.post(
#             '/top_keywords',
#             data=json.dumps(test_data), 
#             content_type='application/json'
#         )
#         return response.json
    
# print(test_top_keywords_endpoint(test_data))

# ==============================================================================
# add entry to database

# def add_entry_to_db(data, db_config):
#     mydb = mysql.connector.connect(**db_config)
#     mycursor = mydb.cursor()

#     sql = """
#     INSERT INTO articles (title, source, url, image, content)
#     VALUES (%s, %s, %s, %s, %s)
#     """
#     val = (data['title'], data['source'], data['url'], data['image'], data['content'])
#     mycursor.execute(sql, val)
#     mydb.commit()

#     mycursor.close()
#     mydb.close()
