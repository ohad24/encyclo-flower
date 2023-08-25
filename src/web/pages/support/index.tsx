import React from "react";
import { motion } from "framer-motion";
import Layout from "../../components/Layout/Layout";
import ImagesSupports from "components/Images/ImagesSupports";
import HeadLine from "components/Headline/headLine";

const Support = () => {
  return (
    <Layout>
      <div className="default-container">
        <HeadLine text={"תומכים"} width={120} />
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
            <br /> <ImagesSupports />* מעוניינים לתמוך גם אתם במיזם? להתפרסם
            כנותני חסות? לקדם את שמירת צמחי הבר? כתבו לנו – והצטרפו למשפחת
            אנציקלופרח ולדרך המשותפת.
          </div>
        </motion.div>
      </div>
    </Layout>
  );
};

export default Support;
