import os
import random
import json
from PIL import Image

class NFTGenerator:
    def __init__(self, asset_path="./assets", output_path="./output", num_nfts=10, layer_config=None):
        self.asset_path = asset_path
        self.output_path = output_path
        self.num_nfts = num_nfts
        self.layer_config = layer_config or {}

    def _generate_image(self, token_id):
        layers = []
        traits = []

        for layer_name, layer_info in self.layer_config.items():
            trait_weights = layer_info.get("traits", {})
            probability = layer_info.get("probability", 1.0)

            # Layer überspringen, falls er zufällig nicht erscheinen soll
            if random.random() > probability:
                continue

            trait_files = list(trait_weights.keys())
            weights = list(trait_weights.values())

            selected_file = random.choices(trait_files, weights=weights, k=1)[0]

            image_path = os.path.join(self.asset_path, layer_name, selected_file)
            layer_image = Image.open(image_path).convert("RGBA")
            layers.append(layer_image)

            traits.append({
                "trait_type": layer_name,
                "value": selected_file.replace(".png", "")
            })

        if not layers:
            print(f"[WARN] Token {token_id} hat keine sichtbaren Layer.")
            return []

        final_image = layers[0]
        for layer in layers[1:]:
            final_image = Image.alpha_composite(final_image, layer)

        os.makedirs(self.output_path, exist_ok=True)
        img_path = os.path.join(self.output_path, f"{token_id}.png")
        final_image.save(img_path)

        return traits

    def _generate_metadata(self, token_id, traits):
        metadata = {
            "name": f"MyNFT #{token_id}",
            "description": "Ein Beispiel-NFT aus Python generiert.",
            "image": f"{token_id}.png",
            "attributes": traits
        }

        with open(os.path.join(self.output_path, f"{token_id}.json"), "w") as f:
            json.dump(metadata, f, indent=4)

    def generate_all(self):
        for token_id in range(1, self.num_nfts + 1):
            traits = self._generate_image(token_id)
            self._generate_metadata(token_id, traits)
        print(f"{self.num_nfts} NFTs erfolgreich generiert.")
