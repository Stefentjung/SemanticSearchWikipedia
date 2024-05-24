indexMapping = {
    "properties":{
        "property_id":{
            "type":"long"
        },
        "en_label":{
            "type":"text"
        },
        "en_description	":{
            "type":"text"
        },
        "en_descriptionvector":{
            "type":"dense_vector",
            "dims": 768,
            "index":True,
            "similarity": "l2_norm"
        }

    }
}