import React from "react";
import Layout from "../../components/Layout/Layout";
import { motion } from "framer-motion";
import HeadLine from "components/HeadLine/HeadLine";

const About = () => {
  return (
    <Layout>
      <div className="default-container">
        <div className="flex flex-col justify-center items-center">
          <HeadLine text={"אודות"} width={120} />
          <motion.div
            className="text-secondary mb-10 max-w-[1000px]"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.7 }}
          >
            ברוכים הבאים לאנציקלופרח.
            <br />
            מי מאיתנו חובבי הצמחים לא חווה הגדרה ארוכה ומסורבלת בספרי ההגדרה
            הכבדים שסחבנו על הגב, באין ספור אתרי אינטרנט, בפורומים ובאפליקציות
            שלא תמיד מצליחות להגדיר?
            <br />
            אחרי שנים (אפשר לומר של תסכול מהמצב), החלטנו לעשות צעד –
            <br />
            <p className="font-bold">
              להעניק גם למתענייני הצומח בישראל את הכבוד הראוי להם - במגדיר
              איכותי, מהיר, מתקדם, וחשוב מכל – להכניס את כל אלה לכיס שלנו
              באפליקציה מותאמת לנייד בכל מקום ובכל זמן!
            </p>{" "}
            על מנת להקים את המיזם, שקד ועמל צוות אנציקלופרח מתוך הכרת החשיבות
            שבשמירת-הטבע ומתוך שאיפה להנגיש אותו לציבור הישראלי הרחב, באמצאות
            פתרון אופטימלי לזיהוי, הגדרה ושיתוף צמחי בר.
            <br />
            ועכשיו קצת מעבר למגדיר עצמו, <br />
            בכל שעות העבודה הרבות של הקמה והפעלת המיזם אנו תמיד רואים לנגד
            עניינו את
            <span className="font-bold">
              {" "}
              השליחות החשובה שבהעלאת המודעות לצמחי הבר בפרט ולשמירת טבע בכלל{" "}
            </span>
            כשליחות חשובה מעין כמוה בעידן של פיתוח מואץ. <br />
            ברור לנו ששמירה על אותם בתי גידול וצמחי בר מתחילה קודם כל בחינוך,
            וזה מתחיל בהנגשת עולם הצומח לכל ילד, ילדה, זקן וטף. הנגשה אמיתית,
            פשוטה, מהירה ונוחה. <br />
            ללא הנגשת תחום צמחי הבר לציבור הישראלי אל לנו להתלונן בדיעבד על
            אובדן מינים ועל רבים הנתונים בסכנת הכחדה. <br />
            <span className="font-bold">עזרתכם חשובה! </span>
            <br />
            אנציקלופרח הוא מיזם קהילתית המתקיים וניזון מ{`"חכמת ההמונים"`}.{" "}
            <br />
            העלו תמונות של צמחי הבר שסביבכם, ושתפו את ידיעותיכם על צמחי הבר!
            <br />
            <span className="font-bold">
              שיתוף תמונות, שאלות ותשובות על זיהוי לא רק יסיעו במענה מהיר
              לסקרנים אלא גם יתרמו לשיפור מאגר המידע הבוטני –
            </span>{" "}
            יחד ניצור מערכת חכמה, שתקל על סקרניות וסקרנים להכיר את צמחי הבר
            ותהווה מאגר מידע רחב עם חשיבות מחקרית וציבורית -{" "}
            <span className="font-bold">
              כל שאלה/תשובה/תמונה יהיו עוד צעד לשמירת צמחי הבר של ישראל.{" "}
            </span>{" "}
            <br /> <br />
            הגדרה נעימה! <br />
            צוות אנציקלופרח.
          </motion.div>
        </div>
      </div>
    </Layout>
  );
};

export default About;
