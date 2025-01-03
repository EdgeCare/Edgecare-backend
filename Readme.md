## This repo contains all API controllers, RAG system, Multi-agent message passing logic of the EdgeCare org.
### How to setup:
- First, create/ activate virtual env:
        create:  python -m venv myenv
        activate:  source myenv/bin/activate

- Install PyTorch suitable for your system's CUDA version by following the [official instructions](https://pytorch.org/get-started/locally/) (2.1.1+cu121 in our case).

- `Git-lfs` is required to download and load corpora for the first time.

- Then, install the remaining requirements using: `pip install -r requirements.txt`

- Re-install huggingfacehub using following commands:
        `pip uninstall huggingface_hub -y`  and 

        `pip install huggingface_hub==0.24.0`




## To Run Server

Start server in port 8000 without 8080/proxy/
``` uvicorn main:app --host 0.0.0.0 --port 8000 ```