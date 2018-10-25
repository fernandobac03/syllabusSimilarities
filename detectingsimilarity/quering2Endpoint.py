from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://localhost:8080/repositories/silabosEC")
sparql.setQuery("""
  PREFIX foaf: <http://xmlns.com/foaf/0.1/>  
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
  PREFIX ies: <http://ies.linkeddata.ec/syllabusOntology/vocabulary#> 
  PREFIX aiiso: <http://purl.org/vocab/aiiso/schema#> 


  SELECT DISTINCT ?s ?nombreCapitulo ?nombreSubcapitulo ?capitulos 
                  ?nombreAsignatura ?nombreObjetivo ?descripcion 
                  ?dependencia ?institucion ?nombreDependencia 
                  ?nombreInstitucion ?fechaCreacion ?creditos 
  WHERE {   
        ?s a <http://purl.org/vocab/aiiso/schema#KnowledgeGrouping> .
        ?s      aiiso:name   ?nombreAsignatura.
               
        OPTIONAL { 
             ?s      aiiso:description  ?descripcion. 
        } .
        OPTIONAL { 
             ?s      ies:is_taught_by   ?dependencia. 
             ?dependencia aiiso:name       ?nombreDependencia.   
        } .
        OPTIONAL { 
             ?s ies:date_creation ?fechaCreacion .
        } . 
        OPTIONAL { 
             ?s ies:credits ?creditos .
        } . 
        OPTIONAL { 
             ?dependencia ies:is_academic_unit_of  ?institucion. 
             ?institucion aiiso:name         ?nombreInstitucion. 
        } .
        OPTIONAL { 
             ?s      ies:has_academic_content  ?contenido. 
             ?contenido  ies:has_chapter ?capitulos. 
             ?capitulos aiiso:name ?nombreCapitulo.  
             ?capitulos ies:has_subchapter ?subcap. 
             ?subcap aiiso:name ?nombreSubcapitulo.    
        } .
        OPTIONAL { 
             ?s ies:has_objective ?objetivos.
             ?objetivos ies:has_item ?objetivo. 
             ?objetivo aiiso:name ?nombreObjetivo . 
        }. 
  } limit 100
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    
    print(result["s"]["value"] + " - "  + result["nombreAsignatura"]["value"] + " - " +result["descripcion"]["value"])
    

