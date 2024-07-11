# Prompts & Responses

This directory contains the dialogue prompts of the experiment, as well as the responses generated through conversational models.

## Model Responses

### **BlenderBot**
[GitHub Repo](https://github.com/seungguini/ParlAI_blender)
1. Install dependencies
    ```bash
        pip3 install -r requirements.txt
    ```

2. Run setup script
   ```bash
   python3 setup.py develop
   ```

3. Export python path
    ```bash
    export PYTHONPATH=$PWD:$PWD/parlai
    ```

4. Place data
5. Run script
    ```bash
    python3 parlai/scripts/safe_interactive.py -t blended_skill_talk -mf zoo:blender/blender_3B/model --include-personas true -sc true -scip esl_prompts.txt -scop generated_outputs --chateval-multi true --single-turn false
    ```


### **BlenderBot 2**

[GitHub Repo](https://github.com/seungguini/ParlAI_blender)

1. Format prompt
   - Covert `txt` to `json` format outlined [here](https://parl.ai/docs/tutorial_task.html#json-file-format-instead-of-text-file-format) (script in `research_sedoc/data_scripts/scripts/txt_to_json.py` )
   - Put `json` files inside `path/to/parlai_recent`
2. Install dependencies
    ```bash
    pip3 install -r requirements.txt
    ```
3. Run setup script
   ```bash
   python3 setup.py develop
   ```
4. Start Python Search server
    - Search engine [repo](https://github.com/JulesGM/ParlAI_SearchEngine.git)
    - Side steps [this issue](https://github.com/facebookresearch/ParlAI/issues/3829)
    - Demo [colab](https://colab.research.google.com/drive/1a8dh0NPVp2LV5P19xRCm_qnqhRRI7z-U?usp=sharing)
    
    ```bash
    git clone https://github.com/JulesGM/ParlAI_SearchEngine.git
    cd ParlAI_SearchEngine/ # into 
    
    python search_server.py serve --host 0.0.0.0:8080 & # & runs the command in the background
    
    # Test server
    curl -X POST "http://0.0.0.0:8080" -d "q=baseball&n=1"
    ```
    
5. Run script:

    - In the ParlAI_blender repo:
    
    3B model
    
    ```bash
    python parlai/scripts/eval_model.py --task jsonfile --jsonfile-datapath $PWD/esl2_prompts_huda.json --world-logs outputfile --model-file zoo:blenderbot2/blenderbot2_3B/model --search_server 0.0.0.0:8080
    ```
    
    400M model
    
    ```bash
    python parlai/scripts/eval_model.py --task jsonfile --jsonfile-datapath $PWD/esl2_prompts_huda.json --world-logs outputfile --model-file zoo:blenderbot2/blenderbot2_400M/model --search_server 0.0.0.0:8080
    ```

### **Plato2**
[Repo link](https://github.com/seungguini/Knover)

1. Clone repository
    ```bash
    git clone https://github.com/seungguini/Knover.git
    ```

2. Install dependencies

    *Taken from [original repo instructions](https://github.com/seungguini/Knover#requirements-and-installation)*

    * python version >= 3.7
    * paddlepaddle-gpu version >= 2.0.0
        * You can install PaddlePaddle following [the instructions](https://www.paddlepaddle.org.cn/documentation/docs/en/install/index_en.html).
        * The specific version of PaddlePaddle is also based on your [CUDA version](https://developer.nvidia.com/cuda-downloads) (recommended version: 10.1) and [CuDNN version](https://developer.nvidia.com/rdp/cudnn-download) (recommended version: 7.6). See more information on [PaddlePaddle document about GPU support](https://www.paddlepaddle.org.cn/documentation/docs/en/install/index_en.html#paddlepaddle-s-support-for-gpu)
    * sentencepiece
    * termcolor
    * If you want to run distributed training, you'll also need [NCCL](https://developer.nvidia.com/nccl/nccl-download)
    * Install Knover locally:

    ```bash
    git clone https://github.com/PaddlePaddle/Knover.git
    cd Knover
    pip3 install -e .
    ```

3. Download pre-trained model
    ```bash
    MODEL_SIZE=24L # can be eitehr 24L or 32L. See original model docs for more information.
    cd /path/to/Knover
    wget https://baidu-nlp.bj.bcebos.com/PLATO-2/${MODEL_SIZE}.tar
    tar xf ${MODEL_SIZE}.tar
    ```

4. Run the model

    ```bash
    # For 24L model
    bash ./scripts/local/job.sh ./projects/PLATO-2/pretrain/24L_infer.conf

    # For 32L model
    bash ./scripts/local/job.sh ./projects/PLATO-2/pretrain/32L_infer.conf
    ```


### **GPT3**

[Repo link](https://github.com/seungguini/GPT3/tree/master)

1. Clone repository
    ```bash
    git clone https://github.com/seungguini/GPT3.git
    ```

2. Install dependencies
    ```bash
    pip3 install -r requirements.txt
    ```

3. Set OpenAI [API Key](https://openai.com/api/)

    ```bash
    # .env
    API_KEY=YOUR_API_KEY_HERE
    ```

4. Place prompt files + set dataset name in `generate_gpt3_prompts.py`
    - Format should follow `test_prompts.txt`
    - Change `DATASET_NAME` variable to the dataset name. IE, for `test_prompts.txt`, `DATASET_NAME="test"`

5. Run script
    ```bash
    python3 generate_gpt3_prompts.py
    ```
