import React from "react";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalBody,
  ModalCloseButton,
  Tabs,
  Tab,
  TabList,
  TabPanels,
  TabPanel,
} from "@chakra-ui/react";
import Register from "../Register/Register";

import Login from "components/Login/Login";

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

const LoginAndRegisterModel = ({ isOpen, onClose }: Props) => {
  return (
    <div>
      <Modal isCentered isOpen={isOpen} onClose={onClose} size="2xl">
        <ModalOverlay
          bg="none"
          backdropFilter="auto"
          backdropInvert="0%"
          backdropBlur="5px"
        />
        <ModalContent>
          <ModalCloseButton />
          <ModalBody className="mt-[2rem]">
            <Tabs variant="enclosed">
              <TabList>
                <Tab>
                  <p className="text-lg font-bold text-secondary border-b-4 border-primary max-w-[200px] text-center mb-4">
                    התחברות
                  </p>
                </Tab>
                <Tab>
                  <p className="text-lg font-bold text-secondary border-b-4 border-primary max-w-[200px] text-center mb-4">
                    הרשמה
                  </p>
                </Tab>
              </TabList>
              <TabPanels className="min-h-[350px] flex items-center justify-center">
                <TabPanel>
                  <Login onClose={onClose} />
                </TabPanel>
                <TabPanel>
                  <Register />
                </TabPanel>
              </TabPanels>
            </Tabs>
          </ModalBody>
        </ModalContent>
      </Modal>
    </div>
  );
};

export default LoginAndRegisterModel;
