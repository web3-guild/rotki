from contextlib import ExitStack

import pytest
import requests

from rotkehlchen.accounting.structures import Balance
from rotkehlchen.assets.asset import EthereumToken
from rotkehlchen.chain.ethereum.yearn.vaults import YearnVaultEvent, YearnVaultHistory
from rotkehlchen.constants.misc import ONE
from rotkehlchen.fval import FVal
from rotkehlchen.tests.utils.api import (
    api_url_for,
    assert_ok_async_response,
    assert_proper_response_with_result,
    wait_for_async_task,
)
from rotkehlchen.tests.utils.rotkehlchen import setup_balances
from rotkehlchen.typing import Timestamp

TEST_ACC1 = '0x7780E86699e941254c8f4D9b7eB08FF7e96BBE10'

# Expected events as of writing of the test. USD values are all mocked.
EXPECTED_HISTORY = {
    'YALINK Vault': YearnVaultHistory(
        events=[YearnVaultEvent(
            event_type='deposit',
            block_number=10693331,
            timestamp=Timestamp(1597877037),
            from_asset=EthereumToken('aLINK'),
            from_value=Balance(amount=FVal('389.42925099069838547'), usd_value=ONE),
            to_asset=EthereumToken('yaLINK'),
            to_value=Balance(amount=FVal('378.670298739289527979'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0x14bbb454cfe3bfbef4e7ea2b03e7aac022048480b3d2f81ea8d191f0543848c4',
            log_index=102,
        ), YearnVaultEvent(
            event_type='deposit',
            block_number=10843734,
            timestamp=Timestamp(1599868806),
            from_asset=EthereumToken('aLINK'),
            from_value=Balance(amount=FVal('72.192501610488361536'), usd_value=ONE),
            to_asset=EthereumToken('yaLINK'),
            to_value=Balance(amount=FVal('69.121544688263989615'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0x01df266c24e3c810665dd92f49d304642594a7c737620b86a78ac3860a87284b',
            log_index=376,
        )],
        profit_loss=Balance(amount=FVal('3.782217772661052898'), usd_value=ONE),
    ),
    'YCRV Vault': YearnVaultHistory(
        events=[YearnVaultEvent(
            event_type='deposit',
            block_number=10712731,
            timestamp=Timestamp(1598134807),
            from_asset=EthereumToken('yDAI+yUSDC+yUSDT+yTUSD'),
            from_value=Balance(amount=FVal('8927.5036'), usd_value=ONE),
            to_asset=EthereumToken('yyDAI+yUSDC+yUSDT+yTUSD'),
            to_value=Balance(amount=FVal('8410.411009462516551526'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0xca33e56e1e529dacc9aa1261c8ba9230927329eb609fbe252e5bd3c2f5f3bcc9',
            log_index=157,
        ), YearnVaultEvent(
            event_type='deposit',
            block_number=10715002,
            timestamp=Timestamp(1598164906),
            from_asset=EthereumToken('yDAI+yUSDC+yUSDT+yTUSD'),
            from_value=Balance(amount=FVal('50000'), usd_value=ONE),
            to_asset=EthereumToken('yyDAI+yUSDC+yUSDT+yTUSD'),
            to_value=Balance(amount=FVal('47071.387341290952647901'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0xa14302d91234e4bbfa0c5cbae86ee3f5007e9214c276c418d8324d3a98e3c326',
            log_index=105,
        ), YearnVaultEvent(
            event_type='deposit',
            block_number=10715305,
            timestamp=Timestamp(1598168863),
            from_asset=EthereumToken('yDAI+yUSDC+yUSDT+yTUSD'),
            from_value=Balance(amount=FVal('10000'), usd_value=ONE),
            to_asset=EthereumToken('yyDAI+yUSDC+yUSDT+yTUSD'),
            to_value=Balance(amount=FVal('9413.460813390417962171'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0xa0d36513b367fb2e9d328dcf5853dff55d9adfc5de21aa9874607920e8cbdf66',
            log_index=214,
        ), YearnVaultEvent(
            event_type='deposit',
            block_number=10721861,
            timestamp=Timestamp(1598256310),
            from_asset=EthereumToken('yDAI+yUSDC+yUSDT+yTUSD'),
            from_value=Balance(amount=FVal('15000'), usd_value=ONE),
            to_asset=EthereumToken('yyDAI+yUSDC+yUSDT+yTUSD'),
            to_value=Balance(amount=FVal('14090.755698636925071707'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0x617be692777f0d35b50c6967f84d0d4519c0b8ae71b2bcff8b6fdeaae7aa0aa0',
            log_index=214,
        ), YearnVaultEvent(
            event_type='deposit',
            block_number=10728692,
            timestamp=Timestamp(1598346410),
            from_asset=EthereumToken('yDAI+yUSDC+yUSDT+yTUSD'),
            from_value=Balance(amount=FVal('15000'), usd_value=ONE),
            to_asset=EthereumToken('yyDAI+yUSDC+yUSDT+yTUSD'),
            to_value=Balance(amount=FVal('14059.293839329373676244'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0x55a09f0f7d71d6674057d6f2fb9bbe94da8691cc70085d3e063a9ef7993eb79d',
            log_index=283,
        ), YearnVaultEvent(
            event_type='deposit',
            block_number=10733933,
            timestamp=Timestamp(1598416438),
            from_asset=EthereumToken('yDAI+yUSDC+yUSDT+yTUSD'),
            from_value=Balance(amount=FVal('36813.0143'), usd_value=ONE),
            to_asset=EthereumToken('yyDAI+yUSDC+yUSDT+yTUSD'),
            to_value=Balance(amount=FVal('34450.215876302284829548'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0x77a84379b8a1a282fd068826b29493de6be8c9b556d6f0f42c973f9b137fafe3',
            log_index=95,
        ), YearnVaultEvent(
            event_type='deposit',
            block_number=10772504,
            timestamp=Timestamp(1598926271),
            from_asset=EthereumToken('yDAI+yUSDC+yUSDT+yTUSD'),
            from_value=Balance(amount=FVal('13232.3137'), usd_value=ONE),
            to_asset=EthereumToken('yyDAI+yUSDC+yUSDT+yTUSD'),
            to_value=Balance(amount=FVal('12266.333137131799971047'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0x30e56f20301609b8963fa6aebb40b2d0fceef150d2d543698bbe9ec7a7eaca77',
            log_index=191,
        ), YearnVaultEvent(
            event_type='withdraw',
            block_number=10801146,
            timestamp=Timestamp(1599305858),
            from_asset=EthereumToken('yyDAI+yUSDC+yUSDT+yTUSD'),
            from_value=Balance(amount=FVal('139761.8577'), usd_value=ONE),
            to_asset=EthereumToken('yDAI+yUSDC+yUSDT+yTUSD'),
            to_value=Balance(amount=FVal('151278.291743620093963985'), usd_value=ONE),
            realized_pnl=Balance(amount=FVal('2305.460143620093963985'), usd_value=ONE),
            tx_hash='0xf8523130b1dc01d5b2e2a2e5f7b1e99a8536b9a0640272f888ac2a031d87e664',
            log_index=121,
        ), YearnVaultEvent(
            event_type='deposit',
            block_number=10805545,
            timestamp=Timestamp(1599363450),
            from_asset=EthereumToken('yDAI+yUSDC+yUSDT+yTUSD'),
            from_value=Balance(amount=FVal('151297.1419'), usd_value=ONE),
            to_asset=EthereumToken('yyDAI+yUSDC+yUSDT+yTUSD'),
            to_value=Balance(amount=FVal('139131.40076027036894831'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0x728ee71ee35a2b59ed110259f1b8fff0dd363cbe23847dd9930bc3b6d42a2a91',
            log_index=179,
        ), YearnVaultEvent(
            event_type='withdraw',
            block_number=10821864,
            timestamp=Timestamp(1599579643),
            from_asset=EthereumToken('yyDAI+yUSDC+yUSDT+yTUSD'),
            from_value=Balance(amount=FVal('139131.4007'), usd_value=ONE),
            to_asset=EthereumToken('yDAI+yUSDC+yUSDT+yTUSD'),
            to_value=Balance(amount=FVal('151404.504263158140919021'), usd_value=ONE),
            realized_pnl=Balance(amount=FVal('107.362363158140919021'), usd_value=ONE),
            tx_hash='0x9a1c9fb76bce709ba23f91aedbb460e3933fd498a12bfcb70e45b6b4d45d8d7a',
            log_index=167,
        ), YearnVaultEvent(
            event_type='deposit',
            block_number=10841907,
            timestamp=Timestamp(1599845114),
            from_asset=EthereumToken('yDAI+yUSDC+yUSDT+yTUSD'),
            from_value=Balance(amount=FVal('181110.2983'), usd_value=ONE),
            to_asset=EthereumToken('yyDAI+yUSDC+yUSDT+yTUSD'),
            to_value=Balance(amount=FVal('165702.940997938854610949'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0x700e94727ce0441a8e1bd16229b15a993ad9855fae992b717f0ee71deed76d75',
            log_index=268,
        )],
        profit_loss=Balance(amount=FVal('2780.795047609987847081'), usd_value=ONE),
    ),
    'YSRENCURVE Vault': YearnVaultHistory(
        events=[YearnVaultEvent(
            event_type='deposit',
            block_number=10737355,
            timestamp=Timestamp(1598461466),
            from_asset=EthereumToken('crvRenWSBTC'),
            from_value=Balance(amount=FVal('19.555772781075598652'), usd_value=ONE),
            to_asset=EthereumToken('ycrvRenWSBTC'),
            to_value=Balance(amount=FVal('19.553175850297437291'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0xad467166dc9737638ad765cd04077a8c4e888295a0162fcda78f0ca90e41561b',
            log_index=283,
        ), YearnVaultEvent(
            event_type='deposit',
            block_number=10761011,
            timestamp=Timestamp(1598774763),
            from_asset=EthereumToken('crvRenWSBTC'),
            from_value=Balance(amount=FVal('4.211408913263015043'), usd_value=ONE),
            to_asset=EthereumToken('ycrvRenWSBTC'),
            to_value=Balance(amount=FVal('4.191779011114917404'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0x0ece646f93da461b71a186df089721ef34d97638d73820a593076bc0aa0af596',
            log_index=73,
        ), YearnVaultEvent(
            event_type='deposit',
            block_number=10765233,
            timestamp=Timestamp(1598830533),
            from_asset=EthereumToken('crvRenWSBTC'),
            from_value=Balance(amount=FVal('2.666602909966091212'), usd_value=ONE),
            to_asset=EthereumToken('ycrvRenWSBTC'),
            to_value=Balance(amount=FVal('2.651888972362284456'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0xed615a8339cc35bbbcf99f7f7fd99ac26ac495fdedba26c16dd414d572c52a32',
            log_index=214,
        ), YearnVaultEvent(
            event_type='deposit',
            block_number=10782416,
            timestamp=Timestamp(1599057411),
            from_asset=EthereumToken('crvRenWSBTC'),
            from_value=Balance(amount=FVal('4.937148173002619273'), usd_value=ONE),
            to_asset=EthereumToken('ycrvRenWSBTC'),
            to_value=Balance(amount=FVal('4.888306645341969126'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0x51e47d6e2018d678d28756bc8c8850781c1f9cdbda7eebc2cd1c5f8c3dba4938',
            log_index=119,
        ), YearnVaultEvent(
            event_type='deposit',
            block_number=10844220,
            timestamp=Timestamp(1599875238),
            from_asset=EthereumToken('crvRenWSBTC'),
            from_value=Balance(amount=FVal('4.553641005086531109'), usd_value=ONE),
            to_asset=EthereumToken('ycrvRenWSBTC'),
            to_value=Balance(amount=FVal('4.461256285325473627'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0x2b890ad5f020357dbc8548e7a540a755a26d0c3acebf2f410a6267eea6b69805',
            log_index=35,
        ), YearnVaultEvent(
            event_type='deposit',
            block_number=10848970,
            timestamp=Timestamp(1599937908),
            from_asset=EthereumToken('crvRenWSBTC'),
            from_value=Balance(amount=FVal('0.578779736043454719'), usd_value=ONE),
            to_asset=EthereumToken('ycrvRenWSBTC'),
            to_value=Balance(amount=FVal('0.566826458001674028'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0x33e58a0d2bbf3caaf3d313f11952833e70c1a4649de30d33b8e3163ef9d48432',
            log_index=195,
        )],
        profit_loss=Balance(amount=FVal('0.612373358448149140'), usd_value=ONE),
    ),
    'YUSDC Vault': YearnVaultHistory(
        events=[YearnVaultEvent(
            event_type='deposit',
            block_number=10568776,
            timestamp=Timestamp(1596217006),
            from_asset=EthereumToken('USDC'),
            from_value=Balance(amount=FVal('24999.3143'), usd_value=ONE),
            to_asset=EthereumToken('yUSDC'),
            to_value=Balance(amount=FVal('24866.402046'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0xf7578003128b72606ccba7d8ff387b795a3fabe91b1670ed3aef1c5c9804ba08',
            log_index=205,
        ), YearnVaultEvent(
            event_type='withdraw',
            block_number=10614066,
            timestamp=Timestamp(1596821226),
            from_asset=EthereumToken('yUSDC'),
            from_value=Balance(amount=FVal('24866.402'), usd_value=ONE),
            to_asset=EthereumToken('USDC'),
            to_value=Balance(amount=FVal('25073.024968'), usd_value=ONE),
            realized_pnl=Balance(amount=FVal('73.710668'), usd_value=ONE),
            tx_hash='0x35bd25ce0c5b36c1eb9b5b20ccff0797bf6583f3f14e5cfe9e13eb051b483f53',
            log_index=227,
        )],
        profit_loss=Balance(amount=FVal('73.710715'), usd_value=ONE),
    ),
    'YUSDT Vault': YearnVaultHistory(
        events=[YearnVaultEvent(
            event_type='deposit',
            block_number=10693416,
            timestamp=Timestamp(1597878032),
            from_asset=EthereumToken('USDT'),
            from_value=Balance(amount=FVal('7996.974556'), usd_value=ONE),
            to_asset=EthereumToken('yUSDT'),
            to_value=Balance(amount=FVal('7954.695816'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0x2100ce91e7c3f3a8af3b79d9e3640682ec68b119f1131e6087bf5907ee44c3d6',
            log_index=268,
        ), YearnVaultEvent(
            event_type='withdraw',
            block_number=10712693,
            timestamp=Timestamp(1598134237),
            from_asset=EthereumToken('yUSDT'),
            from_value=Balance(amount=FVal('7954.695816'), usd_value=ONE),
            to_asset=EthereumToken('USDT'),
            to_value=Balance(amount=FVal('7990.78438'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0xc2d61f739c666868804f8a744bb11b0950d2de6d2ed3835e9d9b65ac0d90a2ea',
            log_index=88,
        )],
        profit_loss=Balance(amount=FVal('-6.190176'), usd_value=ONE),
    ),
    'YYFI Vault': YearnVaultHistory(
        events=[YearnVaultEvent(
            event_type='deposit',
            block_number=10699221,
            timestamp=Timestamp(1597954699),
            from_asset=EthereumToken('YFI'),
            from_value=Balance(amount=FVal('5.06602125157175773'), usd_value=ONE),
            to_asset=EthereumToken('yYFI'),
            to_value=Balance(amount=FVal('5.064598986597546737'), usd_value=ONE),
            realized_pnl=None,
            tx_hash='0x883b5bcd7416b0818e416ac471fb55b7d25ff934b8c384a11505fd25802b776d',
            log_index=291,
        ), YearnVaultEvent(
            event_type='withdraw',
            block_number=10797550,
            timestamp=Timestamp(1599258162),
            from_asset=EthereumToken('yYFI'),
            from_value=Balance(amount=FVal('5.064598986597546737'), usd_value=ONE),
            to_asset=EthereumToken('YFI'),
            to_value=Balance(amount=FVal('5.072075376490965719'), usd_value=ONE),
            realized_pnl=Balance(amount=FVal('0.006054124919207989'), usd_value=ONE),
            tx_hash='0x9acb5f766c715f2afdc0f167b4c2858783a92c05ba91eae6876788b4c3c2862d',
            log_index=132,
        )],
        profit_loss=Balance(amount=FVal('0.006054124919207989'), usd_value=ONE),
    ),
}


def check_vault_history(name, expected_history, result_history):
    """Check that the expected vault history matches for the non-mocked parts
    and only for the events we care for (until this test was written).
    """
    assert name in result_history
    result = result_history[name]
    vault_history = expected_history[name]
    keys = ('event_type', 'block_number', 'timestamp', 'from_asset', 'to_asset', 'tx_hash', 'log_index')  # noqa: E501
    for idx, event in enumerate(vault_history.events):
        s = event.serialize()
        for key in keys:
            msg = f'Unexpected data for event with idx "{idx}" and key "{key}" of {name} vault'
            assert s[key] == result['events'][idx][key], msg
        assert FVal(s['from_value']['amount']) == FVal(result['events'][idx]['from_value']['amount'])  # noqa: E501
        assert FVal(s['to_value']['amount']) == FVal(result['events'][idx]['to_value']['amount'])  # noqa: E501
        if s['realized_pnl']:
            assert FVal(s['realized_pnl']['amount']) == FVal(result['events'][idx]['realized_pnl']['amount'])  # noqa: E501


@pytest.mark.parametrize('ethereum_accounts', [[TEST_ACC1]])
@pytest.mark.parametrize('ethereum_modules', [['yearn_vaults']])
@pytest.mark.parametrize('should_mock_current_price_queries', [True])
@pytest.mark.parametrize('should_mock_price_queries', [True])
@pytest.mark.parametrize('default_mock_price_value', [FVal(1)])
@pytest.mark.parametrize('start_with_valid_premium', [True])
def test_query_yearn_vault_history(rotkehlchen_api_server, ethereum_accounts):
    """Check querying the yearn vaults history endpoint works. Uses real data.
    """
    async_query = False
    rotki = rotkehlchen_api_server.rest_api.rotkehlchen
    setup = setup_balances(
        rotki,
        ethereum_accounts=ethereum_accounts,
        btc_accounts=None,
        original_queries=['zerion'],
    )
    with ExitStack() as stack:
        # patch ethereum/etherscan to not autodetect tokens
        setup.enter_ethereum_patches(stack)
        response = requests.get(api_url_for(
            rotkehlchen_api_server,
            "yearnvaultshistoryresource",
        ), json={'async_query': async_query})
        if async_query:
            task_id = assert_ok_async_response(response)
            outcome = wait_for_async_task(rotkehlchen_api_server, task_id)
            assert outcome['message'] == ''
            result = outcome['result']
        else:
            result = assert_proper_response_with_result(response)

    result = result[TEST_ACC1]
    check_vault_history('YALINK Vault', EXPECTED_HISTORY, result)
    check_vault_history('YCRV Vault', EXPECTED_HISTORY, result)
    check_vault_history('YSRENCURVE Vault', EXPECTED_HISTORY, result)
    check_vault_history('YUSDC Vault', EXPECTED_HISTORY, result)
    check_vault_history('YUSDT Vault', EXPECTED_HISTORY, result)
    check_vault_history('YYFI Vault', EXPECTED_HISTORY, result)
