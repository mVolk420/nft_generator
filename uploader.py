import os
import requests
from dotenv import load_dotenv

# Lade API-Key aus .env-Datei
load_dotenv()
API_KEY = os.getenv("LIGHTHOUSE_API_KEY")

# API-Endpunkt + Ordnerpfad
API_URL = "https://node.lighthouse.storage/api/v0/add?wrap-with-directory=true"

def upload_folder(folder_path):
    files = []
    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith(".json") or filename.endswith(".png"):
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, folder_path)
                files.append(('file', (rel_path, open(full_path, 'rb'))))

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    print(f"📦 Lade {len(files)} Dateien hoch...")

    response = requests.post(API_URL, headers=headers, files=files)

    if response.status_code == 200:
        root_cid = response.json()["Hash"]
        base_uri = f"ipfs://{root_cid}/"
        print("\n✅ Upload erfolgreich!")
        print(f"🔗 baseURI: {base_uri}")
        print(f"🌍 Beispiel-Metadaten: https://gateway.lighthouse.storage/ipfs/{root_cid}/1.json")
        print(f"🖼️ Beispiel-Bild:      https://gateway.lighthouse.storage/ipfs/{root_cid}/1.png")
        return base_uri
    else:
        print("❌ Upload fehlgeschlagen:")
        print(response.status_code)
        print(response.text)
        return None