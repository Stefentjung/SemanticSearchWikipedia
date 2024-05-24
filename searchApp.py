import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

indexName = "all_labels"

try:
    es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "qXCe9zdlLF*zJ_E8XAi7"),
    ca_certs="/Users/STEFANY TJUNG/Downloads/Information Retrieval/elasticsearch-8.13.4-windows-x86_64/elasticsearch-8.13.4/config/certs/http_ca.crt"
    )
except ConnectionError as e:
    print("Connection Error:", e)
    
if es.ping():
    print("Succesfully connected to ElasticSearch!!")
else:
    print("Oops!! Can not connect to Elasticsearch!")




def search(input_keyword):
    model = SentenceTransformer('all-mpnet-base-v2')
    vector_of_input_keyword = model.encode(input_keyword)

    query = {
    "field" : "en_descriptionvector",
    "query_vector" : vector_of_input_keyword,
    "k" : 15,
    "num_candidates" : 7668, 
    }

    res = es.knn_search(index="all_labels"
                        , knn=query 
                        , source=["en_label","en_description"]
                        )
    results = res["hits"]["hits"]

    return results

def main():
    st.title("Search Wikipedia Data")

    # Input: User enters search query
    search_query = st.text_input("Enter your search")

    # Button: User triggers the search
    if st.button("Search"):
        if search_query:
            # Perform the search and get results
            results = search(search_query)

            # Display search results
            st.subheader("Search Results")
            for result in results:
                with st.container():
                    if '_source' in result:
                        try:
                            st.header(f"{result['_source']['en_label']}")
                        except Exception as e:
                            print(e)
                        
                        try:
                            st.write(f"Description: {result['_source']['en_description']}")
                        except Exception as e:
                            print(e)
                        st.divider()

                    
if __name__ == "__main__":
    main()