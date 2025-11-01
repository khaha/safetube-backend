import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.optim import AdamW   # <-- thêm dòng này nè
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from vncorenlp import VnCoreNLP
import pandas as pd
from ultralytics import YOLO


# --- BEGIN VNCORENLP AUTO-SETUP ---
import socket
from vncorenlp import VnCoreNLP

def _check_port(host: str, port: int, timeout: float = 0.8) -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.close()
        return True
    except:
        return False

if _check_port("127.0.0.1", 54053):
    print("✅ VnCoreNLP: detected server on 127.0.0.1:54053 — using server mode")
    rdrsegmenter = VnCoreNLP("http://127.0.0.1:54053", annotators="wseg", max_heap_size='-Xmx2g')
else:
    print("⚙️ VnCoreNLP: no server detected — using local (jar) mode")
    rdrsegmenter = VnCoreNLP("VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx2g', backend='local')
# --- END VNCORENLP AUTO-SETUP ---


data = {
    'text': [
        "Đánh nhau dao búa máu me gun knife violence", "Sex 18+ nude porn hentai sexy nsfw", "Mày ngu chết mẹ mày hate kỳ thị thù địch", "Video an toàn hay cute safe", "Khủng bố bom nổ terrorist bomb", "Tin giả fake news vaccine chết misinformation", "Bạo lực súng knife fight beat", "Cute puppy non-toxic safe", "Hentai sexy girl 18+ porn", "Lật đổ chính quyền extremist hate speech", "Chữa ung thư lá cây fake news", "Kêu gọi bạo lực revolution violence" 
        # Mày add 500+ dòng toxic thật từ crawl YouTube/FB VN để accuracy cao, ví dụ dùng tool crawl comment
    ],
    'label': [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1]
}
df = pd.DataFrame(data)

def preprocess(text):
    segmented = rdrsegmenter.tokenize(text)
    return ' '.join([' '.join(sentence) for sentence in segmented])

df['text'] = df['text'].apply(preprocess)

train_texts, val_texts, train_labels, val_labels = train_test_split(df['text'], df['label'], test_size=0.2)

tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")

class ToxicDataset(Dataset):
    def __init__(self, texts, labels):
        self.encodings = tokenizer(texts.tolist(), truncation=True, padding=True, max_length=128)
        self.labels = labels.tolist()

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = ToxicDataset(train_texts, train_labels)
val_dataset = ToxicDataset(val_texts, val_labels)

model = AutoModelForSequenceClassification.from_pretrained("vinai/phobert-base", num_labels=2)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

optimizer = AdamW(model.parameters(), lr=1e-5)

train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)

for epoch in range(3):
    model.train()
    for batch in train_loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

model.eval()
val_loader = DataLoader(val_dataset, batch_size=8)
preds = []
true = []
for batch in val_loader:
    batch = {k: v.to(device) for k, v in batch.items()}
    with torch.no_grad():
        outputs = model(**batch)
    logits = outputs.logits
    preds.extend(torch.argmax(logits, dim=1).cpu().numpy())
    true.extend(batch['labels'].cpu().numpy())

print("Accuracy:", accuracy_score(true, preds))
print("F1:", f1_score(true, preds))

model.save_pretrained("toxic_model")
tokenizer.save_pretrained("toxic_model")

# YOLO fine-tune xịn (mày crawl data violence VN: images with labels gun/knife/blood, use LabelImg tool to label, save as yaml file)
yolo = YOLO('yolov8n.pt')
yolo.train(data='path/to/your_violence_yaml.yaml', epochs=10, imgsz=640, batch=8, workers=4)  # Xịn: Multi params for better accuracy
yolo.export(format='torchscript')  # Save model
