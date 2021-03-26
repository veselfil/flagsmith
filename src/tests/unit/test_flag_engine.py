from builders import build_environment_model


def test(environment):
    environment_model = build_environment_model(environment)
    assert environment_model
