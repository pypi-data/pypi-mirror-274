import json

import requests

from .data_classes import AccountClass, account_class_from_dict


class Account:
    def __init__(self, trade_url: str, headers: object) -> None:
        """Initialize Account class

        Parameters:
        ___________
        trade_url: str
                Alpaca Trade API URL required

        headers: object
                API request headers required

        Raises:
        _______
        ValueError: If trade URL is not provided

        ValueError: If headers are not provided
        """  # noqa

        self.trade_url = trade_url
        self.headers = headers

    ########################################################
    # \\\\\\\\\\\\\  Get Account Information ///////////////#
    ########################################################
    def get(self) -> AccountClass:
        """Get account information from Alpaca API

        Returns:
        ________
        AccountClass: Account information as an AccountClass object

        Raises:
        _______
        Exception: If the response is not successful

        Example:
        ________
        >>> from py_alpaca_api import PyAlpacaApi
            api = PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
            account = api.account.get()
            print(account)

        AccountClass(
            account_blocked=False,
            account_number="PA2ZVZ6QYJ6U",
            buying_power=100000,
            cash=100000,
            created_at="2021-07-08T18:18:08.182Z",
            currency="USD",
            daytrade_count=0,
            daytrading_buying_power=100000,
            equity=100000,
            id="f3b5d9e2-0e4e-4f0f-8d3f-0f0e7b7e4e6e",
            initial_margin=0,
            last_equity=100000,
            last_maintenance_margin=0,
            long_market_value=0,
            maintenance_margin=0,
            multiplier=4,
            pattern_day_trader=False,
            portfolio_value=100000,
            regt_buying_power=200000,
            short_market_value=0,
            shorting_enabled=True,
            sma=0,
            status="ACTIVE",
            trade_suspended_by_user=False,
            trading_blocked=False,
            transfers_blocked=False,
            updated_at="2021-07-08T18:18:08.182Z",
            withdrawable_amount=100000
        )
        """  # noqa

        # Alpaca API URL for account information
        url = f"{self.trade_url}/account"
        # Get request to Alpaca API for account information
        response = requests.get(url, headers=self.headers)
        # Check if response is successful
        if response.status_code == 200:
            # Convert JSON response to dictionary
            res = json.loads(response.text)
            # Return account information as an AccountClass object
            return account_class_from_dict(res)
        # If response is not successful, raise an exception
        else:
            raise Exception(f"Failed to get account information. Response: {response.text}")
