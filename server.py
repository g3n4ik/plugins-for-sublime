from flask import Flask, request
from transformers import GPT2LMHeadModel
from time import time
import youtokentome as yttm
import torch

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def get_prediction():
    context = request.form.get('context')
    address = request.form.get('address').split('\\')[-1]
    context = address + "₣" + context

    model = GPT2LMHeadModel.from_pretrained('C:/Users/1/gpt2-py-small/gpt2-py-small')
    model.eval()

    tokenizer = yttm.BPE('C:/Users/1/gpt2-py-small/gpt2-py-small/gitbpe-py.bpe')
    inputs = tokenizer.encode(context)

    if len(inputs) > 384:
        inputs = inputs[len(inputs) - 384:]

    inputs = torch.tensor(inputs)

    generation_output = model.generate(inputs.unsqueeze(0), return_dict_in_generate=True, output_scores=True, top_k=5, num_beams=5, num_return_sequences=5, max_length = len(context) + 5, diversity_penalty = 0.75, num_beam_groups = 5)

    return_value = ""
    decoded = tokenizer.decode(list(generation_output[0]))
    predictions = []
    cnt_added = 0

    for idx in range(5):
        predictions.append(decoded[idx][len(context) + 1::].split('\n')[0].rstrip())
        print(decoded[idx][len(context) + 1::])
        print()

    print(predictions)

    predictions = list(set(predictions))

    for idx in range(len(predictions)):
        is_add = True
        for pref_id in range(0, len(predictions)):
            if pref_id == idx:
                continue
            if len(predictions[idx]) > len(predictions[pref_id]):
                continue
            is_pref = True
            for now_char in range(len(predictions[idx])):
                if predictions[idx][now_char] != predictions[pref_id][now_char]:
                    is_pref = False
                    break
            if is_pref:
                is_add = False
        if is_add and cnt_added < 3:
            cnt_added += 1
            return_value = return_value + predictions[idx]
            if cnt_added < 3:
                return_value = return_value + '\n'

    return return_value

if __name__ == '__main__':
    app.run(host='localhost', port=5342)