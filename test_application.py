from application import calculate_results


def test_male():
    mock_data = {
        "Equipment": "Raw",
        "Sex": "M",
        "Age": "17",
        "Bodyweight": "70",
        "Squat": "100",
        "Bench": "100",
        "Deadlift": "100",
    }
    results = calculate_results(mock_data)

    assert results["weight_bin"] == "74kg"
    assert results["age_bin"] == "15-20"
    assert results["best3SquatKg_result"] == "4.9%"
    assert results["best3BenchKg_result"] == "49.9%"
    assert results["best3DeadliftKg_result"] == "0.7%"
    assert results["totalKg_result"] == "4.7%"


def test_female():
    mock_data = {
        "Equipment": "Raw",
        "Sex": "F",
        "Age": "17",
        "Bodyweight": "70",
        "Squat": "100",
        "Bench": "100",
        "Deadlift": "100",
    }
    results = calculate_results(mock_data)

    assert results["weight_bin"] == "76kg"
    assert results["age_bin"] == "15-20"
    assert results["best3SquatKg_result"] == "37.4%"
    assert results["best3BenchKg_result"] == "98.7%"
    assert results["best3DeadliftKg_result"] == "12.9%"
    assert results["totalKg_result"] == "58.4%"
