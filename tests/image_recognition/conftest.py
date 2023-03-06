def pytest_addoption(parser):
    parser.addoption("--url", action="store")
    parser.addoption("--google-cred-file-location", action="store", default=None)


ASSERT_DETECT_DATA = [
    {"class_name": "Erodium gruinum", "score": 0.09766},
    {"class_name": "Solanum laciniatum", "score": 0.05078},
    {"class_name": "Ipomoea indica", "score": 0.03906},
    {"class_name": "Nicandra physalodes", "score": 0.03516},
    {"class_name": "Hibiscus trionum", "score": 0.03125},
]
