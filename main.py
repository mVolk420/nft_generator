import yaml
from generator import NFTGenerator
import uploader

if __name__ == "__main__":
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    generator = NFTGenerator(
        asset_path="./assets",
        output_path="./output",
        num_nfts=20,
        layer_config=config
    )
    generator.generate_all()
    uploader.upload_folder("./output")
