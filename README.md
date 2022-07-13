# exl-chatbot

Required Software :

Python 3.6 and above Node ElasticSearch

elastic Search Installation and initialise the server: Install elastic search and start the server in 9200 port.

Loading data to document-store of elasticsearch: Run 'ElasticSearch_Setup.ipynb' file it will automatically load the cleaned document of auto Insurance policy from 'output' folder.

RASA Opensource - Initialize websocket server: Navigate to 'rasa-chatbot' folder. run 'rasa train' to train and generate latest models run 'rasa run -m models --enable-api --cors "*" --debug' to start RASA websocket server on 5005 port to check if server is up check 'http://localhost:5005/' is up and running

RASA Actions server:

run 'rasa run actions' command to initialise actions server. to check if server is up check 'http://localhost:5505/' is up and running

REACT web application : In 'exl-chatbot\react-insurance-form\web-form' folder run 'npm run start' to initialize front end in on http://localhost:3000/. the web application would be up and running. Enable CROS if chatbot UI is not showing up or use CROS ON extenstion in chrome like https://chrome.google.com/webstore/detail/moesif-origin-cors-change/digfbfaphojjndkpccljibejjbppifbc

Haystack - FASTAPI server: Navigate to 'exl-chatbot\fallback-fastapi' folder. run 'uvicorn main:app' to start haystack server on 8000 port for fallback queries from the user
