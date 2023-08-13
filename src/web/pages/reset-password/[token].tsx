import React from "react";
import Layout from "components/Layout/Layout";
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
import Router from "next/router";
import FormResetPassword from "components/Forms/FormResetPassword";

const Reset = () => {
  const nextPage = (path: string) => {
    Router.push({
      pathname: path,
    });
  };

  return (
    <Layout>
      <div className="default-container">
        <Modal
          isCentered
          isOpen={true}
          onClose={() => nextPage("/")}
          size="2xl"
        >
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
                      איפוס סיסמה
                    </p>
                  </Tab>
                </TabList>
                <TabPanels className="min-h-[350px] flex items-center justify-center">
                  <TabPanel>
                    <FormResetPassword />
                  </TabPanel>
                </TabPanels>
              </Tabs>
            </ModalBody>
          </ModalContent>
        </Modal>
      </div>
    </Layout>
  );
};

export default Reset;
