require("dotenv").config();

async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("📦 Deploying with:", deployer.address);

    const name = process.env.NFT_NAME || "MyNFTCollection";
    const symbol = process.env.NFT_SYMBOL || "MNFT";
    const baseURI = process.env.LIGHTHOUSE_BASE_URI;

    const royaltyReceiver = process.env.ROYALTY_RECEIVER || deployer.address;
    const royaltyBps = parseInt(process.env.ROYALTY_BPS || "100", 10);

    const NFT = await ethers.getContractFactory("ERC721Minter");
    const contract = await NFT.deploy(name, symbol, baseURI, royaltyReceiver, royaltyBps);

    await contract.waitForDeployment();
    console.log("✅ Contract deployed at:", await contract.getAddress());
}

main().catch((err) => {
    console.error("❌ Deployment failed:", err);
    process.exit(1);
});
