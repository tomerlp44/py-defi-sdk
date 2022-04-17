from fireblocks_sdk import FireblocksSDK, TransferPeerPath ,DestinationTransferPeerPath, ONE_TIME_ADDRESS, VAULT_ACCOUNT, \
    EXTERNAL_WALLET
from chain import Chain


CHAIN_TO_ASSET_ID = {
    Chain.MAINNET: 'ETH',
    Chain.ROPSTEN: 'ETH_TEST',
    Chain.KOVAN: 'ETH_TEST2',
    Chain.BSC: 'BNB_BSC',
    Chain.BSC_TEST: 'BNB_TEST',
    Chain.POLYGON: 'MATIC_POLYGON'
}


class Web3Bridge:
    def __init__(self, fb_api_client: FireblocksSDK, vault_account_id: str, external_wallet_id: str, chain: Chain):
        self.fb_api = fb_api_client
        self.source_vault_id = vault_account_id
        self.external_wallet_address = external_wallet_id
        self.chain = chain

    def send_transaction(self, tx_data, note=None):
        if not note:
            note = ''
        # if type(self.external_wallet_id) == EXTERNAL_WALLET:
        #     dest = DestinationTransferPeerPath(EXTERNAL_WALLET, self.external_wallet_id)
        # else:
        #     dest = DestinationTransferPeerPath(ONE_TIME_ADDRESS, one_time_address=self.external_wallet_id)
        return self.fb_api.create_transaction(
            tx_type="CONTRACT_CALL",
            asset_id=CHAIN_TO_ASSET_ID[self.chain],
            source=TransferPeerPath(VAULT_ACCOUNT, self.source_vault_id),
            amount="0",
            destination=DestinationTransferPeerPath(ONE_TIME_ADDRESS, one_time_address={"address": self.external_wallet_address}),
            note=note,
            extra_parameters={
                "contractCallData": tx_data["data"]
            }
        )