from flask import Flask
from .instruct import load_model, api_serve
import os
import json

app = Flask(__name__)

model_dir = "model"

config = {
    "host": "127.0.0.1",
    "port": "5173",
    "cert_file": "",
    "cert_key": ""
}

file_path=os.path.join(model_dir, "apiconfig.json")
if not os.path.exists(file_path):
    with open(file_path, "w") as json_file:
        json.dump(config, json_file)

@app.route('/v1/chat/completions', methods=['POST'])
def chat():
    api_serve()

def main():
        with open(file_path, "r") as json_file:
            config = json.load(json_file)
            host=config["host"]
            port=config["port"]
            cert_file=config["cert_file"]
            cert_key=config["cert_key"]
        if cert_file is not "" and cert_key is not "":
            print(f"Inference is working on https://{host}:{port}/v1/chat/completions. You can configure custom host IP and port, and ssl certificate via the apiconfig.txt file available at {file_path}")
            app.run(host=host, port=port, debug=False, ssl_context=(cert_file,cert_key))
        else:
            print(f"Inference is working on http://{host}:{port}/v1/chat/completions. You can configure custom host IP and port, and ssl certificate via the apiconfig.txt file available at {file_path}")
            app.run(host=host, port=port, debug=False)

if __name__ == "__main__":
    main()
