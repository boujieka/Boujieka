import pytest

from verify_citations import normalize, value_in_quote


@pytest.mark.parametrize("value,quote,expected", [
    (0.06015, "a tariff of 6.015 cents/kWh", True),
    (1093, "USD 1 093/kW", True),
    (1093, "$1,093/kW", True),
    (38e6, "$38-million", True),
    (0.12, "12% in Africa", True),
    (54, "a 54-megawatt plant", True),
    (54, "a 154 MW plant", False),
    (0.0398, "3,98 centimes d'euro", True),
    (15.4, "30 MW/15.4 MWh", True),
    (1093, "1 0930 kW", False),
])
def test_value_in_quote(value, quote, expected):
    assert value_in_quote(value, normalize(quote)) is expected


def test_normalize_accents_and_quotes():
    assert normalize("Énergie  “solaire”") == "energie solaire"


def test_near_value_table_cells():
    from verify_citations import near_value
    doc = normalize("Highveld Solar   Infinity Power   Pele Green\n  240   420,74   90,00   Mpumalanga\n"
                    "  Consortium   Holding SA   Energy")
    quote = normalize("Highveld Solar Consortium Infinity Power Holding SA 240 420,74 Mpumalanga")
    assert near_value(420.74, quote, doc)
    assert not near_value(999, quote, doc)
