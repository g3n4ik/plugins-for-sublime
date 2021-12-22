import torch
import youtokentome as yttm

from flask import Flask, request
from transformers import GPT2LMHeadModel
from time import time
import youtokentome as yttm
import torch

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def get_prediction():
    context = request.form.get("context")

    context = context.lstrip('\n')

    new_context = context[0]

    for i in range(1, len(context)):
        if new_context[-1] == '\n' and context[i] == '\n':
            continue
        new_context = new_context + context[i]

    context = new_context

    token_end = ""
    token_suffix = ""

    for pos in range(len(context) - 1, 0, -1):
        if context[pos] == '\n':
            break
        token_suffix = context[pos] + token_suffix

        print(f"Now token suffix {token_suffix}")

        flag = False

        for now_word in tokenizer.vocab():
            if token_suffix in now_word and len(now_word) > 1:
                print(now_word)
                token_end = now_word[now_word.rfind(token_suffix) + len(token_suffix)::]
                last_position = pos
                flag = True

        if not(flag):
            break

    context = context + token_end

    print(context)

    name = request.form.get('address').split('\\')[-1]
    context = name + "₣" + context

    print(f"Input context is {context}")

    inputs = tokenizer.encode(context)

    if len(inputs) > 384:
        inputs = inputs[len(inputs) - 384:]

    inputs = torch.tensor(inputs)

    generation_output = model.generate(
        inputs.unsqueeze(0), 
        return_dict_in_generate=True, 
        output_scores=True, 
        top_k=5, 
        num_beams=5, 
        num_return_sequences=5,
        max_length=len(inputs) + 5,
        diversity_penalty=0.75,
        num_beam_groups=5
    )

    return_value = ""
    decoded = tokenizer.decode(list(generation_output[0]))
    predictions = []
    cnt_added = 0

    for idx in range(5):
        predictions.append(token_end + decoded[idx][len(context)::].lstrip('\n').split('\n')[0].rstrip())

    print(f"Decoded predictions is {predictions}")

    predictions = list(set(predictions))

    for idx in range(len(predictions)):
        is_add = True
        for pref_id in range(0, len(predictions)):
            if pref_id == idx:
                continue
            if predictions[pref_id].startswith(predictions[idx]):
                is_add = False
        if is_add and cnt_added < 3:
            cnt_added += 1
            return_value = return_value + predictions[idx]
            if cnt_added < 3:
                return_value = return_value + '\n'

    return return_value


if __name__ == "__main__":
    model = GPT2LMHeadModel.from_pretrained("./gpt2-py-small")
    tokenizer = yttm.BPE("./gpt2-py-small/gitbpe-py.bpe")
    app.run(host="localhost", port=5342)
