import React from "react";
import { Spinner } from "@chakra-ui/react";
import { motion, AnimatePresence } from "framer-motion";

interface Props {
  text: string;
  isLoading: boolean;
}
const Loader = ({ text = "Loading...", isLoading }: Props) => {
  return (
    <div>
      {isLoading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <AnimatePresence>
            <div className="wof-loader">
              <div className="loader-bg"></div>
              <div className="wof-loader-content">
                <div className="flex items-center  flex-col gap-0 justify-center">
                  <div>
                    <Spinner
                      color="white"
                      emptyColor="gray.300"
                      size="xl"
                      thickness="15px"
                      speed="1.5s"
                    />
                  </div>
                  <div>{text}</div>
                </div>
              </div>
            </div>
          </AnimatePresence>
        </motion.div>
      )}
    </div>
  );
};

export default Loader;
