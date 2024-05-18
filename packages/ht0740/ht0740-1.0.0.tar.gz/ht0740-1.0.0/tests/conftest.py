import sys

import mock
import pytest
from i2cdevice import MockSMBus


@pytest.fixture(scope="function")
def smbus2():
    sys.modules["smbus2"] = mock.Mock()
    sys.modules["smbus2"].SMBus = MockSMBus
    yield MockSMBus
    del sys.modules["smbus2"]


@pytest.fixture(scope="function")
def ht0740():
    import ht0740
    yield ht0740
    del sys.modules["ht0740"]
