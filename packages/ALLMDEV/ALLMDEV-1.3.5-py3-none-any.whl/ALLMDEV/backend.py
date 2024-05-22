from fastapi import FastAPI, WebSocket, Request, File, UploadFile, Form
from flask import request
from pydantic import BaseModel
from llama_index.llms.llama_cpp import LlamaCPP
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import asyncio
import os
import json
from fastapi.middleware.cors import CORSMiddleware
import vertexai
from vertexai.generative_models import GenerativeModel
from openai import AzureOpenAI
from fastapi.responses import JSONResponse
from langchain.document_loaders import CSVLoader, PDFMinerLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


max_new_tokens = 512
prompt_template = "<s>[INST] {prompt} [/INST]"
config_path = "model/config.json"
vertex_config_path = "model/vertex_config.json"
azure_config_path = "model/azure_config.json"

class Message(BaseModel):
    userInput: str
    model: str
    temperature: float

class Response(BaseModel):
    response: str

class ModelConfig(BaseModel):
    temp: float
    model: str
    gpu: bool
    agent: str

def load_config():
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    else:
        return {
            "temperature": 0.5,
            "model": "",
            "model_path": "",
            "gpu": False
        }
    
def load_vertex_config():
    if os.path.exists(vertex_config_path):
        with open(vertex_config_path, "r") as f:
            return json.load(f)
    else:
        return {
            "projectId": "",
            "modelInput": "gemini-1.0-pro-002",
            "region": "",
        }
    
def load_azure_config():
    if os.path.exists(azure_config_path):
        with open(azure_config_path, "r") as f:
            return json.load(f)
    else:
        return {
            "apikey": "",
            "modelInput": "gemini-1.0-pro-002",
            "version": "",
            "endpoint": ""
        }

def save_config(config):
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)
def save_azure_config(config):
    with open(azure_config_path, "w") as f:
        json.dump(config, f, indent=4)
def save_vertex_config(config):
    with open(vertex_config_path, "w") as f:
        json.dump(config, f, indent=4)

config = load_config()

@app.websocket("/model_config")
async def websocket_model_config(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            print("Received model config:", data)
            is_vertex_model = "projectId" in data or "region" in data
            is_azure_model = "key" in data  or "version" in data or "endpoint" in data
            if is_vertex_model:
                vertex_config = {
                    "project_id" : data["projectId"],
                    "model" : data["modelInput"],
                    "region" : data["region"]
                }
                save_vertex_config(vertex_config)
            if is_azure_model:
                azure_config = {
                    "apikey" : data["key"],
                    "version" : data["version"],
                    "endpoint" : data["endpoint"],
                    "modelInput" : data["modelInput"]
                }
                save_azure_config(azure_config)
            else:

                model_config = load_config()
                temp = model_config["temperature"]
                model = model_config["model"]
                gpu = model_config["gpu"]
                
                if model != data["model"] or temp != data["temperature"]:
                    model_config["model"] = data["model"]
                    model_config["temperature"] = data["temperature"]

                    model_directory = "model"
                    for file in os.listdir(model_directory):
                        if file.endswith('.gguf') and config["model"].lower() in file:
                            config["model_path"] = os.path.join(model_directory, file)
                            break

                    save_config(config)

                model_kwargs = {"n_gpu_layers": -1 if gpu else 0}
                # llm = LlamaCPP(
                #     model_path=config["model_path"],
                #     temperature=config["temperature"],
                #     max_new_tokens=max_new_tokens,
                #     context_window=3900,
                #     model_kwargs=model_kwargs,
                #     verbose=False,
                # )
            await websocket.send_json({"status": "success", "message": "Model configuration updated."})

    except Exception as e:
        print(e)
    # finally:
    #     await websocket.close()




@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            print("ws route")
            user_input = data["userInput"]
            
            if user_input.lower() == "exit":
                print("Exiting chat.")
                break
            
            # Update config if model or temperature changes
            # if data["model"] != config["model"] or temp != config["temperature"]:
            #     config["model"] = data["model"]
            #     config["temperature"] = temp

            #     model_directory = "model"
            #     for file in os.listdir(model_directory):
            #         if file.endswith('.gguf') and config["model"].lower() in file:
            #             config["model_path"] = os.path.join(model_directory, file)
            #             break

            #     save_config(config)

            prompt = prompt_template.format(prompt=user_input)
            model_kwargs = {"n_gpu_layers" : -1 if config["gpu"] else 0}
            llm = LlamaCPP(
                model_path=config["model_path"],
                temperature=config["temperature"],
                max_new_tokens=max_new_tokens,
                context_window=3900,
                model_kwargs=model_kwargs,
                verbose=False,
            )
            response_iter = llm.stream_complete(prompt)

            for response in response_iter:
                await websocket.send_text(response.delta)
                await asyncio.sleep(0)

    except Exception as e:
        print(e)
    

@app.websocket("/available_agents")
async def agentinfo(websocket: WebSocket):
    await websocket.accept()
    agents = os.listdir('db')
    dict = {
        'agentinfo': agents
    }
    await websocket.send_json(dict)

@app.websocket("/agent")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        config=load_config()
        model_kwargs = {"n_gpu_layers" : -1 if config["gpu"] else 0}
        llm = LlamaCPP(
            model_path=config["model_path"],
            temperature=config["temperature"],
            max_new_tokens=max_new_tokens,
            context_window=3900,
            model_kwargs=model_kwargs,
            verbose=False,
        )
        while True:
            data = await websocket.receive_json()
            print(data)
            print("agent route")
            user_input = data["userInput"]
            
            if user_input.lower() == "exit":
                print("Exiting chat.")
                break

            agent = data['agent']
            persist_directory = os.path.join('db', agent)
            embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)

            docs = db.similarity_search(user_input, k=3)
            context = docs[0].page_content
            prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query:<s>[INST] {prompt} [/INST]"
            prompt = prompt_template.format(context=context, prompt=user_input)

            # model_kwargs = {"n_gpu_layers" : -1 if config["gpu"] else 0}
            # llm = LlamaCPP(
            #     model_path=config["model_path"],
            #     temperature=config["temperature"],
            #     max_new_tokens=max_new_tokens,
            #     context_window=3900,
            #     model_kwargs=model_kwargs,
            #     verbose=False,
            # )

            response_iter = llm.stream_complete(prompt)

            for response in response_iter:
                await websocket.send_text(response.delta)
                await asyncio.sleep(0)

            # if data["model"] != config["model"] or temp != config["temperature"]:
            #     config["model"] = data["model"]
            #     config["temperature"] = temp

            #     model_directory = "model"
            #     for file in os.listdir(model_directory):
            #         if file.endswith('.gguf') and config["model"].lower() in file:
            #             config["model_path"] = os.path.join(model_directory, file)
            #             break

                save_config(config)

           

    except Exception as e:
        print(e)
    finally:
        await websocket.close()

@app.websocket("/vertex")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        config=load_vertex_config()
        # model_kwargs = {"n_gpu_layers" : -1 if config["gpu"] else 0}
        # llm = LlamaCPP(
        #     model_path=config["model_path"],
        #     temperature=config["temperature"],
        #     max_new_tokens=max_new_tokens,
        #     context_window=3900,
        #     model_kwargs=model_kwargs,
        #     verbose=False,
        # )
        while True:
            data = await websocket.receive_json()
            print(data)
            print("vertex route")
            prompt = data["userInput"]
            
            if prompt.lower() == "exit":
                print("Exiting chat.")
                break

            agent = data['agent']
            projectid=config["project_id"]
            region=config["region"]
            model=config["model"]
            # projectid=data['projectId']
            # region=data['region']
            # model=data['modelInput']

            # if model != config["model"] or projectid!= config["projectId"]:
            #     config["model"] = model
            #     config["projectId"] = projectid
            #     config["region"] = region
            #     save_vertex_config(config)
            vertexai.init(project=projectid, location=region)
            multimodal_model = GenerativeModel(model_name=model)
            if agent == "None":
                response = multimodal_model.generate_content(prompt)
                await websocket.send_text(response.text)
            else:

                persist_directory = os.path.join('db', agent)
                embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
                db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)

                docs = db.similarity_search(prompt, k=3)
                context = docs[0].page_content
                prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query:<s>[INST] {prompt} [/INST]"
                prompt = prompt_template.format(context=context, prompt=prompt)
                response = multimodal_model.generate_content(prompt)
                await websocket.send_text(response.text)

            


            # model_kwargs = {"n_gpu_layers" : -1 if config["gpu"] else 0}
            # llm = LlamaCPP(
            #     model_path=config["model_path"],
            #     temperature=config["temperature"],
            #     max_new_tokens=max_new_tokens,
            #     context_window=3900,
            #     model_kwargs=model_kwargs,
            #     verbose=False,
            # )

            # response_iter = llm.stream_complete(prompt)

            # for response in response_iter:
            #     await websocket.send_text(response.delta)
            await asyncio.sleep(0)

            # if data["model"] != config["model"] or temp != config["temperature"]:
            #     config["model"] = data["model"]
            #     config["temperature"] = temp

            #     model_directory = "model"
            #     for file in os.listdir(model_directory):
            #         if file.endswith('.gguf') and config["model"].lower() in file:
            #             config["model_path"] = os.path.join(model_directory, file)
            #             break

           

    except Exception as e:
        print(e)
    finally:
        await websocket.close()

@app.websocket("/azure")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        config=load_azure_config()

        # model_kwargs = {"n_gpu_layers" : -1 if config["gpu"] else 0}
        # llm = LlamaCPP(
        #     model_path=config["model_path"],
        #     temperature=config["temperature"],
        #     max_new_tokens=max_new_tokens,
        #     context_window=3900,
        #     model_kwargs=model_kwargs,
        #     verbose=False,
        # )
        while True:
            data = await websocket.receive_json()
            print(data)
            print("azure route")
            prompt = data["userInput"]
            
            if prompt.lower() == "exit":
                print("Exiting chat.")
                break

            agent = data['agent']
            key=config['apikey']
            version=config['version']
            model=config['modelInput']
            endpoint=config['endpoint']

            # if model != config["model"] or endpoint!= config["endpoint"]:
            #     config["model"] = model
            #     config["endpoint"] = endpoint
            #     config["version"] = version
            #     config["key"] = key
            #     save_azure_config(config)
            client = AzureOpenAI(
                api_key = (key),
                api_version = version,
                azure_endpoint = (endpoint)
            )

            if agent == "None":
                response = client.chat.completions.create(
                    model=model, # model = "deployment_name".
                    messages=[
                        {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                        {"role": "user", "content": prompt}
                        
                    ]
                )
                for choice in response.choices:
                    await websocket.send_text(choice.message.content)
            else:
                persist_directory = os.path.join('db', agent)
                if os.path.exists(persist_directory):
                    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
                    db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)
                    docs = db.similarity_search(prompt, k=3)
                    context = docs[0].page_content
                    prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query:<s>[INST] {prompt} [/INST]"
                    prompt = prompt_template.format(context=context, prompt=prompt)
                    response = client.chat.completions.create(
                            model=model, # model = "deployment_name".
                            messages=[
                                {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                                {"role": "user", "content": prompt}
                                
                            ]
                        )
                    for choice in response.choices:
                            await websocket.send_text(choice.message.content)


            # model_kwargs = {"n_gpu_layers" : -1 if config["gpu"] else 0}
            # llm = LlamaCPP(
            #     model_path=config["model_path"],
            #     temperature=config["temperature"],
            #     max_new_tokens=max_new_tokens,
            #     context_window=3900,
            #     model_kwargs=model_kwargs,
            #     verbose=False,
            # )

            # response_iter = llm.stream_complete(prompt)

            # for response in response_iter:
            #     await websocket.send_text(response.delta)
            await asyncio.sleep(0)

            # if data["model"] != config["model"] or temp != config["temperature"]:
            #     config["model"] = data["model"]
            #     config["temperature"] = temp

            #     model_directory = "model"
            #     for file in os.listdir(model_directory):
            #         if file.endswith('.gguf') and config["model"].lower() in file:
            #             config["model_path"] = os.path.join(model_directory, file)
            #             break

           

    except Exception as e:
        print(e)
    finally:
        await websocket.close()


# class RequestData(BaseModel):
#     agent: str
#     file: UploadFile
@app.post("/create_agent")
async def upload_file(name: str = Form(...),file: UploadFile = File(...)):
        try:
            agentname = name
            uploaded_file = file
            # Process the uploaded file
            # Example: Save the file locally
            if not os.path.exists("uploads"):
                os.mkdir("uploads")
            file_path = f"uploads/{uploaded_file.filename}"
            with open(file_path, "wb") as file_object:
                file_object.write(await uploaded_file.read())
            persist_directory = 'db'
            doc_path = os.path.normpath(file_path)
            agent_directory = os.path.join(persist_directory, agentname)
            if not os.path.exists(agent_directory):
                os.makedirs(agent_directory)

            # Load the document
            if doc_path.endswith(".csv"):
                loader = CSVLoader(doc_path)
            elif doc_path.endswith(".pdf"):
                loader = PDFMinerLoader(doc_path)
            elif doc_path.endswith(".docx"):
                loader = TextLoader(doc_path)
            else:
                raise ValueError("Unsupported file format. Supported formats are CSV, PDF, and DOCX.")

            documents = loader.load()

            # Split the document into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=500)
            texts = text_splitter.split_documents(documents)

            # Create embeddings
            embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

            # Create ChromaDB and store document IDs
            db = Chroma.from_documents(texts, embeddings, persist_directory=agent_directory)
            db.persist()

            doc_ids_path = os.path.join(agent_directory, f"{agentname}_docids.txt")

            # Store document IDs in a file
            with open(doc_ids_path, "a") as f:
                for text_id, _ in enumerate(texts):
                    document_id = f"doc_{text_id}"
                    f.write(f"{document_id}\n")
            return JSONResponse(content={"agentname": name, "message": "agent created successfully"}) 
        



        except Exception as e:
            print(e)

@app.websocket("/configdata")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        print(data)
        if data == "Azure":
            azure_config=load_azure_config()
            await websocket.send_json(azure_config)
        elif data == "Vertex":
            vertex_config=load_vertex_config()
            await websocket.send_json(vertex_config)
        else:
            config=load_config()
            await websocket.send_json(config)

    except Exception as e:
        print(e)
    finally:
        await websocket.close()

def main():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()