"""Module for managing spaces."""

from lemon_markets.helpers.api_client import _ApiClient
from lemon_markets.account import Account

from enum import Enum
from dataclasses import dataclass


class SpaceType(Enum):
    """
    Type of the space.

    Attributes
    ----------
    STRATEGY
        Type is `strategy`
    APP
        Type is `app`

    """

    STRATEGY = 'strategy'
    APP = 'app'


@dataclass
class Space(_ApiClient):
    """
    Class representing a space.

    Raises
    ------
    ValueError
        If the space type is invalid

    """

    uuid: str = None
    name: str = None
    type: str = None
    _state: dict = None

    _account: Account = None

    @classmethod
    def _from_response(cls, account: Account, data: dict):
        try:
            type_ = SpaceType(data.get('type'))
        except (ValueError, KeyError):
            raise ValueError('Unexpected space type: %r' % data.get('type'))

        return cls(
            uuid=data.get('uuid'),
            name=data.get('name'),
            _state=data.get('state'),
            type=type_,
            _account=account
        )

    def update_values(self, data: dict):
        """
        Update values from response data.

        Parameters
        ----------
        data : dict
            Response data

        Raises
        ------
        ValueError
            Raised if the space type in data is invalid

        """
        try:
            type_ = SpaceType(data.get('type'))
        except (ValueError, KeyError):
            raise ValueError('Unexpected space type: %r' % data.get('type'))

        self.uuid = data.get('uuid')
        self.name = data.get('name')
        self._state = data.get('state')
        self.type = type_

    def __post_init__(self):            # noqa
        super().__init__(account=self._account)

    def _update_space_state(self):
        data = self._request(f"spaces/{self.uuid}/")
        self.update_values(data)

    @property
    def state(self) -> dict:
        # TODO is state of type dict?
        """
        Get the space of the state.

        Returns
        -------
        dict
            The space state

        """
        self._update_space_state()
        return self._state

    @property
    def balance(self) -> float:
        # TODO what is the type of balance (should be float?)
        """
        Get space balance.

        Returns
        -------
        str
            The balance

        """
        self._update_space_state()
        return float(self._state.get("balance"))

    @property
    def cash_to_invest(self) -> float:
        # TODO isnt this the same as balance?
        """
        Get cash to invest.

        Returns
        -------
        str
            Cash to invest

        """
        self._update_space_state()
        return float(self._state.get("cash_to_invest"))
