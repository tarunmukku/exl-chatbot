# This files contains your custom actions which can be used to run
# custom Python code.

# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"


import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from haystack.nodes import FARMReader, TransformersReader
from haystack.document_stores import OpenSearchDocumentStore
from haystack.nodes import DensePassageRetriever
from haystack.nodes import BM25Retriever
from haystack.pipelines import ExtractiveQAPipeline


url = "search-auto-insurance-nbdvjfxbsyudd5yhpq3e4ic6bu.ap-south-1.es.amazonaws.com"
username = "tarunm"
password = "May#2022password"

document_store = OpenSearchDocumentStore(host=url,port=443, username=username, password=password, index="auto-insurance")
#retriever = BM25Retriever(document_store=document_store)

retriever = DensePassageRetriever(
    document_store=document_store,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
    max_seq_len_query=64,
    max_seq_len_passage=256,
    batch_size=16,
    use_gpu=True,
    embed_title=True,
    use_fast_tokenizers=True,
)

reader =FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)
#reader = FARMReader(model_name_or_path="deepset/tinyroberta-squad2", use_gpu=False)

pipe = ExtractiveQAPipeline(reader=reader, retriever=retriever)
    

class ActionHelloWorld(Action):


    def name(self) -> Text:
        return "action_set_vin"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        dispatcher.utter_message(text="Hello World!")

        return []

class ActionShowCarsousel(Action):

    def name(self) -> Text:
        return "action_get_recommendations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            recommendations_products = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [{
                    "title": "Home Insurance",
                    "subtitle": "Cover against Fire, Theft, Earthquake & all Natural Calamities.",
                    "image_url": "https://static.vecteezy.com/system/resources/previews/005/911/705/original/home-insurance-icon-house-protection-symbol-for-your-web-site-logo-app-ui-design-free-vector.jpg",
                    "buttons": [{
                        "title": "Buy Product",
                        "url": "https://purchase.allstate.com/onlineshopping/welcome?zipcode=&product=Home&intcid=%2Fhome-insurance%7CNavigationHeader%7CQuote%7CHome&_ga=2.237427136.197248041.1657354953-1002433013.1655873442",
                        "type": "web_url"
                    },
                        {
                            "title": "Know more",
                            "url": "https://www.allstate.com/home-insurance",
                            "type": "web_url"
                        }
                    ]
                },
                    {
                    "title": "Life Insurance",
                    "subtitle": "Get Benefits As Per Your Changing Age and Life Style Needs",
                    "image_url": "https://www.kindpng.com/picc/m/123-1239666_family-life-insurance-logo-hd-png-download.png",
                    "buttons": [{
                        "title": "Buy Product",
                        "url": "https://purchase.allstate.com/onlineshopping/welcome?zipcode=&product=TLF&intcid=%2Flife-insurance%7CNavigationHeader%7CQuote%7Cquote_box:TLF&_ga=2.30654207.197248041.1657354953-1002433013.1655873442",
                        "type": "web_url"
                    },
                        {
                            "title": "Know more",
                            "url": "https://www.allstate.com/life-insurance",
                            "type": "web_url"
                        }
                    ]
                },
                    {
                    "title": "Condo Insurance",
                    "subtitle": "protect your condo and the things you love inside",
                    "image_url": "https://public.libertymutual-cdn.com/lm-media-assets/content-images/products/property/condo/condo.svg",
                    "buttons": [{
                        "title": "Buy Product",
                        "url": "https://purchase.allstate.com/onlineshopping/welcome?zipcode=&product=Co&intcid=%2Fcondo-insurance%7CPromotionQuoteHero%7CQuote%7CCo",
                        "type": "web_url"
                    },
                        {
                            "title": "Know more",
                            "url": "https://www.allstate.com/condo-insurance",
                            "type": "web_url"
                        }
                    ]
                }
                   ,
                    {
                    "title": "Motorcycle Insurance",
                    "subtitle": "hit the open road knowing you're protectede",
                    "image_url": "https://i.pinimg.com/564x/23/d1/68/23d16895b037e9fbe32ecbb0cf984d22.jpg",
                    "buttons": [{
                        "title": "Buy Product",
                        "url": "https://purchase.allstate.com/onlineshopping/welcome?zipcode=%7BSelectedZipCode%7D&product=Mo&intcid=%2Fmotorcycle-insurance%7CPromotionQuoteHero%7CQuote%7CMotorcycle-Insurance&_ga=2.1384177.197248041.1657354953-1002433013.1655873442",
                        "type": "web_url"
                    },
                        {
                            "title": "Know more",
                            "url": "https://www.allstate.com/motorcycle-insurance",
                            "type": "web_url"
                        }
                    ]
                }
                ]
            }
        }

            dispatcher.utter_message(text='Here are some of the recommendations',attachment=recommendations_products)
            return []



class ActionHelloWorld(Action):
   
    def name(self) -> Text:
        return "action_intent_question"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global pipe
        message = tracker.latest_message.get('text')
        result = pipe.run(query=message)
        
        dispatcher.utter_message(text=result['answers'][0].answer)

        return []            

class ActionHaystack(Action):

    def name(self) -> Text:
        return "call_haystack"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = "http://localhost:8000/query"
        payload = {"query": str(tracker.latest_message["text"])}
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, json=payload).json()

        if response["answers"]:
            answer = response["answers"][0]["answer"]
        else:
            answer = "No Answer Found!"

        dispatcher.utter_message(text=answer)

        return []