import React from "react";
import Layout from "../../components/Layout/Layout";
import { motion } from "framer-motion";

const writeToUs = () => {
  return (
    <Layout>
      <div className="default-container">
        <div className="flex items-center justify-center my-5">
          <p className="font-bold text-secondary  border-b-4 border-b-orange-300 text-xl w-[80px] text-center ">
            כתבו לנו{" "}
          </p>
        </div>
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
