def tn2():

    print("""

###########################################################

##grad_fn = ms.grad(model, None, optimizer.parameters)

grad_fn = ms.value_and_grad(model, None, optimizer.parameters)

def train_step(data, seq_length, label):
    loss, grads = grad_fn(data, seq_length, label)
    optimizer(grads)
    return loss

from tqdm import tqdm

steps = 500
with tqdm(total=steps) as t:
    for i in range(steps):
        loss = train_step(data, seq_length, label)
        t.set_postfix(loss=loss)
        t.update(1)



### Finally, let’s observe the model effect after 500 steps of training. First, use the model to predict 
### possible path scores and candidate sequences.
score, history = model(data, seq_length)
score


## Perform post-processing on the predicted score.
predict = post_decode(score, history, seq_length)
predict


#####  convert the predicted index sequence into a label sequence, print the output 
###  result, and view the effect.
idx_to_tag = {idx: tag for tag, idx in tag_to_idx.items()}

def sequence_to_tag(sequences, idx_to_tag):
    outputs = []
    for seq in sequences:
        outputs.append([idx_to_tag[i] for i in seq])
    return outputs


##########################################################
# train_dataset = ds.NumpySlicesDataset({
#     "data":data,
#     "label":label, 
#     "seq_length":seq_length
# }, shuffle = True)

## or
# train_dataset = ds.GeneratorDataset((data, label, seq_length)
#                                     , column_names = ["data", "label", "seq_length"], shuffle = True)

# train_dataset = train_dataset.batch(32)


model_t = Model(
    network = model,
    loss_fn=None,
    optimizer=optimizer)


model_t.train(
    10,
    train_dataset
)



###Export into MindIR
from mindspore.train.serialization import save_checkpoint, export  
##OR## 
from mindspore import export

export(net, dummy_input, file_name='model',file_format='MINDIR')
    
    """)