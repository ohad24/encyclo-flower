import React, { useState } from "react";
import { useRouter } from "next/router";
import Layout from "components/Layout/Layout";
import { postWithObj } from "services/flowersService";
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

import Input from "components/Input/Input";

interface Obj {
  password: string;
  confirm_password: string;
}

const initialUser: Obj = {
  password: "",
  confirm_password: "",
};

const Reset = () => {
  const [obj, setObj] = useState<Obj>(initialUser);
  const [error, setError] = useState<string>("");
  const [success, setSuccess] = useState<boolean>(false);
  const router = useRouter();

  const isError = (p: string) => {
    const isError: boolean = p.length > 1;
    return isError;
  };

  const onChange = (
    e: React.FormEvent<HTMLInputElement> | React.ChangeEvent<HTMLSelectElement>
  ) => {
    const name = e.currentTarget.name;
    const value = e.currentTarget.value;
    setObj({ ...obj, [name]: value });
  };

  const validateForm = () => {
    let isValid: boolean = true;
    if (obj.password.length < 1) {
      setError("סיסמה - חובה");
      isValid = false;
    } else if (obj.password !== obj.confirm_password) {
      setError("סיסמאות לא תואמות");
      isValid = false;
    }
    return isValid;
  };

  const reset = async () => {
    setError("");
    if (!validateForm()) return;
    try {
      await postWithObj("reset-password", {
        ...obj,
        token: router.query.token,
      });
      setSuccess(true);
    } catch (err: any) {
      console.log(err.response.data.error);
      setError("איפוס הסיסמה נכשל");
    }
  };

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
                    <div>
                      <Input
                        text={"סיסמה"}
                        inputName={"password"}
                        val={obj.password}
                        onChange={onChange}
                        error={""}
                      />
                      <Input
                        text={"אימות סיסמה"}
                        inputName={"confirm_password"}
                        val={obj.confirm_password}
                        onChange={onChange}
                        error={""}
                      />
                      <p
                        className={`${
                          isError(error) ? "" : "hidden"
                        }bg-red-300 text-sm text-white rounded px-1 p-[.5px] my-1 text-center`}
                      >
                        {error}
                      </p>
                      {success ? (
                        <p
                          className={
                            "bg-sky-300 text-sm text-white rounded px-1 p-[.5px] my-1 text-center"
                          }
                        >
                          {"הסיסמה אופסה בהצלחה"}
                        </p>
                      ) : null}
                      <button
                        className="button-primary w-full mt-2"
                        onClick={reset}
                      >
                        אפס סיסמה
                      </button>
                    </div>
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
