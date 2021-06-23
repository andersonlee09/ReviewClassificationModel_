import torch
from importlib import import_module
key = {
    1: '真实评论',
    0: '虚假评论',
}

model_name = 'bert'
x = import_module('models.' + model_name)
config = x.Config('THUCNews')
model = x.Model(config).to(config.device)
model.load_state_dict(torch.load(config.save_path, map_location='cuda' if torch.cuda.is_available() else 'cpu'))


def build_predict_text(text):
    token = config.tokenizer.tokenize(text)
    token = ['[CLS]'] + token
    seq_len = len(token)
    mask = []
    token_ids = config.tokenizer.convert_tokens_to_ids(token)
    pad_size = config.pad_size
    if pad_size:
        if len(token) < pad_size:
            mask = [1] * len(token_ids) + ([0] * (pad_size - len(token)))
            token_ids += ([0] * (pad_size - len(token)))
        else:
            mask = [1] * pad_size
            token_ids = token_ids[:pad_size]
            seq_len = pad_size
    ids = torch.LongTensor([token_ids])
    seq_len = torch.LongTensor([seq_len])
    mask = torch.LongTensor([mask])
    return ids, seq_len, mask


def predict(text):
    """
    单个文本预测
    :param text:
    :return:
    """
    data = build_predict_text(text)
    with torch.no_grad():
        outputs = model(data)
        num = torch.argmax(outputs)
    return key[int(num)]


if __name__ == '__main__':
    data = "这东西太烂了，我不喜欢"
    print(predict(data))