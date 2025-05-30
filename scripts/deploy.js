require("dotenv").config(); 

async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("📦 Deploying with:", deployer.address);
  
    const baseURI = process.env.LIGHTHOUSE_BASE_URI;
  
    const NFT = await ethers.getContractFactory("ERC721Minter");
    const contract = await NFT.deploy(baseURI);
  
    await contract.waitForDeployment();
    console.log("✅ Contract deployed at:", await contract.getAddress());
  }
  
  main().catch((err) => {
    console.error("❌ Deployment failed:", err);
    process.exit(1);
  });
  