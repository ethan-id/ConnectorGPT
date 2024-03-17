# chatgpt-retrieval

This is a Flask API that let's you use ChatGPT on your own data.

Inspiration and original Source Code from here [YouTube Video](https://youtu.be/9AXP7tCI9PI) and [here](https://github.com/techleadhd/chatgpt-retrieval).

## Installation
Run these to install the necessary libraries
```
pip install langchain-community openai chromadb tiktoken unstructured
pip install "unstructured[pdf]"
```
Modify `constants.py.default` to use your own [OpenAI API key](https://platform.openai.com/account/api-keys), and rename it to `constants.py`.

Place your own data into `data/data.txt`.

## Docker Usage
```
docker build -t image-name .
docker run -p 5000:5000 image-name
```

### Docker Deployment
```
docker tag local_tag google-cloud-repo-url/local_tag:latest
docker push google-cloud-repo-url/local_tag:latest
```

If the revision is failing to start from something like an exec format error, you may have to build with this command:
```
docker build --platform linux/amd64 -t image-name .
```

### Sending Requests to the Flask API:
```
curl -X POST http://localhost:5000/query -H "Content-Type: application/json" -d '{"question":"Can you give me a summary of all of the data? Not just the price history", "chat_history": []}'
```

## Example usage
Test reading `data/data.txt` file.
```
> python chatgpt.py "what is my dog's name"
Your dog's name is Sunny.
```

Test reading `data/cat.pdf` file.
```
> python chatgpt.py "what is my cat's name"
Your cat's name is Muffy.
```
