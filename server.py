import torch
import youtokentome as yttm

from flask import Flask, request
from transformers import GPT2LMHeadModel

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def get_prediction():
    context = request.form.get("context")
    name = request.form.get("address").split('/')[-1]

    model = GPT2LMHeadModel.from_pretrained("./gpt2-py-small")
    model.eval()

    tokenizer = yttm.BPE("./gpt2-py-small/gitbpe-py.bpe")
    inputs = tokenizer.encode(context)
    inputs = torch.tensor(inputs)

    generation_output = model.generate(
        inputs.unsqueeze(0), 
        return_dict_in_generate=True, 
        output_scores=True, 
        top_k=3, 
        num_beams=5, 
        num_return_sequences=5,
        max_length=len(inputs) + 5,
    )

    predictions = ""
    decoded = tokenizer.decode(list(generation_output[0]))

    for idx in range(3):
        if idx > 0:
            predictions = predictions + '\n'
        predictions = predictions + decoded[idx][len(context)::].split('\n')[0]

    return predictions


if __name__ == "__main__":
    app.run(host="localhost", port=5342)
