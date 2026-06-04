def test_type_chart():
    from model.type_chart import TypeChart,  TYPE_CHART

    typeChart = TypeChart(TYPE_CHART)
    assert typeChart.multiplier("fire", "water") == 0.5
    assert typeChart.multiplier("fire", "grass") == 2
    assert typeChart.multiplier("poison", "rock") == 0.5
    assert typeChart.multiplier("normal", "ghost") == 0