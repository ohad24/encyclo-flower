from typing import Literal

GENUS = Literal[
    "זקנצית",
    "שום",
    "כלנית",
    "עבקנה",
    "צחר",
    "ברברית",
    "בת-לובליה",
    "היפוכריס",
    "ערבז",
    "אבטיח",
    "סתוונית",
    "כרכום",
    "גומא",
    "מלקולמיה",
    "פרנקניה",
    "שמשון",
    "פרע",
    "הפוכריס",
    "אגמון",
    "עפעפית",
    "תורמוס",
    "דבשה",
    "רוזמרין",
    "מוריקה",
    "מגסטומה",
    "קנה",
    "נשרן",
    "כוכבן",
    "אוג",
    "שרשר",
    "חוח",
    "לוענית",
    "שיטה",
    "ציפורנית",
    "מורית",
    "אשבל",
    "דל-קרנים",
    "סוף",
    "בקיה",
    "ירבוז",
    "שלוחית",
    "חודיים",
    "ארנבית",
    "אגבה",
    "קדד",
    "מלוח",
    "שיבולת-שועל",
    "גלונית",
    "עקצר",
    "שרוכנית",
    "לשון-כלב",
    "אורזית",
    "אלומית",
    "עפרון",
    "מקור-חסידה",
    "גדותן",
    "עשנן",
    "מחטנית",
    "טופח",
    "כתמה",
    "שושן",
    "עדעד",
    "מרסיה",
    "מורינגה",
    "נרקיס",
    "דבורנית",
    "סחלב",
    "חבצלת",
    "פרג",
    "פגופירון",
    "ערבה",
    "מרווה",
    "הרדופנין Podospermum",
    "נטופית",
    "זנבן",
    "קחוון",
    "לוע-ארי",
    "כף-אווז",
    "קוצן",
    "חבלבל",
    "גד",
    "עטינית",
    "אחילוטוס",
    "פשתנית",
    "מנתור",
    "אספסת",
    "כרבולת",
    "סמקן",
    "עלקת",
    "שלח",
    "רכפה",
    "אשחר",
    "ורד",
    "זיפן",
    "תלתן",
    "ורוניקה",
    "עקצוץ",
    "בן-חטה",
    "אלקנה",
    "ספלול",
    "עיריוני",
    "אספלנון",
    "אחילוף",
    "בולנתוס",
    "ילקוט",
    "כריך",
    "צלקנית",
    "קרטם",
    "זלזלת",
    "כתרון Coronilla",
    "קרוטלריה",
    "שרביטן",
    "צנינה",
    "ורבורגינת",
    "פרסה",
    "מימון",
    "זקנן",
    "איסטיס",
    "דוגון",
    "לוניאה",
    "סגולית",
    "אזובית",
    "קחונית",
    "אלון",
    "נורית",
    "חמעה",
    "ברזילון",
    "כוכבית",
    "גרגרנית",
    "מתלולן",
    "לענה",
    "לוף",
    "זמזומית",
    "מצלתיים",
    "ציפורני-החתול",
    "קרן-יעל",
    "עוזרר",
    "גלדן",
    "גרניון",
    "יינית",
    "חמציץ",
    "בן-קוצן",
    "כמנון",
    "לחך",
    "געדה",
    "מתנן",
    "קוטב",
    "שילשון",
    "לשון-פר",
    "אסתר",
    "פעמונית",
    "דרדר",
    "באשן",
    "קורידלית",
    "צלבית",
    "כתרים",
    "בן-חילף",
    "חרחבינה",
    "חלבלוב",
    "פרגה",
    "מעלה-עשן",
    "לוטוס",
    "מרקולית",
    "אהל",
    "דו-קרן",
    "שלהבית",
    "שזיף",
    "יתדן",
    "מלעניאל",
    "טבורית",
    "זוזימה",
    "אכילאה",
    "דו-פרית",
    "חוורית",
    "ברומית",
    "לשישית",
    "ניסנית",
    "אדמדמית",
    "ערברבה",
    "כלכלך",
    "שוש",
    "דרכנית",
    "מאירית",
    "זוטה",
    "נופר",
    "לבנונית",
    "אלה",
    "פרעושית",
    "ריבס",
    "מלענן",
    "אשל",
    "ולרינית",
    "דמומית",
    "גלעינית",
    "חלבינה",
    "בן-חורש",
    "צמר",
    "זהבית",
    "שעורה",
    "בינית",
    "אלמוות",
    "בוען",
    "מררית",
    "סיסנית",
    "דורית",
    "וליסנריה",
    "זנב-שועל",
    "צחנן",
    "תודרנית",
    "אזנן",
    "טטרקליניס",
    "כשות",
    "אכסף",
    "פגוניה",
    "פילגון",
    "גרויה",
    "חסה",
    "צללית",
    "ארכובית",
    "קנה-סוכר",
    "מלחית",
    "סביון",
    "תלת-חד",
    "חרשף",
    "זעזועית",
    "קרנונית",
    "לוטם",
    "דורבנית",
    "שכרון",
    "מצילות",
    "בהק",
    "מרבה-חלב",
    "עבדקן",
    "סוויניה",
    "הרדופנין",
    "חרדל",
    "תודרה",
    "נדד",
    "בבונגית",
    "בוצין",
    "סיגל",
    "אליסון",
    "אמברוסיה",
    "חסרף",
    "תלת-מלען",
    "קיצנית",
    "קלינופודיון",
    "טוריים",
    "שחליים",
    "פשתה",
    "מרצענית",
    "נר-הלילה",
    "כף-עוף",
    "ארז",
    "מכנפים",
    "פואנית",
    "פטל",
    "מסרק",
    "טמוס",
    "ארבע-כנפות",
    "גפן",
    "ארביס",
    "חננית",
    "שלמון",
    "דובדבן",
    "ציפורן",
    "חמד",
    "תולענית",
    "ישומון",
    "רימון",
    "אגורה",
    "נוניאה",
    "שברק",
    "פספלון",
    "רב-פרי",
    "פרסיון",
    "דגנין",
    "מכבד",
    "בת-יבלית",
    "דמסון",
    "פלומית",
    "ציצן",
    "עליעב",
    "צהרון",
    "חמנית",
    "טיון",
    "משערת",
    "בת-אורז",
    "חוחן",
    "אחישבת",
    "צנון",
    "סגינה",
    "צתרה",
    "תגית",
    "קערורית",
    "צורית",
    "אגמית",
    "חלמונית",
    "ורבנה",
    "שקד",
    "ארגמון",
    "טובענית",
    "סרב",
    "אלית",
    "גלית",
    "דטורה",
    "קפודן",
    "אל-ציצית",
    "דבקה",
    "סייפן",
    "מתקה",
    "ערטל",
    "אפיונה",
    "יורינאה",
    "מעוג",
    "זון",
    "דודא",
    "מנכיה",
    "אשמר",
    "אפון",
    "אשליל",
    "בקעצור",
    "צמרורה",
    "צבעוני",
    "בוקיצה",
    "בן-מלח",
    "Erigeron",
    "לוגפיה",
    "אירוס",
    "מניפנית",
    "נהרונית",
    "נוציץ",
    "פואה",
    "שנן",
    "צתרנית",
    "שיזף",
    "ליבן",
    "תריסנית",
    "שחליל",
    "ספלילה",
    "סמר",
    "אזוביון",
    "עדשת-מים",
    "מרואה",
    "מלקולמייה",
    "בבונג",
    "ברקן",
    "בר-זית",
    "חמשן",
    "ארנין",
    "קרדומית-כתרון Securigera",
    "אפזרית",
    "גזיר",
    "אנקון",
    "קרדריה",
    "קרקש",
    "דבקנית",
    "רקפת",
    "אריסימון",
    "נזמית",
    "אטד",
    "אזדרכת",
    "נץ-חלב",
    "שסיע",
    "ששית",
    "סולנום",
    "זגאה",
    "צלע-שור",
    "מגנונית",
    "קריתמון",
    "יצהרון",
    "מצמרת",
    "מרמר",
    "זנב-עכבר",
    "נירית",
    "מרור",
    "דבקון",
    "חיעד",
    "אמניה",
    "שחורן",
    "אנטינורית",
    "עירית",
    "כוכב",
    "אצבוע",
    "חרצית",
    "מלפפון",
    "מחרוזת",
    "מדד",
    "חפורית",
    "בן-חצב",
    "מדחול",
    "טורגניה",
    "אבגר",
    "כף-צפרדע",
    "גפוף",
    "בסיה",
    "קרסולה",
    "ירוקת-חמור",
    "כלך",
    "הרקליאון",
    "לשון-שור",
    "מגלית",
    "בן-ציצית",
    "חלמית",
    "מיאגרון",
    "טבק",
    "ליפיה",
    "בשנית",
    "תמריר",
    "רושליה",
    "רופיה",
    "אוכם",
    "אבוטילון",
    "ארנריה",
    "דחנית",
    "רתמה",
    "קיסוס",
    "אזנב",
    "סרפד",
    "עטיה",
    "שערור",
    "בר-דורבן",
    "זנב-כלב",
    "עכנאי",
    "ערער",
    "נרדורית",
    "שנית",
    "רפרף",
    "בת-רכפה",
    "תמר",
    "עפרית",
    "צפצפה",
    "ערידת",
    "סינפיטון",
    "חיטה",
    "שעלב",
    "אליאריה",
    "גפנן",
    "חולית",
    "נורית (פיקריה)",
    "אפרורית",
    "פרקינסוניה",
    "קזוח",
    "נזרית",
    "שלשי",
    "חגוית",
    "חד-שפה",
    "ידיד-חולות",
    "קטלב",
    "נעצוצית",
    "סהרון",
    "ערר",
    "אצבען",
    "איכהורניה",
    "גודיניה",
    "לבדנית",
    "מסמור",
    "צלען",
    "סכיכון",
    "עדשה",
    "מליסה",
    "קצח",
    "אחיגזר",
    "צמרנית",
    "טרשנית",
    "זוגן",
    "חספסת",
    "דו-שן",
    "כרוב",
    "קרדמין",
    "כליל",
    "דונגית",
    "גזר",
    "זקנונית",
    "מילה",
    "עוקץ-עקרב",
    "גלעינון",
    "גרגריון",
    "גרגיר",
    "לשון-אפעה",
    "פלגית",
    "שלחלח",
    "סנא",
    "זיברה",
    "כף-חתול",
    "חטמית",
    "יפרוק",
    "אנודה",
    "כרסתן",
    "לעוסית",
    "דק-זנב",
    "ינבוט",
    "קיסוסית",
    "חלוקה",
    "שמשונית",
    "בן-חרדל",
    "דם-המכבים",
    "לפית",
    "זרעזיף",
    "זכריני",
    "דוחן",
    "מציץ",
    "סקליגריה",
    "חצב",
    "יבשוש",
    "הגה",
    "גבשונית",
    "קנרס",
    "אלניה",
    "בר-גביע",
    "מללויקה",
    "נפית",
    "הרדוף",
    "שננית",
    "פיטולקה",
    "בקבוקון",
    "רומולאה",
    "נסמנית",
    "ריסן",
    "כרבולתן",
    "סחלבן",
    "בר-נורית",
    "כוסנית",
    "קרד",
    "בת-מדבר",
    "אתרוג",
    "דו-מוץ",
    "בן-סחלב",
    "איטן",
    "עצבונית",
    "קיטה",
    "כנפון",
    "צלף",
    "אביבית",
    "פיגמית",
    "מעריב",
    "לפופית",
    "כרמלית",
    "בן-פרג",
    "עלוק",
    "חרירים",
    "עשבה",
    "כונדרילה",
    "כחלית",
    "כדן",
    "עלקלוק",
    "טפרוסיה",
    "לכיד",
    "Tetraena",
    "חדעד",
    "קחוינה",
    "דלעת-נחש",
    "חרוב",
    "עולש",
    "לשנן",
    "עכובית",
    "ערטנית",
    "רגלה",
    "רותם",
    "שושנתית",
    "וינקה",
    "אזולה",
    "אברנית",
    "חופניים",
    "בלבסן",
    "תות",
    "זיף-נוצה",
    "ארויה",
    "לועית",
    "ושינגטוניה",
    "לחן",
    "רב-מוץ",
    "דרבה",
    "ישרוע",
    "עוגית",
    "כף-זאב",
    "מרסיליה",
    "שלטה",
    "גזרנית",
    "חרטומית",
    "טלפיון",
    "בת-קורנית",
    "זקן-תיש",
    "אנטיכריס",
    "בת-חלמית",
    "שנס",
    "חלביב",
    "כנפן",
    "פיגם",
    "בן-חרצית",
    "זיזיים",
    "זקן-סב",
    "סווד",
    "עקר",
    "רוריפה",
    "בן-דחן",
    "סילון",
    "אאירה",
    "מרגנית",
    "פרסטיה",
    "משקפיים",
    "חזרזרת",
    "מסורן",
    "ליסיאה",
    "סמבוק",
    "בן-אפר",
    "דורה",
    "טיסדליה",
    "גביעול",
    "אמיתה",
    "זקניים",
    "דרבונית",
    "אלטין",
    "דום",
    "ליסימכיה",
    "נימפאה",
    "הילל",
    "יקשן",
    "סידה",
    "שלש-כנפות",
    "פשטה",
    "חבלבלן",
    "קרדה",
    "ספה",
    "כתלה",
    "כרבה",
    "דקורניה",
    "אמיך",
    "לולינית",
    "גלנית",
    "מוצנית",
    "סיסון",
    "מלענת",
    "זערורית",
    "אבובית",
    "כספסף",
    "קידה",
    "אזן-גדי",
    "בלוטנית",
    "יבלית",
    "יורניה",
    "מורטיה",
    "אלף-עלה",
    "אורן",
    "ביברשטיניה",
    "עריר",
    "היביסקוס",
    "דמיה",
    "בופוניה",
    "פתילת-המדבר",
    "שרכרך",
    "יקינטונית",
    "אחירותם",
    "חספסנית",
    "שמרר",
    "שרדיניה",
    "פקטורובסקיית",
    "מנטיסלקה",
    "גלימה",
    "מוצית",
    "אגס",
    "בן-חוזרר",
    "בר-עשנן",
    "קוסיניה",
    "צברת",
    "בן-טיון",
    "שנק",
    "בר-לע",
    "פלפלון",
    "נאדיד",
    "חוטית",
    "דרדית",
    "טופל",
    "ילקוטון",
    "מללנית",
    "כתנן",
    "אולדנית",
    "אחי-חרגל",
    "אברה",
    "קיקיון",
    "גפית",
    "ישימונית",
    "אנדרוסק",
    "פקעון",
    "קרנן",
    "חילף",
    "משין",
    "מישויה",
    "בן-סירה",
    "אבי-ארבע",
    "כרפס",
    "חד-אבקן",
    "יחנוק",
    "שבטבט",
    "גביעונית",
    "לקוקיה",
    "נענע",
    "מפריק",
    "כותלית",
    "קרקפן",
    "רבועה",
    "אגרוסטמה",
    "עוגנן",
    "אספרג",
    "דו-פרק",
    "כפיות",
    "רימונית",
    "בר-עכנאי",
    "ניל",
    "חטוטרן",
    "פרתניון",
    "דלב",
    "נימית",
    "סם-כלב",
    "לובד",
    "חשפונית",
    "ברבראה",
    "סיסן",
    "שעלבית",
    "גלניה",
    "אחישום",
    "ניקנדרה",
    "אדר",
    "נוצנית",
    "משיובית",
    "ססבניה",
    "לוביה",
    "אהרונסוניה",
    "קורנית",
    "חנק",
    "נואית",
    "עדעדית",
    "כדורן",
    "טורגנית",
    "סבונית",
    "ויתניה",
    "מרית",
    "דגנה",
    "לבדן",
    "רצועית",
    "שעמון",
    "סלביניה",
    "סירה",
    "רב-גולה",
    "בת-חול",
    "חבושית",
    "בן-שעורה",
    "לטמית",
    "בטנונית",
    "שבטן",
    "אדמונית",
    "מרונית",
    "שיח-אברהם",
    "שפרירה",
    "בוציץ",
    "פמה",
    "דו-כנף",
    "הררית",
    "שנהבית",
    "שבטוט",
    "פוקה",
    "משנצת",
    "לוטונית",
    "רשתון",
    "כפתור",
    "בצלציה",
    "גמד",
    "חוזרר",
    "לפסנה",
    "פריינית",
    "אחיגמא",
    "שפתן",
    "זליה",
    "זקום",
    "תכלתן",
    "צלצל",
    "בצעוני",
    "פיקוס",
    "כליינית",
    "יערה",
    "פספלת",
    "חלוק",
    "סלודורה",
    "קוציץ",
    "פורסקולאה",
    "גבסנית",
    "טיונית",
    "רכפתן",
    "לבנה",
    "שלחופן",
    "ביצן",
    "שבת",
    "אסתום",
    "כרפסית",
    "ימלוח",
    "צנורית",
    "ולרינה",
    "זעריר",
    "סלק",
    "בורהביה",
    "בואסירה",
    "גלינסוגה",
    "כנפה",
    "חוגית",
    "איסם",
    "איילנתה",
    "דנתוניה",
    "זנב-ארנבת",
    "הרנוג",
    "מחמש",
    "פרקן",
    "טגטס",
    "שושנת-יריחו",
    "מיש",
    "איקליפטוס",
    "ער",
    "נאוטינאה",
    "טורית",
    "כדרורית",
    "לופית",
    "שרעול",
    "עדן",
    "נידה",
    "זנב-עקרב",
    "מורן",
    "סייגית",
    "ברגיה",
    "קרצף",
    "רוש",
    "זנבה",
    "דודוניאה",
    "יקינטון",
    "ארבעוני",
    "שלשית",
    "מלוכיה",
    "קפודית",
    "פלופיה",
    "שומר",
    "יסמין",
    "לנטנה",
    "זית",
    "שבר",
    "זצניה",
    "גדילן",
    "אינדיה",
    "אצבעית",
    "ימון",
    "שיפון",
    "ארקטותקה",
    "רב-רגל",
    "פיסטיה",
    "שעונית",
    "שערות-שולמית",
    "אוג (סירסיה)",
    "שרכייה",
    "אמקורית",
    "סלולית",
    "אלואינה",
    "טחובית",
    "חבליל",
    "אורתוטריכום",
    "פיסידנס",
    "גרימיה",
    "קזוארינה",
    "צפורנית",
    "אלשן",
    "סקלרופודיום",
    "סינטריכיה",
    "צייצת",
    "רבוליה",
    "מיקרובריום",
    "פליה",
    "טרגיוניה",
    "פילונוטיס",
    "סהרונית",
    "פלאורוכטה",
    "ברקית",
    "אוקסימיטרה",
    "מרשנטיה",
    "אתלמיה",
    "פוסומברוניה",
    "אמקור",
    "רינכוסטגיום",
    "אנטיטריכיה",
    "זקנית",
    "טימיאלה",
    "אנתוסטודון",
    "עקרבית",
    "צנופית",
    "צבר",
    "אמבליסטגיום",
    "ספרוקרפוס",
    "ריקציה",
    "וויסיה",
    "טורטלה",
    "משינית",
    "פברוניה",
    "טריכוסטומום",
    "חרגל",
    "אשחרית",
    "בת-גלית",
    "ימית",
    "פואירנה",
    "",
    "בן-בצת",
    "בקמניה",
    "בת-סיסנית",
    "גמדונית",
    "דחנן",
    "מצדית",
    "משבל",
    "נחלית",
    "רב-זקן",
    "רפרפון",
    "שנפלדיה",
    "דטיסקה",
    "גיאון",
    "סולננתה",
    "שנין",
    "פילנתוס",
    "דיגרה",
    "חצצון",
    "בוריכיה",
    "גיזוטיה",
    "גרדיולוס",
    "דיסודיה",
    "חסנית",
    "קוטולה",
    "קרדנית",
    "שופרית",
    "אלודאה",
    "אבריים",
    "איקלידון",
    "ארכן",
    "בורובית",
    "הלדריכיה",
    "לפתית",
    "צלוקית",
    "קמלינה",
    "קרקשית",
    "דפנית",
    "ברכנית",
    "דק-נוף",
    "בת-חבצלת",
    "ברולה",
    "חרמשית",
    "כמנונית",
    "כרופילון",
    "סוכשך",
    "עבדור",
    "הלופפליס",
    "פרדתים",
    "פודנתון",
    "חמצה",
    "חרטום",
    "סיסם",
    "רוביניה",
    "בורית",
    "נוקשן",
    "שביט",
    "ששן",
    "אלוי",
]

CLADE1 = Literal["צמחי הזרעים", "שרכים", "צמחי עובר"]

CLADE2 = Literal[
    "מכוסי הזרע",
    "שרכניים",
    "שרביטניים (גנטניים)",
    "אצטרובלניים",
    "שבטבטיים",
    "טחבי עלים",
    "טחבי כבד",
]

CLADE3 = Literal[
    "חד-פסיגיים",
    "דו-פסיגיים",
]

FAMILY = Literal[
    "דגניים",
    "נרקיסיים",
    "נוריתיים",
    "קטניות",
    "ערטניתיים",
    "פעמוניתיים",
    "מורכבים",
    "ערבזיים",
    "דלועיים",
    "סתווניתיים (שושניים)",
    "אירוסיים",
    "גמאיים",
    "מצליבים",
    "פרנקניים",
    "לוטמיים",
    "פרעיים",
    "לועניתיים",
    "שפתניים",
    "זיפניים",
    "אלתיים",
    "סלקיים",
    "ציפורניים",
    "סוככיים",
    "סופיים",
    "ירבוזיים",
    "חלבלוביים",
    "שושניים",
    "גרניים",
    "עשנניים",
    "עפריתיים",
    "מורינגיים",
    "סחלביים",
    "פרגיים",
    "ארכוביתיים",
    "ערבתיים",
    "חלמיתיים",
    "ורדיים",
    "חבלבליים",
    "עלקתיים",
    "רכפתיים",
    "אשחריים",
    "ספלוליים",
    "אספלניים",
    "לופיים",
    "חיעדיים",
    "שרביטניים",
    "פואתיים",
    "מימוניים",
    "אלוניים",
    "חמציציים",
    "לחכיים",
    "מתנניים",
    "זוגניים",
    "צלפיים",
    "אסקלפיים",
    "טבוריתיים",
    "נר-הלילה",
    "נופריים",
    "אשליים",
    "ולריניים",
    "סולניים",
    "ברושיים",
    "טליתיים",
    "מרבה-חלב",
    "סגליים",
    "פשתיים",
    "אורניים",
    "טמוסיים",
    "גפניים",
    "שלמוניים",
    "כפריים",
    "כף-הצפרדע",
    "עדשת-המים",
    "ורבניים",
    "טובעניתיים",
    "גליתיים",
    "בקעצוריים",
    "מישיים",
    "נהרוניתיים",
    "אדריים",
    "סמריים",
    "זיתיים",
    "רקפתיים",
    "אזדרכתיים",
    "יצהרוניים",
    "הרנוגיים",
    "רופיניים",
    "קיסוסיים",
    "סרפדיים",
    "דקליים",
    "אפרוריתיים",
    "אברשיים",
    "סהרוניים",
    "פונטדריים",
    "טרשניתיים",
    "לשון-אפעה",
    "סנטליים",
    "הדסיים",
    "הרדופיים",
    "פיטולקיים",
    "קוציציים",
    "פיגמיים",
    "רגלתיים",
    "אזוליים",
    "אברניתיים",
    "תותיים",
    "מרסיליים",
    "יערתיים",
    "אלטיניים",
    "לילניים",
    "אלף-העלה",
    "שרכרכיים",
    "נאדידיים",
    "חוטיתיים",
    "טופליים",
    "אברתיים",
    "שרכיתיים",
    "קרנניים",
    "שבטבטיים",
    "רפלסיים",
    "דלביים",
    "חשפוניתיים",
    "כדורניים",
    "סלביניים",
    "אדמוניתיים",
    "בוציציים",
    "כפתוריים",
    "סלודוריים",
    "לבניים",
    "סימרוביים",
    "עריים",
    "נידיים",
    "סבונניים",
    "רב-רגליים",
    "שעוניתיים",
    "שערות-שולמית",
    "שרכיניים",
    "טחבי עלים",
    "קזואריניים",
    "טחבי כבד",
    "צבריים",
    "דטיסקיים",
]

# * For future use
# clade4 = []

SUBFAMILY = Literal["פרפרניים", r"מימוסיים \ שיטיים", "קסאלפיניים"]
