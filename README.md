# exl-chatbot

Required Software :

Python 3.6 and above Node ElasticSearch


RASA Opensource - 
RASA NLU 
Initialize websocket server: Navigate to 'rasa-chatbot' folder. in the command terminal  
'rasa train' 
to train and generate latest models run 
'rasa run -m models --enable-api --cors "*" --debug' 
to start RASA websocket server on 5005 port to check if server is up check 'http://localhost:5005/' is up and running

RASA Actions server:

In 'rasa-chatbot' folder path run 
'rasa run actions' 
to initialise actions server. to check if server is up check 'http://localhost:5505/' is up and running

REACT web application :
In 'exl-chatbot\react-insurance-form\web-form' folder in the command terminal  run 
'npm run start'
to initialize front end in on http://localhost:3000/. the web application would be up and running.
Enable CROS if chatbot UI is not showing up or use CROS ON extenstion in chrome like https://chrome.google.com/webstore/detail/moesif-origin-cors-change/digfbfaphojjndkpccljibejjbppifbc

Haystack - FASTAPI server (Optional): 
Navigate to 'exl-chatbot\fallback-fastapi' folder. in the command prompt run
'uvicorn main:app' 
to start haystack server on 8000 port for fallback queries from the user
