// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// ✅ Importiert die erweiterte ERC721-Logik inkl. Enumerable (z. B. totalSupply, tokenByIndex)
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/token/common/ERC2981.sol";

// ✅ Importiert Zugriffskontrolle: `onlyOwner` & Besitzer-Logik
import "@openzeppelin/contracts/access/Ownable.sol";

// 🔨 Der NFT-Vertrag: Jeder kann minten, aber nur der Owner kann die baseURI ändern
contract ERC721Minter is ERC721Enumerable, ERC2981, Ownable {
    // 🔗 Die Basis-URL für alle Metadaten (z. B. IPFS baseURI)
    string private _baseTokenURI;

    // 🆔 Zähler für die nächste Token-ID (beginnt bei 1)
    uint256 public nextTokenId = 1;

    // 🏗️ Konstruktor: Setzt Collection-Namen, Symbol & IPFS-BaseURI + Owner
    constructor(string memory name_, string memory symbol_, string memory baseURI)
        ERC721(name_, symbol_)            // Name + Symbol
        Ownable(msg.sender)                          // Setzt den Owner des Contracts auf den Deployenden
    {
        _baseTokenURI = baseURI;
         _setDefaultRoyalty(msg.sender, 100);         // 1% Royalties an den Owner
    }

    // 🪙 Öffentliche Mint-Funktion – jeder darf minten
    function mint() external {
        _safeMint(msg.sender, nextTokenId);          // Mintet neues NFT an den Absender
        nextTokenId++;                               // Erhöht Token-ID-Zähler für nächstes NFT
    }

    // ⚙️ Nur Owner darf die baseURI nachträglich ändern (z. B. bei neuem IPFS-Upload)
    function setBaseURI(string memory newBaseURI) external onlyOwner {
        _baseTokenURI = newBaseURI;
    }

    // 📤 Gibt die aktuelle baseURI zurück → wird intern von tokenURI() verwendet
    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }
    // 💰 Royalty-Support (EIP-2981)
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721Enumerable, ERC2981)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
