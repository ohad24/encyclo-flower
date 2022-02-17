from typing import Literal, Tuple, get_args

HebMonthLiteral = Literal[
    "ינואר",
    "פברואר",
    "מרץ",
    "אפריל",
    "מאי",
    "יוני",
    "יולי",
    "אוגוסט",
    "ספטמבר",
    "אוקטובר",
    "נובמבר",
    "דצמבר",
]

# * from https://stackoverflow.com/questions/64522040/typing-dynamically-create-literal-alias-from-list-of-valid-values
HebMonths: Tuple[HebMonthLiteral] = get_args(HebMonthLiteral)

LocationHebLiteral = Literal[
    "חוף הגליל",
    "חוף הכרמל",
    "שרון",
    "מישור החוף הדרומי",
    "גליל עליון",
    "גליל תחתון",
    "כרמל",
    "רמות מנשה",
    "עמק יזרעאל",
    "הרי שומרון",
    "שפלת יהודה",
    "הרי יהודה",
    "צפון הנגב",
    "מערב הנגב",
    "מרכז והר הנגב",
    "דרום הנגב",
    "עמק החולה",
    "בקעת כינרות",
    "עמק בית שאן",
    "גלבוע",
    "מדבר שומרון",
    "מדבר יהודה",
    "בקעת הירדן",
    "בקעת ים המלח",
    "ערבה",
    "חרמון",
    "גולן",
    "גלעד",
    "עמון",
    "מואב",
    "אדום",
]
