pragma solidity ^0.5.0;

// Imports


import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Mintable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

// Import another file from the same folder:
import "./FileNmae.sol";


/*----------------------------------------------------------------------------*/
/*----------------------------------------------------------------------------*/

// Token Contract Solidity Code

//ERC721
contract ArtToken is ERC721Full {
    constructor() public ERC721Full("ArtToken", "ART") {}

    function registerArtwork(address owner, string memory tokenURI)
        public
        returns (uint256)
    {
        uint256 tokenId = totalSupply();
        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        return tokenId;
    }
}


// ERC20
contract XP_Token is ERC20, ERC20Detailed {
    address payable owner;

    modifier onlyOwner {
        // @TODO: add a `require` to check if `owner` is the `msg.sender`
        require(msg.sender == owner, "You do not have permission to mint these tokens!");
        _; // this underscore sends us back to the function that called this modifier
    }

    // @TODO: Pass the required parameters to `ERC20Detailed`
    constructor(uint initial_supply) ERC20Detailed("XP_Token", "XPT",18) public {
        // @TODO: Set the owner to be `msg.sender`
        owner = msg.sender;
        // @TODO: Call the internal `_mint` function to give `initial_supply` to the `owner`
        _mint(owner, initial_supply);
    }

    // @TODO: Add the `onlyOwner` modifier to this function after `public`
    function mint(address recipient, uint amount) public onlyOwner {
        // @TODO: Call the internal `_mint` function and pass the `recipient` and `amount` variables
        _mint(recipient, amount);
    }
}

/*----------------------------------------------------------------------------*/
/*----------------------------------------------------------------------------*/

// NFT Certificate Solidity Code

contract certificate is ERC721Full {
    constructor() public ERC721Full ("certificate","CERT") {}

    function awardCertificate(address student, string memory tokenURI)
        public
        returns(uint256)
        {
            uint256 newCertificateId = totalSupply();
            _mint(student, newCertificateId);
            _setTokenURI(newCertificateId, tokenURI);

            return newCertificateId;
        }
}