import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class WebSearcher:
    def __init__(self, meta_descriptions):
        self.meta_descriptions = meta_descriptions
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.meta_descriptions)

    def search(self, query):
        query_vector = self.vectorizer.transform([query])
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix)
        top_indices = similarity_scores.argsort()[0][-5:][::-1]
        top_results = df.iloc[top_indices]

        return {"result": top_results, "similarity_scores": similarity_scores};

if __name__ == "__main__":
    db = sqlite3.connect('scrapy_data.db')
    cursor = db.cursor()
    result = cursor.execute("SELECT * FROM pages")

    df = pd.DataFrame(result)
    df.columns = [description[0] for description in result.description]

    cursor.close()
    db.close()

    meta_descriptions = df.iloc[:, 3].astype(str).tolist()
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(meta_descriptions)

    model = WebSearcher(meta_descriptions)
    result = model.search(input("Enter your query: "))

    print("Top 5 results:")
    for index, row in result["result"].iterrows():
        print(f"Başlık: {row['title']}")
        print(f"URL: {row['url']}")
        print(f"Meta Açıklamaso: {row['meta_description']}")
        print(f"Eşleşme Skoru: {result['similarity_scores'][0][index]}")
        print("Made by Ömer Asaf Karasu")
