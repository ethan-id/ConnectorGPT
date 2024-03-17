# GPT Connector

This is a Flask API that let's you programmatically use ChatGPT on your own data.

It has been containerized with Docker, and deployed to Google Cloud Run for usage in my other projects, specifically [BizGlimpse](https://github.com/ethan-id/BizGlimpse)

## Features

* Place your own data into `data/data.txt`, so that it is built into the image and the chatbot will constantly be aware of it. 
* Send POST requests to the API with an `additional_data` member of the body, which the chatbot will be made aware of.

## Local Installation
Run these to install the necessary libraries
```
pip install langchain-community openai chromadb tiktoken unstructured
pip install "unstructured[pdf]"
```
Create and modify `.env` to use your own [OpenAI API key](https://platform.openai.com/account/api-keys).
E.G. `OPENAI_API=myapikey`

## Docker
```
docker build -t image-name .
docker run -p 5000:5000 image-name
```
_May have to adjust ports in the command above and the dockerfile to run the API locally_

### Docker Deployment
```
docker tag local_tag google-cloud-repo-url/local_tag:latest
docker push google-cloud-repo-url/local_tag:latest
```

If you are using a Mac running ARM architecture and attempting to deploy the container to a service like Google Cloud Run, you should use this build command instead:
```
docker build --platform linux/amd64 -t image-name .
```

### Sending Requests to the Flask API:
```
curl -X POST http://localhost:5000/query -H "Content-Type: application/json" -d '{"question":"How old is my dog?", "chat_history": [], "additional_data", "My dog is 12 years old."}'
```

### Credits

Inspiration and some of the original Source Code is from this [YouTube Video](https://youtu.be/9AXP7tCI9PI) and this [github repo](https://github.com/techleadhd/chatgpt-retrieval).
