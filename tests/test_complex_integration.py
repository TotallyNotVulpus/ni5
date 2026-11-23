from src.models import ApartmentSettlement
from src.manager import Manager
from src.models import Parameters
from src.models import Bill


def test_apartment_costs_with_optional_parameters():
    manager = Manager(Parameters())
    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-03-15',
        settlement_year=2025,
        settlement_month=2,
        amount_pln=1250.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-03-15',
        settlement_year=2024,
        settlement_month=2,
        amount_pln=1150.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-02-02',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=222.0,
        type='electricity'
    ))

    costs = manager.get_apartment_costs('apartment-1', 2024, 1)
    assert costs is None

    costs = manager.get_apartment_costs('apart-polanka', 2024, 3)
    assert costs == 0.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1)
    assert costs == 222.0

    costs = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert costs == 910.0
    
    costs = manager.get_apartment_costs('apart-polanka', 2024)
    assert costs == 1372.0

    costs = manager.get_apartment_costs('apart-polanka')
    assert costs == 3532.0

def test_create_apartment_settlement_with_bills():
    manager = Manager(Parameters())
    manager.bills = [
        Bill(
            apartment="apart-polanka",
            date_due="2025-02-01",
            settlement_year=2025,
            settlement_month=1,
            amount_pln=760.0,
            type="rent",
        ),
        Bill(
            apartment="apart-polanka",
            date_due="2025-02-02",
            settlement_year=2025,
            settlement_month=1,
            amount_pln=150.0,
            type="electricity",
        ),
        Bill(
            apartment="apart-polanka",
            date_due="2025-03-01",
            settlement_year=2025,
            settlement_month=2,
            amount_pln=500.0,
            type="rent",
        ),
        Bill(
            apartment="other-apartment",
            date_due="2025-02-03",
            settlement_year=2025,
            settlement_month=1,
            amount_pln=999.0,
            type="rent",
        ),
    ]

    result = manager.create_apartment_settlement("apart-polanka", 2025, 1)

    assert isinstance(result, ApartmentSettlement)
    assert result.apartment == "apart-polanka"
    assert result.year == 2025
    assert result.month == 1
    assert result.total_rent_pln == 760.0
    assert result.total_bills_pln == 150.0
    assert result.total_due_pln == 910.0
    assert result.total_due_pln == result.total_rent_pln + result.total_bills_pln


def test_create_apartment_settlement_without_bills():
    manager = Manager(Parameters())
    manager.bills = []

    result = manager.create_apartment_settlement("apart-polanka", 2025, 1)

    assert isinstance(result, ApartmentSettlement)
    assert result.apartment == "apart-polanka"
    assert result.year == 2025
    assert result.month == 1
    assert result.total_rent_pln == 0.0
    assert result.total_bills_pln == 0.0
    assert result.total_due_pln == 0.0