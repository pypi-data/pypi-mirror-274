# pylint: disable=C0115
# pylint: disable=C0116
# flake8: noqa

import os
from unittest.mock import Mock
import hashlib
import pytest

from ..api_type import TProfile, TUserEssentials, TUserSettings
from ..base_client import user_name, get_sha_256, full_name, parse_jwt, BaseAPIClient

API_HOST = os.getenv("NOVUM_API_URL", "https://localhost")


class TestBaseAPIClient:
    # auxiliar functions
    @pytest.fixture
    def user_sample_mage(self):
        """Fixture: sample of user."""
        user_sample = TUserEssentials(
            jwt="SuperSecret123!",
            refresh_token="MagicToken123",
            auth0_id="EnchantedWizard123",
            meta_data={"user_type": "MysticalBeing"},
            roles=["sorcerer", "enchanter"],
            scope="arcane_magic",
            stats=None,
            permissions=["granted", "enchanted"],
            profile=TProfile(
                name="Gandalf the Grey",
                first_name="Gandalf",
                last_name="Grey",
                given_name="The Enchanter",
                email="wizard@fantasyrealm.com",
                family_name="Grey",
                email_verified=True,
                picture="magical_staff.jpg",
            ),
            settings=TUserSettings(ServiceCenterSettings=None),
        )
        return user_sample

    def test_get_sha_256(self):
        """Check sha_256."""
        assert get_sha_256("hello world") == hashlib.sha256(b"hello world").hexdigest()
        assert get_sha_256("test") == hashlib.sha256(b"test").hexdigest()

    def test_user_name(self, user_sample_mage):
        """Check user name fetch."""
        result = user_name(user_sample_mage)
        expected_name = "Gandalf the Grey"
        assert result == expected_name

    def test_full_name(self, user_sample_mage):
        """Check full name check."""
        result = full_name(user_sample_mage)
        expected_result = "Gandalf Grey"
        assert result == expected_result

    def test_parse_jwt(self):
        """Check jwt."""
        sample_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im9Ma1Ridm93cnFndXdoN3lPaUttTCJ9.eyJodHRwczovL25vdnVtLWJhdHRlcmllcy5jb20vcm9sZXMiOlsidXNlciIsImludm9pY2VDcmVhdG9yIiwibm92dW1FeHBlcnQiXSwiaHR0cHM6Ly9ub3Z1bS1iYXR0ZXJpZXMuY29tL3NldHRpbmdzIjp7ImludmVydEF4aXMiOnRydWUsInNlcnZpY2VDZW50ZXIiOnsic2hvd0FkdmFuY2VkT3B0aW9ucyI6dHJ1ZSwiaW52ZXJ0QXhpcyI6dHJ1ZSwiZmF2b3JpdGVCYXR0ZXJpZXNJZHMiOlsiOW94SHZjNnlOWld1VzNzRWsiLCIyRUdFTjd1TU40YWg4ckRGWiIsIkRUQUhIRFR1SkJEQ3ZRRlNKIiwiOVJBU0VIZHZxRW9odlBFU1oiLCJkenBEd3NoUEFHc2N5NkJHaCIsIkFjY3lxSGdvR25IU0F3ZTlHIiwiczdNU1g0ZjNIcWpDcHZ1TEoiLCI1YzdlYkJTekNXNFJuckYzNCIsIkhQZ0RLVFRUSjNEUUhGZ0FEIl0sImJhdHRlcnlUYWJsZUNvbHVtbnMiOlsibmFtZSIsInN0YXRlLnN0YXRlX29mX2NoYXJnZS52YWx1ZSIsInN0YXRlLnN0YXRlX29mX2hlYWx0aC52YWx1ZSIsIm1ldHJpY3Muc3RhdGVfb2ZfaGVhbHRoIiwiaW50ZXJuYWxfY2FwYWNpdHlfY291bnQiLCJpbnRlcm5hbF9kYXRhc2V0X2NvdW50IiwiY3JlYXRvcl9pZCIsImxpZmV0aW1lX2luZGljYXRvciIsImludGVybmFsX2FjdGlvbnMiXSwiZGFzaGJvYXJkVGFibGVDb2x1bW5zIjpbIm5hbWUiLCJiYXR0ZXJ5X3R5cGUubmFtZSIsInN0YXRlLnN0YXRlX29mX2NoYXJnZS52YWx1ZSIsInN0YXRlLnN0YXRlX29mX2hlYWx0aC52YWx1ZSIsImxpZmV0aW1lX2luZGljYXRvciIsImludGVybmFsX2FjdGlvbnMiXSwiZWlzRGF0YXNldFRhYmxlQ29sdW1ucyI6WyJpZCIsIm1ldGEuYmF0dGVyeS5uYW1lIiwiYW5hbHlzaXMuc3RhdGVfb2ZfY2hhcmdlIiwiYW5hbHlzaXMuc3RhdGVfb2ZfaGVhbHRoIiwiaW50ZXJuYWxfYWN0aW9ucyIsImFuYWx5c2lzLmdyYWRlIiwiY3JlYXRvcl9pZCIsImNvbnRleHRfaWQiLCJjcmVhdGVkX2F0Il0sImNhcGFjaXR5TWVhc3VyZW1lbnRUYWJsZUNvbHVtbnMiOlsiaWQiLCJiYXR0ZXJ5Lm5hbWUiLCJzdGF0ZV9vZl9oZWFsdGgiLCJjcmVhdGVkX2F0IiwiaW50ZXJuYWxfYWN0aW9ucyIsImdyYWRlIiwiY3JlYXRvcl9pZCIsImNvbnRleHRfaWQiLCJzdGFydF90aW1lIiwiZW5kX3RpbWUiXX19LCJnaXZlbl9uYW1lIjoiTGVvbmFyZG8iLCJmYW1pbHlfbmFtZSI6IkJpeiIsIm5pY2tuYW1lIjoibC5iaXoiLCJuYW1lIjoiTGVvIEJpeiIsInBpY3R1cmUiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci8yZTRiYTE2Y2U0MzY4NTE0NDVmMzcxNDM1M2QyNzAwNz9zPTQ4MCZyPXBnJmQ9aHR0cHMlM0ElMkYlMkZjZG4uYXV0aDAuY29tJTJGYXZhdGFycyUyRmwucG5nIiwidXBkYXRlZF9hdCI6IjIwMjMtMTEtMDFUMTE6NDc6NTYuMjE3WiIsImVtYWlsIjoibC5iaXpAbm92dW0tZW5naW5lZXJpbmcuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOi8vZGV2LW5vdnVtLmV1LmF1dGgwLmNvbS8iLCJhdWQiOiJwN0pSSEI3bVlvOGt5RXVlVWt2VnhTWFo5YllXSWZSbCIsImlhdCI6MTY5ODg0Nzk2MywiZXhwIjoxNjk4ODgzOTYzLCJzdWIiOiJhdXRoMHw2MjMzM2RiNGJjNzgzNDAwNjhjMzdjOTEiLCJzaWQiOiIwOHVGV09oX3V2N3J2Z0p3dy1HMVhMQ0F1QTNsUUFjQyIsIm5vbmNlIjoiV0hvd1NXTnlORmhpUkdGdmEwWnViSFJtUTBGUVdGcEdaRXRRTlM1bU1WVnVUa2hHZVMwdVlqVXRRdz09In0.YtOCMsRWNQIbt_XxKdyLr7Y4IP60FQea3T5KKtLJ2V753A91DbTYYGxvCdwsrGtyoXge1_8Yp7_6_bAbGKkr5K1RLSGzbUEkgqe9KvbBSI8uDvDM8hPOPGAUYq5-XyL4j2I36NWQqsT1i32d6ozf_fJqXHurfvXASfXHK7Wp6moTAV7HtqvYhcwfC9ZbV9hqplldLCkxYPe2lkzky0H-EfJqLh1X-g8hLCnn_9TW2d1LFIxHbciIaYaAqhjtU01KveDKyu3imi4m5z2pxa3hW6T_nYKB1utXUHacvMX89zMuGGSOZrNa9Ww9zhmzVgA4NG-SFCKQFNMThGkMdPdKqA"
        result = parse_jwt(sample_token)
        assert result is not None
        assert "user" in result["https://novum-batteries.com/roles"]

    # Base API tests

    @pytest.fixture
    def base_api_client(self):
        """Fixture: Base API Client."""
        base_api = BaseAPIClient()
        return base_api

    def test_from_window_location(self):
        """# Check from_window_location class method."""
        origin = "https://novum-batteries.com"
        client = BaseAPIClient.from_window_location(origin)
        assert client.host == origin

    def test_clear_user(self, base_api_client):
        """Check clear user info method."""
        base_api_client.user = self.user_sample_mage
        base_api_client._clear_user()
        assert base_api_client.user is None

    def test_remove_relogin_timer_handle(self, base_api_client):
        """Check _remove_relogin_timer_handle method."""
        base_api_client._relogin_timer_handle = 3
        base_api_client._remove_relogin_timer_handle()
        assert base_api_client._relogin_timer_handle is None

    def test_get_expire_time_from_token_in_unix_time_millis(self, base_api_client):
        """Check  _get_expire_time_from_token_in_unix_time_millis method."""
        sample_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im9Ma1Ridm93cnFndXdoN3lPaUttTCJ9.eyJodHRwczovL25vdnVtLWJhdHRlcmllcy5jb20vcm9sZXMiOlsidXNlciIsImludm9pY2VDcmVhdG9yIiwibm92dW1FeHBlcnQiXSwiaHR0cHM6Ly9ub3Z1bS1iYXR0ZXJpZXMuY29tL3NldHRpbmdzIjp7ImludmVydEF4aXMiOnRydWUsInNlcnZpY2VDZW50ZXIiOnsic2hvd0FkdmFuY2VkT3B0aW9ucyI6dHJ1ZSwiaW52ZXJ0QXhpcyI6dHJ1ZSwiZmF2b3JpdGVCYXR0ZXJpZXNJZHMiOlsiOW94SHZjNnlOWld1VzNzRWsiLCIyRUdFTjd1TU40YWg4ckRGWiIsIkRUQUhIRFR1SkJEQ3ZRRlNKIiwiOVJBU0VIZHZxRW9odlBFU1oiLCJkenBEd3NoUEFHc2N5NkJHaCIsIkFjY3lxSGdvR25IU0F3ZTlHIiwiczdNU1g0ZjNIcWpDcHZ1TEoiLCI1YzdlYkJTekNXNFJuckYzNCIsIkhQZ0RLVFRUSjNEUUhGZ0FEIl0sImJhdHRlcnlUYWJsZUNvbHVtbnMiOlsibmFtZSIsInN0YXRlLnN0YXRlX29mX2NoYXJnZS52YWx1ZSIsInN0YXRlLnN0YXRlX29mX2hlYWx0aC52YWx1ZSIsIm1ldHJpY3Muc3RhdGVfb2ZfaGVhbHRoIiwiaW50ZXJuYWxfY2FwYWNpdHlfY291bnQiLCJpbnRlcm5hbF9kYXRhc2V0X2NvdW50IiwiY3JlYXRvcl9pZCIsImxpZmV0aW1lX2luZGljYXRvciIsImludGVybmFsX2FjdGlvbnMiXSwiZGFzaGJvYXJkVGFibGVDb2x1bW5zIjpbIm5hbWUiLCJiYXR0ZXJ5X3R5cGUubmFtZSIsInN0YXRlLnN0YXRlX29mX2NoYXJnZS52YWx1ZSIsInN0YXRlLnN0YXRlX29mX2hlYWx0aC52YWx1ZSIsImxpZmV0aW1lX2luZGljYXRvciIsImludGVybmFsX2FjdGlvbnMiXSwiZWlzRGF0YXNldFRhYmxlQ29sdW1ucyI6WyJpZCIsIm1ldGEuYmF0dGVyeS5uYW1lIiwiYW5hbHlzaXMuc3RhdGVfb2ZfY2hhcmdlIiwiYW5hbHlzaXMuc3RhdGVfb2ZfaGVhbHRoIiwiaW50ZXJuYWxfYWN0aW9ucyIsImFuYWx5c2lzLmdyYWRlIiwiY3JlYXRvcl9pZCIsImNvbnRleHRfaWQiLCJjcmVhdGVkX2F0Il0sImNhcGFjaXR5TWVhc3VyZW1lbnRUYWJsZUNvbHVtbnMiOlsiaWQiLCJiYXR0ZXJ5Lm5hbWUiLCJzdGF0ZV9vZl9oZWFsdGgiLCJjcmVhdGVkX2F0IiwiaW50ZXJuYWxfYWN0aW9ucyIsImdyYWRlIiwiY3JlYXRvcl9pZCIsImNvbnRleHRfaWQiLCJzdGFydF90aW1lIiwiZW5kX3RpbWUiXX19LCJnaXZlbl9uYW1lIjoiTGVvbmFyZG8iLCJmYW1pbHlfbmFtZSI6IkJpeiIsIm5pY2tuYW1lIjoibC5iaXoiLCJuYW1lIjoiTGVvIEJpeiIsInBpY3R1cmUiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci8yZTRiYTE2Y2U0MzY4NTE0NDVmMzcxNDM1M2QyNzAwNz9zPTQ4MCZyPXBnJmQ9aHR0cHMlM0ElMkYlMkZjZG4uYXV0aDAuY29tJTJGYXZhdGFycyUyRmwucG5nIiwidXBkYXRlZF9hdCI6IjIwMjMtMTEtMDFUMTE6NDc6NTYuMjE3WiIsImVtYWlsIjoibC5iaXpAbm92dW0tZW5naW5lZXJpbmcuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOi8vZGV2LW5vdnVtLmV1LmF1dGgwLmNvbS8iLCJhdWQiOiJwN0pSSEI3bVlvOGt5RXVlVWt2VnhTWFo5YllXSWZSbCIsImlhdCI6MTY5ODg0Nzk2MywiZXhwIjoxNjk4ODgzOTYzLCJzdWIiOiJhdXRoMHw2MjMzM2RiNGJjNzgzNDAwNjhjMzdjOTEiLCJzaWQiOiIwOHVGV09oX3V2N3J2Z0p3dy1HMVhMQ0F1QTNsUUFjQyIsIm5vbmNlIjoiV0hvd1NXTnlORmhpUkdGdmEwWnViSFJtUTBGUVdGcEdaRXRRTlM1bU1WVnVUa2hHZVMwdVlqVXRRdz09In0.YtOCMsRWNQIbt_XxKdyLr7Y4IP60FQea3T5KKtLJ2V753A91DbTYYGxvCdwsrGtyoXge1_8Yp7_6_bAbGKkr5K1RLSGzbUEkgqe9KvbBSI8uDvDM8hPOPGAUYq5-XyL4j2I36NWQqsT1i32d6ozf_fJqXHurfvXASfXHK7Wp6moTAV7HtqvYhcwfC9ZbV9hqplldLCkxYPe2lkzky0H-EfJqLh1X-g8hLCnn_9TW2d1LFIxHbciIaYaAqhjtU01KveDKyu3imi4m5z2pxa3hW6T_nYKB1utXUHacvMX89zMuGGSOZrNa9Ww9zhmzVgA4NG-SFCKQFNMThGkMdPdKqA"
        result = base_api_client._get_expire_time_from_token_in_unix_time_millis(
            sample_token
        )
        assert isinstance(result, str)

    # TODO: def test_install_token_refresh_procedure(self, user_mage):

    @pytest.mark.parametrize(
        "ok_value, status_code, expected_error",
        [
            (True, 200, None),
            (
                False,
                400,
                f"Failed to load resource {API_HOST} -> Status:400",
            ),
        ],
    )
    def test_fetch_by_URL(self, base_api_client, ok_value, status_code, expected_error):
        """Mock the _get_json method to return a response."""
        response = {"ok": ok_value, "status": status_code}
        base_api_client._get_json = Mock(return_value=response)

        url = API_HOST
        options = {}

        if expected_error:
            with pytest.raises(ValueError) as excinfo:
                base_api_client._fetch_by_URL(url, options)
            assert str(excinfo.value) == expected_error
        else:
            result = base_api_client._fetch_by_URL(url, options)
            assert result == response

    @pytest.mark.parametrize(
        "ok_value, status_code, expected_error",
        [
            (True, 200, None),
            (
                False,
                400,
                f"('Failed to load resource {API_HOST} -> Status:400'",
            ),
        ],
    )
    def test_post_by_URL(self, base_api_client, ok_value, status_code, expected_error):
        """Check the _post_json method to return a response."""
        response = {"ok": ok_value, "status": status_code}
        base_api_client._post_json = Mock(return_value=response)

        url = API_HOST
        options = {}

        if expected_error:
            with pytest.raises(ValueError) as excinfo:
                base_api_client._post_by_URL(url, options)
            assert str(excinfo.value) == expected_error + ", " + str(response) + ")"
        else:
            result = base_api_client._post_by_URL(url, options)
            assert result == response
