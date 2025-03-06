const Land = artifacts.require("Land");

contract("Land Contract", accounts => {
    let land;
    const [owner, seller, buyer] = accounts;

    before(async () => {
        land = await Land.deployed();
    });

    it("should deploy the contract", async () => {
        const landInspector = await land.Land_Inspector();
        assert.equal(landInspector, owner, "Land inspector should be the contract owner");
    });

    it("should register a seller", async () => {
        await land.SellerMapping(seller, { from: owner });
        const sellerData = await land.SellerMapping(seller);
        assert.equal(sellerData.id, seller, "Seller ID should be registered correctly");
    });

    it("should allow the land inspector to verify a seller", async () => {
        await land.verifySeller(seller, { from: owner });
        const isVerified = await land.SellerVerification(seller);
        assert.equal(isVerified, true, "Seller should be verified by the inspector");
    });

    it("should reject a seller", async () => {
        await land.rejectSeller(seller, { from: owner });
        const isRejected = await land.SellerRejection(seller);
        assert.equal(isRejected, true, "Seller should be rejected by the inspector");
    });

    it("should allow payment to be made to the seller", async () => {
        const landId = 1;
        const initialBalance = await web3.eth.getBalance(seller);
        const paymentAmount = web3.utils.toWei('1', 'ether');

        // Make the payment
        await land.payment(seller, landId, { from: buyer, value: paymentAmount });

        const newBalance = await web3.eth.getBalance(seller);
        assert.isTrue(parseInt(newBalance) > parseInt(initialBalance), "Seller should receive the payment");
    });

    it("should prevent multiple payments for the same land", async () => {
        const landId = 1;
        try {
            await land.payment(seller, landId, { from: buyer, value: web3.utils.toWei('1', 'ether') });
            assert.fail("Payment should not be allowed for the same land again");
        } catch (err) {
            assert.include(err.message, "Payment already received", "Expected error message");
        }
    });

    it("should verify the land inspector role", async () => {
        const isInspector = await land.isLandInspector(owner);
        assert.equal(isInspector, true, "Owner should be a land inspector");
    });

    // Additional tests can be added for other functionalities like adding land, requesting land, etc.
});
