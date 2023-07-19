import React, { useState } from "react";
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
import { login } from "services/flowersService";
import { useDispatch } from "react-redux";
import { UpdateToken, UpdateUserName } from "redux/action";

type Props = {
  isOpen: boolean;
  onClose: () => void;
};

interface User {
  username: string;
  password: string;
}

const initialUser: User = {
  username: "",
  password: "",
};

const API_URL = process.env.SERVER_BASE_URL || "";

const LoginAndRegisterModel = ({ isOpen, onClose }: Props) => {
  const [user, setUser] = useState<User>(initialUser);
  const dispatch = useDispatch();
  const [errors, setErrors] = useState({
    ...initialUser,
    accept_terms_of_service: true,
  });
  const [isRegisterError, setIsRegisterError] = useState(false);

  const validateForm = () => {
    let isValid: boolean = true;
    if (user.username.length < 1) {
      setErrors((prev) => {
        return { ...prev, username: "שם משתמש - חובה" };
      });
      isValid = false;
    }

    if (user.password.length < 1) {
      setErrors((prev) => {
        return { ...prev, password: "סיסמה - חובה" };
      });
      isValid = false;
    }

    return isValid;
  };
  const handleChange = (
    e:
      | React.ChangeEvent<HTMLSelectElement>
      | React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value } = e.target;
    const obj = { ...user };
    (obj as any)[name] = value;
    setUser(obj);
  };

  const connection = async () => {
    setErrors({
      ...initialUser,
      accept_terms_of_service: true,
    });

    if (!validateForm()) return;
    setIsRegisterError(false);
    try {
      const { data } = await login("token", user);
      dispatch(UpdateToken(data.access_token));
      onClose();
    } catch (err: any) {
      setIsRegisterError(true);
      console.log(err);
    }
  };

  const isError = (p: string) => {
    const isError: boolean = p.length > 1;
    return isError;
  };
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
                  <div
                    style={{ overflow: "hidden" }}
                    className="flex  flex-col items-center  justify-center "
                  >
                    <div>
                      <div className=" flex flex-col gap-4 w-[200px]   md:w-[300px]">
                        <div>
                          <input
                            className="input w-full"
                            type="text"
                            name="username"
                            placeholder="שם משתמש"
                            onChange={handleChange}
                          />
                          <p
                            className={`${
                              isError(errors.username) ? "" : "hidden"
                            } bg-red-300 text-sm text-white rounded px-1 p-[.5px] my-1 text-center`}
                          >
                            {errors.username}
                          </p>
                        </div>
                        <div>
                          <input
                            className="input w-full"
                            type="password"
                            name="password"
                            placeholder="סיסמה"
                            onChange={handleChange}
                          />
                          <p
                            className={`${
                              isError(errors.password) ? "" : "hidden"
                            } bg-red-300 text-sm text-white rounded px-1 p-[.5px] my-1 text-center`}
                          >
                            {errors.password}
                          </p>
                        </div>
                        <div>
                          <input
                            onClick={connection}
                            type="button"
                            className="button-primary input w-full font-bold"
                            value="התחבר >>"
                          />
                        </div>
                        <p className="text-secondary text-xs font-bold underline">
                          שכחת סיסמה?
                        </p>
                      </div>
                    </div>
                    {isRegisterError && (
                      <div className="mt-5 text-white bg-red-500 p-2 rounded">
                        ההרשמה נכשלה, אנא בדוק את השדות ונסה שוב.
                      </div>
                    )}
                  </div>
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
