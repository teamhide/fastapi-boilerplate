import pytest

from core.helpers.cache.custom_key_maker import CustomKeyMaker

key_maker = CustomKeyMaker()


@pytest.mark.asyncio
async def test_make_no_args():
    # Given
    def test():
        pass

    # When
    sut = await key_maker.make(function=test, prefix="hide")

    # Then
    assert sut == "hide::tests.core.helpers.cache.test_custom_key_maker.test"


@pytest.mark.asyncio
async def test_make_with_args():
    # Given
    def test(a: int):
        pass

    # When
    sut = await key_maker.make(function=test, prefix="hide")

    # Then
    assert sut == "hide::tests.core.helpers.cache.test_custom_key_maker.test.a"
