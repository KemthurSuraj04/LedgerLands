// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Land {

    struct User {
        string name;
        uint age;
        string city;
        string aadharNumber;
        string panNumber;
        string document;
        string email;
        bool isVerified;
    }

    struct Landreg {
        uint id;
        uint area;
        string city;
        string state;
        uint landPrice;
        uint propertyPID;
        uint physicalSurveyNumber;
        string ipfsHash;
        string document;
        bool isVerified;
        bool isForSale;
    }

    address public landRegistrar;
    uint public landsCount;
    mapping(address => User) public users;
    mapping(uint => Landreg) public lands;
    mapping(address => uint[]) public userOwnedLands;
    mapping(uint => address) public landOwner;
    mapping(uint => address[]) public landOwnershipHistory;

    event UserRegistered(address indexed user);
    event UserVerified(address indexed user);
    event LandAdded(uint indexed landId);
    event LandVerified(uint indexed landId);
    event LandForSale(uint indexed landId);
    event LandSold(uint indexed landId, address indexed buyer, address indexed seller);
    event LandRemovedFromSale(uint landId);

    modifier onlyLandRegistrar() {
        require(msg.sender == landRegistrar, "Only Land Registrar can perform this action");
        _;
    }

    modifier onlyVerifiedUser() {
        require(users[msg.sender].isVerified, "User not verified");
        _;
    }

    constructor() {
        landRegistrar = msg.sender;
        users[msg.sender] = User("Registrar", 51, "Bengaluru", "111111", "1212d1X", "Hashed", "registrar@gmail.com", true);
        emit UserRegistered(msg.sender);
        emit UserVerified(msg.sender);
    }

    function registerUser(
        string memory _name,
        uint _age,
        string memory _city,
        string memory _aadharNumber,
        string memory _panNumber,
        string memory _document,
        string memory _email
    ) public {
        require(bytes(users[msg.sender].name).length == 0, "User already registered");
        users[msg.sender] = User(_name, _age, _city, _aadharNumber, _panNumber, _document, _email, false);
        emit UserRegistered(msg.sender);
    }

    function verifyUser(address _user) public onlyLandRegistrar {
        require(bytes(users[_user].name).length > 0, "User not registered");
        require(!users[_user].isVerified, "User already verified");
        users[_user].isVerified = true;
        emit UserVerified(_user);
    }

    function unverifyUser(address _user) public onlyLandRegistrar {
        require(users[_user].isVerified, "User is not verified");
        users[_user].isVerified = false;
    }

    function unverifyLand(uint _landId) public onlyLandRegistrar {
        require(lands[_landId].isVerified, "Land is not verified");
        lands[_landId].isVerified = false;
    }

    function addLand(
        uint _area,
        string memory _city,
        string memory _state,
        uint _landPrice,
        uint _propertyPID,
        uint _physicalSurveyNumber,
        string memory _ipfsHash,
        string memory _document
    ) public onlyVerifiedUser {
        landsCount++;
        lands[landsCount] = Landreg(
            landsCount,
            _area,
            _city,
            _state,
            _landPrice,
            _propertyPID,
            _physicalSurveyNumber,
            _ipfsHash,
            _document,
            false,
            false
        );
        landOwner[landsCount] = msg.sender;
        userOwnedLands[msg.sender].push(landsCount);
        emit LandAdded(landsCount);
    }

    function verifyLand(uint _landId) public onlyLandRegistrar {
        require(lands[_landId].id != 0, "Land not found");
        require(!lands[_landId].isVerified, "Land already verified");
        lands[_landId].isVerified = true;
        emit LandVerified(_landId);
    }

    function batchVerifyUsers(address[] memory _users) public onlyLandRegistrar {
        for (uint i = 0; i < _users.length; i++) {
            if (!users[_users[i]].isVerified && bytes(users[_users[i]].name).length > 0) {
                users[_users[i]].isVerified = true;
                emit UserVerified(_users[i]);
            }
        }
    }

    function batchUnverifyUsers(address[] memory _users) public onlyLandRegistrar {
        for (uint i = 0; i < _users.length; i++) {
            if (users[_users[i]].isVerified) {
                users[_users[i]].isVerified = false;
            }
        }
    }

    function batchVerifyLands(uint[] memory _landIds) public onlyLandRegistrar {
        for (uint i = 0; i < _landIds.length; i++) {
            if (!lands[_landIds[i]].isVerified && lands[_landIds[i]].id != 0) {
                lands[_landIds[i]].isVerified = true;
                emit LandVerified(_landIds[i]);
            }
        }
    }

    function batchUnverifyLands(uint[] memory _landIds) public onlyLandRegistrar {
        for (uint i = 0; i < _landIds.length; i++) {
            if (lands[_landIds[i]].isVerified) {
                lands[_landIds[i]].isVerified = false;
            }
        }
    }

    function putLandForSale(uint _landId) public {
        require(users[msg.sender].isVerified, "User not verified");
        require(landOwner[_landId] == msg.sender, "You are not the owner of this land");
        require(lands[_landId].isVerified, "Land is not verified");
        require(!lands[_landId].isForSale, "Land already for sale");

        lands[_landId].isForSale = true;
        emit LandForSale(_landId);
    }

    function removeLandFromSale(uint _landId) public {
        require(landOwner[_landId] == msg.sender, "You are not the owner of this land");
        require(lands[_landId].isForSale == true, "This land is not listed for sale");

        // Remove land from sale
        lands[_landId].isForSale = false;
        
        emit LandRemovedFromSale(_landId);
    }

    function buyLand(uint _landId) public payable {
        require(lands[_landId].isForSale, "Land is not for sale");
        require(lands[_landId].isVerified, "Land is not verified");
        require(msg.value == lands[_landId].landPrice, "Incorrect payment amount");

        address seller = landOwner[_landId];
        require(seller != msg.sender, "Seller cannot buy their own land");

        // Record historical ownership
        landOwnershipHistory[_landId].push(seller);

        // Transfer ownership
        landOwner[_landId] = msg.sender;

        // Update user land ownership mappings
        userOwnedLands[seller] = removeLandFromUser(userOwnedLands[seller], _landId);
        userOwnedLands[msg.sender].push(_landId);

        // Mark land as not for sale
        lands[_landId].isForSale = false;

        // Transfer funds to the seller
        payable(seller).transfer(msg.value);

        emit LandSold(_landId, msg.sender, seller);
    }

    function getLandsForSale() public view returns (uint[] memory) {
        uint[] memory landsForSale = new uint[](landsCount);
        uint counter = 0;

        for (uint i = 1; i <= landsCount; i++) {
            if (lands[i].isForSale) {
                landsForSale[counter] = i;
                counter++;
            }
        }

        uint[] memory result = new uint[](counter);
        for (uint i = 0; i < counter; i++) {
            result[i] = landsForSale[i];
        }

        return result;
    }

    function getLandsOwnedByUser(address _user) public view returns (uint[] memory) {
        return userOwnedLands[_user];
    }

    function removeLandFromUser(uint[] storage landsArray, uint _landId) internal returns (uint[] storage) {
        for (uint i = 0; i < landsArray.length; i++) {
            if (landsArray[i] == _landId) {
                landsArray[i] = landsArray[landsArray.length - 1];
                landsArray.pop();
                break;
            }
        }
        return landsArray;
    }


    function subdivideLand(uint _landId, uint[] memory _areas, uint[] memory _prices) public {
        require(landOwner[_landId] == msg.sender, "You are not the owner of this land");
        require(lands[_landId].isVerified, "Land is not verified");
        require(_areas.length == _prices.length, "Mismatch in areas and prices");

        uint totalArea = 0;
        for (uint i = 0; i < _areas.length; i++) {
            totalArea += _areas[i];
        }
        require(totalArea <= lands[_landId].area, "Total area exceeds original land area");

        // Remove ownership of the original land
        delete landOwner[_landId];
        userOwnedLands[msg.sender] = removeLandFromUser(userOwnedLands[msg.sender], _landId);

        // Mark the original land as unverified
        lands[_landId].isVerified = false;
        lands[_landId].isForSale=false;

        for (uint i = 0; i < _areas.length; i++) {
            landsCount++;
            lands[landsCount] = Landreg(
                landsCount,
                _areas[i],
                lands[_landId].city,
                lands[_landId].state,
                _prices[i],
                lands[_landId].propertyPID,
                lands[_landId].physicalSurveyNumber,
                lands[_landId].ipfsHash,
                lands[_landId].document,
                true,  // Verified for new subdivided land
                false
            );
            landOwner[landsCount] = msg.sender;
            userOwnedLands[msg.sender].push(landsCount);
            emit LandAdded(landsCount);
        }

        // Update the original land's area
        lands[_landId].area -= totalArea;
    }

    function mergeLands(uint[] memory _landIds, uint _newLandPrice) public {
        require(_landIds.length > 1, "At least two lands must be merged");

        string memory city = lands[_landIds[0]].city;
        string memory state = lands[_landIds[0]].state;
        uint totalArea = 0;

        for (uint i = 0; i < _landIds.length; i++) {
            require(landOwner[_landIds[i]] == msg.sender, "You are not the owner of one or more lands");
            require(lands[_landIds[i]].isVerified, "One or more lands are not verified");
            require(
                keccak256(bytes(lands[_landIds[i]].city)) == keccak256(bytes(city)) &&
                keccak256(bytes(lands[_landIds[i]].state)) == keccak256(bytes(state)),
                "Lands must be in the same city and state"
            );

            totalArea += lands[_landIds[i]].area;

            // Remove the old land mappings
            delete landOwner[_landIds[i]];
            userOwnedLands[msg.sender] = removeLandFromUser(userOwnedLands[msg.sender], _landIds[i]);

            // Mark the original lands as unverified
            lands[_landIds[i]].isVerified = false;
            lands[_landIds[i]].isForSale=false;
        }

        // Create a new merged land
        landsCount++;
        lands[landsCount] = Landreg(
            landsCount,
            totalArea,
            city,
            state,
            _newLandPrice,
            lands[_landIds[0]].propertyPID,
            lands[_landIds[0]].physicalSurveyNumber,
            lands[_landIds[0]].ipfsHash,
            lands[_landIds[0]].document,
            true,  // Verified for merged land
            false
        );

        landOwner[landsCount] = msg.sender;
        userOwnedLands[msg.sender].push(landsCount);
        emit LandAdded(landsCount);
    }

    function getOwnershipHistory(uint _landId) public view returns (address[] memory) {
        return landOwnershipHistory[_landId];
        
    }

    function getCurrentOwner(uint _landId) public view returns (address) {
        return landOwner[_landId];
    }

}