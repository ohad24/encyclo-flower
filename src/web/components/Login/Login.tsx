import ResetPassword from "components/ResetPassword/ResetPassword";
import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { UpdateToken } from "redux/action";
import { post } from "services/flowersService";

interface Props {
  onClose: () => void;
}

interface User {
  username: string;
  password: string;
}

const initialUser: User = {
  username: "",
  password: "",
};

const Login = ({ onClose }: Props) => {
  const [isRegisterError, setIsRegisterError] = useState(false);
  const [user, setUser] = useState<User>(initialUser);
  const [email, setEmail] = useState<string>("");
  const [isForgot, setIsForgot] = useState<boolean>(false);
  const dispatch = useDispatch();
  const [errors, setErrors] = useState({
    ...initialUser,
    accept_terms_of_service: true,
  });

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
      const { data } = await post("token", user);
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

  if (isForgot) return <ResetPassword />;

  return (
    <div className="flex flex-col items-center justify-center overflow-hidden">
      <div>
        <div className="flex flex-col gap-4 w-[200px] md:w-[300px]">
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
          <p
            className="text-secondary text-xs font-bold underline cursor-pointer"
            onClick={() => setIsForgot(true)}
          >
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
  );
};

export default Login;
