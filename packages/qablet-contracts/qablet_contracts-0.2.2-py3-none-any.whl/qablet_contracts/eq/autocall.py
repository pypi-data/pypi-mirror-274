"""
This module contains examples of autocallable notes.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List

import numpy as np
import pandas as pd

from qablet_contracts.ir.dcf import dcf_30_360 as dcf
from qablet_contracts.timetable import EventsMixin


@dataclass
class DiscountCert(EventsMixin):
    """An **Autocallable Discount Certificate** is called if the asset price is above the barrier level
    on any of the barrier observation dates. If called, the note pays the principal and the coupon accreted
    till the call date. Otherwise, at maturity, if the asset is above strike, it pays the principal and the
    coupon at maturity. If the asset is below strike, the principal payment is scaled down proportionately
    with the asset price.

    Args:
        ccy: the currency of the option.
        asset_name: the name of the underlying asset.
        initial_spot: the initial spot price of the asset.
        strike: downside participation below this strike.
        maturity: the maturity of the option in years.
        barrier: the note is called above this barrier level.
        barrier_dates: the barrier observation points.
        cpn_rate: the coupon rate.
        notional: the notional amount.
        track: an optional identifier for the contract.

    Examples:
        >>> start = datetime(2024, 3, 31)
        >>> maturity = datetime(2024, 9, 30)
        >>> barrier_dates = pd.date_range(start, maturity, freq="ME", inclusive="right")
        >>> tt = DiscountCert(
            "USD", "AAPL", 100, 80, start, maturity, 102, barrier_dates, 0.092
        ).timetable()
        >>> print(tt["events"].to_pandas())
          track                      time    op    quantity    unit
        0       2024-04-30 00:00:00+00:00  CALL  100.769613     USD
        1       2024-05-31 00:00:00+00:00  CALL  101.545149     USD
        2       2024-06-30 00:00:00+00:00  CALL  102.326654     USD
        3       2024-07-31 00:00:00+00:00  CALL  103.114173     USD
        4       2024-08-31 00:00:00+00:00  CALL  103.907753     USD
        5       2024-09-30 00:00:00+00:00  CALL  104.707441     USD
        6       2024-09-30 00:00:00+00:00     +    1.000000  PAYOFF
    """

    ccy: str
    asset_name: str
    initial_spot: float
    strike: float
    accrual_start: datetime
    maturity: datetime
    barrier: float
    barrier_dates: List[datetime]
    cpn_rate: float
    notional: float = 100.0
    track: str = ""

    def events(self):
        events = []
        # Autocall events
        for barrier_date in self.barrier_dates:
            # daycount_fraction
            frac = dcf(barrier_date, self.accrual_start)
            events.append(
                {
                    "track": self.track,
                    "time": barrier_date,
                    "op": "CALL",
                    "quantity": self.notional * np.exp(frac * self.cpn_rate),
                    "unit": self.ccy,
                }
            )

        # payoff at maturity
        events.append(
            {
                "track": "",
                "time": self.maturity,
                "op": "+",
                "quantity": 1.0,
                "unit": "PAYOFF",
            }
        )
        return events

    def fixed_payoff(self):
        return self.notional * np.exp(
            dcf(self.maturity, self.accrual_start) * self.cpn_rate
        )

    def expressions(self):
        # Define the autocall condition
        def ko_fn(inputs):
            [S] = inputs
            return [S > (self.barrier * self.initial_spot / self.notional)]

        call = {
            "type": "phrase",
            "inp": [self.asset_name],
            "fn": ko_fn,
        }

        # Define the final payoff
        def payoff_fn(inputs):
            [s] = inputs
            eq_pay = s * (self.notional / self.initial_spot)
            return [
                np.where(eq_pay < self.strike, eq_pay, self.fixed_payoff())
            ]

        payoff = {
            "type": "phrase",
            "inp": [self.asset_name],
            "fn": payoff_fn,
        }

        return {"PAYOFF": payoff, "CALL": call}


@dataclass
class ReverseCB(DiscountCert):
    """An **Autocallable Reverse Convertible** is called if the asset price is above the barrier level
    on any of the barrier observation dates. Otherwise, at maturity, if the asset is above strike, it pays the principal and the
    coupon at maturity. If the asset is below strike, the principal payment is scaled down proportionately
    with the asset price. The note pays periodic coupons until called or matured.

    Args:
        ccy: the currency of the option.
        asset_name: the name of the underlying asset.
        initial_spot: the initial spot price of the asset.
        strike: downside participation below this strike.
        maturity: the maturity of the option in years.
        barrier: the note is called above this barrier level.
        barrier_dates: the barrier observation points.
        cpn_rate: the coupon rate.
        notional: the notional amount.
        track: an optional identifier for the contract.

    Examples:
        >>> start = datetime(2024, 3, 31)
        >>> maturity = datetime(2024, 9, 30)
        >>> barrier_dates = pd.date_range(start, maturity, freq="ME", inclusive="right")
        >>> tt = ReverseCB(
            "USD", "AAPL", 100, 80, start, maturity, 102, barrier_dates, 0.10
        ).timetable()
        >>> print(tt["events"].to_pandas())
           track                      time    op    quantity    unit
        0        2024-04-30 00:00:00+00:00     +    0.833333     USD
        1        2024-04-30 00:00:00+00:00  CALL  100.000000     USD
        2        2024-05-31 00:00:00+00:00     +    0.833333     USD
        3        2024-05-31 00:00:00+00:00  CALL  100.000000     USD
        4        2024-06-30 00:00:00+00:00     +    0.833333     USD
        5        2024-06-30 00:00:00+00:00  CALL  100.000000     USD
        6        2024-07-31 00:00:00+00:00     +    0.833333     USD
        7        2024-07-31 00:00:00+00:00  CALL  100.000000     USD
        8        2024-08-31 00:00:00+00:00     +    0.833333     USD
        9        2024-08-31 00:00:00+00:00  CALL  100.000000     USD
        10       2024-09-30 00:00:00+00:00     +    0.833333     USD
        11       2024-09-30 00:00:00+00:00  CALL  100.000000     USD
        12       2024-09-30 00:00:00+00:00     +    1.000000  PAYOFF
    """

    def events(self):
        events = []
        cpn_start_dates = [self.accrual_start] + list(self.barrier_dates[:-1])
        # Autocall events
        for start, end in zip(cpn_start_dates, self.barrier_dates):
            # daycount_fraction
            frac = dcf(end, start)
            events.append(
                {
                    "track": self.track,
                    "time": end,
                    "op": "+",
                    "quantity": self.notional * frac * self.cpn_rate,
                    "unit": self.ccy,
                }
            )
            events.append(
                {
                    "track": self.track,
                    "time": end,
                    "op": "CALL",
                    "quantity": self.notional,
                    "unit": self.ccy,
                }
            )

        # payoff at maturity
        events.append(
            {
                "track": "",
                "time": self.maturity,
                "op": "+",
                "quantity": 1.0,
                "unit": "PAYOFF",
            }
        )
        return events

    def fixed_payoff(self):
        return self.notional


if __name__ == "__main__":
    # Create the autocallable contract
    start = datetime(2024, 3, 31)
    maturity = datetime(2024, 9, 30)
    barrier_dates = pd.date_range(
        start, maturity, freq="ME", inclusive="right"
    )
    timetable = ReverseCB(
        "USD", "AAPL", 100, 80, start, maturity, 102, barrier_dates, 0.10
    ).timetable()
    print(timetable["events"].to_pandas())
