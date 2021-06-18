from flag_engine.builders import build_environment_model


def test(environment, feature):
    environment_model = build_environment_model(environment)
    assert environment_model
