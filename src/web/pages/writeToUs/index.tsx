import React from "react";
import Layout from "../../components/Layout/Layout";
import { motion } from "framer-motion";
import HeadLine from "components/HeadLine/headLine";

const writeToUs = () => {
  return (
    <Layout>
      <div className="default-container">
        <HeadLine text={"כתבו לנו"} width={110} />
        <motion.div
          className="flex justify-center text-lg"
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 120 }}
          transition={{ duration: 0.7 }}
        >
          <motion.p
            className="text-secondary max-w-[1000px]"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 120 }}
            transition={{ duration: 0.7 }}
          >
            {" "}
            אנו צוות אנציקלופרח, עושים כל שביכולתינו על מנת לתת לכם את החוויה
            הטובה ביותר. נשמח לקבל פידבק, הערות, הצעות לשיפור, תיקונים ופשוט כל
            דבר שמתחשק לכם לחלוק! במייל: encyclo.flower@gmail.com
          </motion.p>
        </motion.div>
      </div>
    </Layout>
  );
};

export default writeToUs;
