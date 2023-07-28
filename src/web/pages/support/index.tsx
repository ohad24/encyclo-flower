import React from "react";
import Image from "next/image";
import { motion } from "framer-motion";
import support1 from "../../images/support-1.png";
import support2 from "../../images/support-2.jpg";
import support3 from "../../images/support-3.jpg";
import Layout from "../../components/Layout/Layout";

const Support = () => {
  return (
    <Layout>
      <div className="default-container">
        <div className="flex items-center justify-center my-5">
          <p className="font-bold text-secondary  border-b-4 border-b-orange-300 text-xl w-[120px] text-center ">
            תומכים
          </p>
        </div>
        <motion.div
          className="flex justify-center text-lg"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.7 }}
        >
          <div className="text-secondary max-w-[1001px]">
            <p className="font-bold">
              הקמת מיזם אנציקלופרח התאפשרה הודות לקבלת המיזם למרכז היזמות
              והחדשנות של מכללת תל-חי והקרן הקיימת לישראל.
            </p>
            מיזם אנציקלופרח הוקם במטרה לשמור ולהגן על הטבע הישראלי המיוחד כל כך.
            אנו שואפים לעשות זאת באמצעות מתן כלי חכם ומתקדם לציבור הרחב, שיסייע
            לכל אחת ואחד לכיר מקרוב, בקלות ובפשטות את צמחי הבר של ישראל.
            <br />{" "}
            <p className="font-bold">
              אך כל זה לא היה מתאפשר ללא תמיכת מרכז היזמות והחדשנות, מכללת תל
              חי, והקרן הקיימת לישראל.
            </p>{" "}
            על כן אנו צוות המיזם וכלל המשתמשים והנהנים ממנו, מוקירים ומברכים על
            תמיכה זו להגדלת המודעות ועל חשיבותה להגדלת המודעות לצמחי הבר ולשמירת
            הטבע הישראלי.
            <br />{" "}
            <div className="flex flex-col md:flex-row items-center md:justify-center  gap-[1.6rem] md:gap-[4.5rem]   min-h-[310px] md:min-h-[170px]">
              <div>
                <Image
                  width="280px"
                  height="92.14px"
                  src={support1}
                  alt="support kkl "
                />
              </div>
              <div>
                <Image
                  width="280px"
                  height="118.69px"
                  src={support2}
                  alt="support kkl "
                />
              </div>
              <div>
                <Image
                  width="280px"
                  height="157px"
                  src={support3}
                  alt="support 2 "
                />
              </div>
            </div>
            * מעוניינים לתמוך גם אתם במיזם? להתפרסם כנותני חסות? לקדם את שמירת
            צמחי הבר? כתבו לנו – והצטרפו למשפחת אנציקלופרח ולדרך המשותפת.
          </div>
        </motion.div>
      </div>
    </Layout>
  );
};

export default Support;
/*  
    <Layout>
      <div className="default-container">
        <div className="flex items-center justify-center my-5">
          <p className="font-bold text-secondary  border-b-4 border-b-orange-300 mb-7 text-xl w-[120px] text-center ">
            תומכים
          </p>
        </div>
        <motion.div
          className="flex justify-center my-10 text-lg"
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 120 }}
          transition={{ duration: 0.7 }}
        >
          <motion.p
            className="text-secondary"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 120 }}
            transition={{ duration: 0.7 }}
          >
            <p className="font-bold">
              הקמת מיזם אנציקלופרח התאפשרה הודות לקבלת המיזם למרכז היזמות
              והחדשנות של מכללת תל-חי והקרן הקיימת לישראל.
            </p>
            <br />
            מיזם אנציקלופרח הוקם במטרה לשמור ולהגן על הטבע הישראלי המיוחד כל כך.
            אנו שואפים לעשות זאת באמצעות מתן כלי חכם ומתקדם לציבור הרחב, שיסייע
            לכל אחת ואחד לכיר מקרוב, בקלות ובפשטות את צמחי הבר של ישראל.
            <br />{" "}
            <p className="font-bold">
              אך כל זה לא היה מתאפשר ללא תמיכת מרכז היזמות והחדשנות, מכללת תל
              חי, והקרן הקיימת לישראל.
            </p>{" "}
            על כן אנו צוות המיזם וכלל המשתמשים והנהנים ממנו, מוקירים ומברכים על
            תמיכה זו להגדלת המודעות ועל חשיבותה להגדלת המודעות לצמחי הבר ולשמירת
            הטבע הישראלי.
            <br />{" "}
            <motion.div
              className="flex flex-col md:flex-row items-center md:justify-center  gap-[1.6rem] md:gap-[4.5rem]   min-h-[310px] md:min-h-[170px]"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 120 }}
              transition={{ duration: 0.7 }}
            >
              <div>
                <Image
                  width="280px"
                  height="92.14px"
                  src={support1}
                  alt="support kkl "
                />
              </div>
              <div>
                <Image
                  width="280px"
                  height="118.69px"
                  src={support2}
                  alt="support kkl "
                />
              </div>
              <div>
                <Image
                  width="280px"
                  height="157px"
                  src={support3}
                  alt="support 2 "
                />
              </div>
            </motion.div>
            * מעוניינים לתמוך גם אתם במיזם? להתפרסם כנותני חסות? לקדם את שמירת
            צמחי הבר? כתבו לנו – והצטרפו למשפחת אנציקלופרח ולדרך המשותפת.
          </motion.p>
        </motion.div>
      </div>
    </Layout>*/
