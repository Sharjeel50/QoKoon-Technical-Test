import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    with TestClient(app, headers={"X-User-Fingerprint": "Test"}) as client:
        yield client


def test_timefame_monthly(client: TestClient):
    response = client.get("/cash-flow/calculate?start_date=2019-04-30&timeframe=monthly")
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "non_cash_charges": 9155.77506092397,
            "changes_in_working_capital": 0,
            "cash_flow_from_operations": 30816.336352061688
        }
    }


def test_timefame_quaterly(client: TestClient):
    response = client.get("/cash-flow/calculate?start_date=2019-04-30&timeframe=quarterly")
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "non_cash_charges": 26656.25388225018,
            "changes_in_working_capital": 3558.1986318838153,
            "cash_flow_from_operations": 101409.4193951872
        }
    }


def test_timefame_yearly(client: TestClient):
    response = client.get("/cash-flow/calculate?start_date=2020-03-03&timeframe=yearly")
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "non_cash_charges": 57216.233703513855,
            "changes_in_working_capital": 45160.19778989973,
            "cash_flow_from_operations": 342712.9250877804
        }
    }


def test_timefame_quaterly_with_working_data(client: TestClient):
    response = client.get("/cash-flow/calculate?start_date=2020-03-03&timeframe=quarterly&include_working_data=true")
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "non_cash_charges": 13959.985703967315,
            "changes_in_working_capital": -106.74491788584055,
            "cash_flow_from_operations": 72115.26901693898,
            "working_data": {
                "pnl_original_data": {
                    "sales": {
                        "0": 140718.32972259997,
                        "1": 106916.6995455138,
                        "2": 169742.87731445636
                    },
                    "cost_of_sales": {
                        "0": 100988.3981468569,
                        "1": 81920.61132655852,
                        "2": 123198.76397061642
                    },
                    "net_income": {
                        "0": 20509.49089945072,
                        "1": 14603.453615456649,
                        "2": 23149.08371595012
                    },
                    "depreciation": {
                        "0": 4698.842890780779,
                        "1": 5050.345855298864,
                        "2": 4210.796957887674
                    },
                    "id": {
                        "0": 14,
                        "1": 15,
                        "2": 16
                    },
                    "date": {
                        "0": "2020-03-31",
                        "1": "2020-04-30",
                        "2": "2020-05-31"
                    }
                },
                "working_capital_original_data": {
                    "inventory": {
                        "0": 23210.68142787597,
                        "1": 42555.20567682544,
                        "2": 15615.358311973876
                    },
                    "accounts_receivable": {
                        "0": 9572.93101965891,
                        "1": 18542.82288222848,
                        "2": 16857.60541562315
                    },
                    "accounts_payable": {
                        "0": 19302.8650405072,
                        "1": 16161.02473314525,
                        "2": 19098.961238455187
                    },
                    "id": {
                        "0": 14,
                        "1": 15,
                        "2": 16
                    },
                    "date": {
                        "0": "2020-03-31",
                        "1": "2020-04-30",
                        "2": "2020-05-31"
                    }
                }
            }
        }
    }


def test_timefame_yearly_with_working_data(client: TestClient):
    response = client.get("/cash-flow/calculate?start_date=2020-03-03&timeframe=yearly&include_working_data=true")
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "non_cash_charges": 57216.233703513855,
            "changes_in_working_capital": 45160.19778989973,
            "cash_flow_from_operations": 342712.9250877804,
            "working_data": {
                "pnl_original_data": {
                    "sales": {
                        "0": 140718.32972259997,
                        "1": 106916.6995455138,
                        "2": 169742.87731445636,
                        "3": 145354.26826780688,
                        "4": 172205.5599470348,
                        "5": 186638.2325928629,
                        "6": 197552.15050028855,
                        "7": 185580.3342392611,
                        "8": 101171.4084185002,
                        "9": 135997.8064478364,
                        "10": 172999.0562424058,
                        "11": 117162.96772614404
                    },
                    "cost_of_sales": {
                        "0": 100988.3981468569,
                        "1": 81920.61132655852,
                        "2": 123198.76397061642,
                        "3": 112581.26045587978,
                        "4": 112744.42782311644,
                        "5": 141772.14967727193,
                        "6": 125865.84630173168,
                        "7": 146712.07937580324,
                        "8": 74613.6764897726,
                        "9": 87460.39814072434,
                        "10": 136578.2773587224,
                        "11": 87423.62769590183
                    },
                    "net_income": {
                        "0": 20509.49089945072,
                        "1": 14603.453615456649,
                        "2": 23149.08371595012,
                        "3": 16642.43469310241,
                        "4": 22194.79473976151,
                        "5": 25935.05687449443,
                        "6": 27613.744461180304,
                        "7": 21754.937327045704,
                        "8": 14016.654966525106,
                        "9": 18603.778431993745,
                        "10": 18523.930047478996,
                        "11": 16789.133821927146
                    },
                    "depreciation": {
                        "0": 4698.842890780779,
                        "1": 5050.345855298864,
                        "2": 4210.796957887674,
                        "3": 5789.972929084934,
                        "4": 5718.5871813522635,
                        "5": 4161.025313513788,
                        "6": 8078.676769114624,
                        "7": 5088.976997085224,
                        "8": 2143.666914808145,
                        "9": 2964.524921086633,
                        "10": 3776.9770029247466,
                        "11": 5533.83997057619
                    },
                    "id": {
                        "0": 14,
                        "1": 15,
                        "2": 16,
                        "3": 17,
                        "4": 18,
                        "5": 19,
                        "6": 20,
                        "7": 21,
                        "8": 22,
                        "9": 23,
                        "10": 24,
                        "11": 25
                    },
                    "date": {
                        "0": "2020-03-31",
                        "1": "2020-04-30",
                        "2": "2020-05-31",
                        "3": "2020-06-30",
                        "4": "2020-07-31",
                        "5": "2020-08-31",
                        "6": "2020-09-30",
                        "7": "2020-10-31",
                        "8": "2020-11-30",
                        "9": "2020-12-31",
                        "10": "2021-01-31",
                        "11": "2021-02-28"
                    }
                },
                "working_capital_original_data": {
                    "inventory": {
                        "0": 23210.68142787597,
                        "1": 42555.20567682544,
                        "2": 15615.358311973876,
                        "3": 19094.49796310007,
                        "4": 12754.078579734958,
                        "5": 38228.4017595843,
                        "6": 25809.329741453475,
                        "7": 22433.59908573264,
                        "8": 38745.05561364608,
                        "9": 23439.10169361021,
                        "10": 39110.85092857672,
                        "11": 42607.97581257254
                    },
                    "accounts_receivable": {
                        "0": 9572.93101965891,
                        "1": 18542.82288222848,
                        "2": 16857.60541562315,
                        "3": 5201.273913121867,
                        "4": 14516.523917144455,
                        "5": 19175.407818820975,
                        "6": 5879.508640481812,
                        "7": 22590.4296604746,
                        "8": 15401.628332713462,
                        "9": 5613.220966514358,
                        "10": 9488.272238416805,
                        "11": 24073.51392854626
                    },
                    "accounts_payable": {
                        "0": 19302.8650405072,
                        "1": 16161.02473314525,
                        "2": 19098.961238455187,
                        "3": 13372.73727140053,
                        "4": 5106.200952293356,
                        "5": 5227.102570243851,
                        "6": 15224.435751473731,
                        "7": 6665.819594379985,
                        "8": 6021.509603385136,
                        "9": 24310.332782749465,
                        "10": 22180.052793161172,
                        "11": 8040.544544191391
                    },
                    "id": {
                        "0": 14,
                        "1": 15,
                        "2": 16,
                        "3": 17,
                        "4": 18,
                        "5": 19,
                        "6": 20,
                        "7": 21,
                        "8": 22,
                        "9": 23,
                        "10": 24,
                        "11": 25
                    },
                    "date": {
                        "0": "2020-03-31",
                        "1": "2020-04-30",
                        "2": "2020-05-31",
                        "3": "2020-06-30",
                        "4": "2020-07-31",
                        "5": "2020-08-31",
                        "6": "2020-09-30",
                        "7": "2020-10-31",
                        "8": "2020-11-30",
                        "9": "2020-12-31",
                        "10": "2021-01-31",
                        "11": "2021-02-28"
                    }
                }
            }
        }
    }


def test_invalid_timefame(client: TestClient):
    response = client.get("/cash-flow/calculate?start_date=2019-04-30&timeframe=test")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "enum",
                "loc": [
                    "query",
                    "timeframe"
                ],
                "msg": "Input should be 'monthly', 'quarterly' or 'yearly'",
                "input": "test",
                "ctx": {
                    "expected": "'monthly', 'quarterly' or 'yearly'"
                }
            }
        ]
    }


def test_invalid_start_date_format(client: TestClient):
    response = client.get("/cash-flow/calculate?start_date=2020/03-03&timeframe=monthly")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "date_from_datetime_parsing",
                "loc": [
                    "query",
                    "start_date"
                ],
                "msg": "Input should be a valid date or datetime, invalid date separator, expected `-`",
                "input": "2020/03-03",
                "ctx": {
                    "error": "invalid date separator, expected `-`"
                },
                "url": "https://errors.pydantic.dev/2.6/v/date_from_datetime_parsing"
            }
        ]
    }
