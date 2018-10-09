import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from parkingd import ParkingDaemon
from parking_config import ParkingConfig


def test_parkingd():
    config_text = ParkingConfig.slurp_config_file(config.parking_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'0000095c12d41a58c6f5fc729487df423d95dfc63ec02096192a143bd57acc44'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'0000095c12d41a58c6f5fc729487df423d95dfc63ec02096192a143bd57acc44'

    creds = ParkingConfig.get_rpc_creds(config_text, network)
    parkingd = ParkingDaemon(**creds)
    assert parkingd.rpc_command is not None

    assert hasattr(parkingd, 'rpc_connection')

    # Parking testnet block 0 hash == 0000095c12d41a58c6f5fc729487df423d95dfc63ec02096192a143bd57acc44
    # test commands without arguments
    info = parkingd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert parkingd.rpc_command('getblockhash', 0) == genesis_hash
