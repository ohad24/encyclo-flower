def pytest_addoption(parser):
    parser.addoption("--url", action="store")
    parser.addoption(
        "--google-cred-file-location",
        action="store",
        default=None
    )
