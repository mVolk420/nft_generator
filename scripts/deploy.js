async function main() {
    const [deployer] = await ethers.getSigners();
  
    console.log("Deploying contract with:", deployer.address);
  
    const baseURI = "ipfs://your-ipfs-cid/output/";
    const NFT = await ethers.getContractFactory("ERC721Minter");
    const contract = await NFT.deploy(baseURI);
  
    console.log("✅ Contract deployed to:", contract.address);
  }
  
  main()
    .then(() => process.exit(0))
    .catch((err) => {
      console.error(err);
      process.exit(1);
    });
  