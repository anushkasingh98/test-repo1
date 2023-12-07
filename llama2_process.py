# from transformers import LlamaForCausalLM, CodeLlamaTokenizer

# tokenizer = CodeLlamaTokenizer.from_pretrained("codellama/CodeLlama-7b-hf")
# model = LlamaForCausalLM.from_pretrained("codellama/CodeLlama-7b-hf")

# PROMPT = '''def remove_non_ascii(s: str) -> str:
# """ <FILL_ME>
#     return result
# '''

# input_ids = tokenizer(PROMPT, return_tensors="pt")["input_ids"]
# generated_ids = model.generate(input_ids, max_new_tokens=128)

# filling = tokenizer.batch_decode(generated_ids[:, input_ids.shape[1]:], skip_special_tokens = True)[0]
# print(PROMPT.replace("<FILL_ME>", filling))

# from transformers import pipeline
# import torch

# generator = pipeline("text-generation",model="codellama/CodeLlama-7b-hf",torch_dtype=torch.float16, device_map="auto")
# generator('def remove_non_ascii(s: str) -> str:\n    """ <FILL_ME>\n    return result', max_new_tokens = 128, return_type = 1)

import vault
import os
import replicate

token = vault.get_Secret("replicate_key")
os.environ["REPLICATE_API_TOKEN"] = token

def create_base_prompt(file_contents,file_names):
    prompt = ""
    length = len(file_contents)
    # prompt = "I have a Python project with the following files: \n"
    for i in range(length):
        prompt = prompt + "\n" + file_names[i] + ": " + file_contents[i]
    # prompt = prompt + "\n Can you create a README file for this project?"
    return prompt

def custom_prompt(system_prompt,prompt):
    output = replicate.run(
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={
            "debug": False,
            "top_k": 50,
            "top_p": 1,
            "prompt": prompt,
            "temperature": 0.5,
            "system_prompt":system_prompt,
            "max_new_tokens": 500,
            "min_new_tokens": -1
        }
    )

    print(output)

    # https://stackoverflow.com/questions/56331795/printing-generator-objects-in-python
    res = ''.join([char for char in output])
    print("\nResponse: \n",res)

    return(res)

def control(file_contents,file_names):
    print("Inside CONTROL")
    prompt = create_base_prompt(file_contents,file_names)

    output = replicate.run(
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={
            "debug": False,
            "top_k": 50,
            "top_p": 1,
            "prompt": prompt,
            "temperature": 0.5,
            "system_prompt":"You will be provided with multiple file contents from one project, and your task is to create a README file for the project. Only respond with the README file contents.",
            "max_new_tokens": 500,
            "min_new_tokens": -1
        }
    )

    # print(output)

    # https://stackoverflow.com/questions/56331795/printing-generator-objects-in-python
    res = ''.join([char for char in output])
    print("\nResponse: \n",res)

    return(res)

# full_response = ''
# for item in output:
#     print("Inside for")
#     full_response += item
# print(full_response)
if __name__=="__main__":
    out = control(['#testing file content\n def sum():\n\treturn (1+2)'],['test.py'])
    print("Returned output: ",out)