def pytest_addoption(parser):
    parser.addoption("--url", action="store")
    parser.addoption("--google-cred-file-location", action="store", default=None)


ASSERT_DETECT_DATA = [
    {"class_name": "Erodium gruinum", "score": 0.13281},
    {"class_name": "Ipomoea indica", "score": 0.05469},
    {"class_name": "Solanum laciniatum", "score": 0.04688},
    {"class_name": "Nicandra physalodes", "score": 0.04297},
    {"class_name": "Hibiscus trionum", "score": 0.02344},
]
