from datetime import datetime
from elasticsearch import Elasticsearch

def map_course(es) :
	body = {
		'mappings' : {
				"course" : {
			        "properties" : {
        				"course_code" : {"type" : "string" , "index" : "not_analyzed" } ,
        				"section" : { "type" : "string" } ,
        				"seat" : {"type" : "integer" } ,
        				"new_seat" : {"type" : "integer"},
        				"max_seat" : {"type" : "integer"}
        			}
    			}
			}
	}
	es.indices.delete_mapping(index='reg.chula' , doc_type = "course")
	es.indices.put_mapping(index = 'reg.chula' , doc_type ="course" , body = body )
	#es.indices.create(index = 'reg.chula' , body = body)

def connect() :
	es = Elasticsearch()
	#if (es.exists(index = ['reg.chula'] , id = 1)) :
		#Create new index
		#create_new_index(es)
	#map_course(es)
	return es

def put_doc(es , data) :
	es.index(index="reg.chula", doc_type="course", body=data)