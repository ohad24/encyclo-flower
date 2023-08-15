import React, { useState } from "react";
import Input from "components/Input/Input";
import { postWithObj } from "services/flowersService";
import SelectGender from "components/Selects/SelectGender";
import ApprovalOfTerms from "components/ApprovalOfTerms/ApprovalOfTerms";

interface User {
  password: string;
  confirm_password: string;
  username: string;
  f_name: string;
  l_name: string;
  email: string;
  phone?: string;
  settlement?: string;
  sex: string;
  accept_terms_of_service?: boolean;
  isFormValid?: boolean;
}

const initialUser: User = {
  password: "",
  confirm_password: "",
  username: "",
  f_name: "",
  l_name: "",
  email: "",
  phone: "",
  settlement: "",
  sex: "",
  accept_terms_of_service: false,
};

const Register = () => {
  const [user, setUser] = useState<User>(initialUser);
  const [errors, setErrors] = useState({
    ...initialUser,
    accept_terms_of_service: true,
  });
  const [isRegisterd, setIsRegistered] = useState<boolean>(false);
  const [isRegisterError, setIsRegisterError] = useState(false);
  const onChange = (
    e: React.FormEvent<HTMLInputElement> | React.ChangeEvent<HTMLSelectElement>
  ) => {
    const name = e.currentTarget.name;
    const value = e.currentTarget.value;
    setUser({ ...user, [name]: value });
  };

  const onAcceptTerms = (e: React.ChangeEvent<HTMLInputElement>) => {
    const name = e.target.name;
    const value = e.target.checked;
    setUser({ ...user, [name]: value });
  };
  const validateForm = () => {
    let isValid: boolean = true;
    if (user.f_name.length < 1) {
      setErrors((prev) => {
        return { ...prev, f_name: "שם פרטי - חובה" };
      });
      isValid = false;
    }

    if (user.l_name.length < 1) {
      setErrors((prev) => {
        return { ...prev, l_name: "שם משפחה - חובה" };
      });
      isValid = false;
    }

    if (user.username.length < 1) {
      setErrors((prev) => {
        return { ...prev, username: "שם משתמש - חובה" };
      });
      isValid = false;
    }

    if (!isValidEmail(user.email)) {
      setErrors((prev) => {
        return { ...prev, email: 'דוא"ל לא תקני' };
      });
      isValid = false;
    }

    if (user.password.length < 1) {
      setErrors((prev) => {
        return { ...prev, password: "סיסמה - חובה" };
      });
      isValid = false;
    } else if (user.password !== user.confirm_password) {
      setErrors((prev) => {
        return { ...prev, password: "סיסמאות לא תואמות" };
      });
      isValid = false;
    }

    if (!user.accept_terms_of_service) {
      setErrors((prev) => {
        return { ...prev, accept_terms_of_service: false };
      });
      isValid = false;
    }

    if (!user.sex || user.sex === "0") {
      setErrors((prev) => {
        return { ...prev, sex: "יש לבחור מגדר." };
      });
      isValid = false;
    }

    return isValid;
  };

  const onSubmit = async () => {
    setErrors({
      ...initialUser,
      accept_terms_of_service: true,
    });

    if (!validateForm()) return;
    setIsRegisterError(false);
    try {
      await postWithObj("users/", user);
      setIsRegistered(true);
    } catch (err: any) {
      setIsRegisterError(true);
      console.log(err.response.data.error);
    }
  };

  const isError = (p: string) => {
    const isError: boolean = p.length > 1;
    return isError;
  };

  const isValidEmail = (email: string) => {
    const isValid = /\S+@\S+\.\S+/.test(email);
    return isValid;
  };

  if (isRegisterd)
    return (
      <div className="flex  flex-col justify-center items-center gap-2 text-primary shadow-sm rounded p-2 ">
        <p className="text-xl s border-2 border-transparent border-b-primary  pb-[.5px] mb-1">
          ההרשמה הושלמה בהצלחה!
        </p>
        <p>נרשמת בהצלחה, אנא אשר את אשר את המייל ששלחנו אליך לסיום ההרשמה</p>
        <p className="text-center mb-2">תודה!</p>
      </div>
    );

  return (
    <div className="flex  flex-col items-center justify-center overflow-hidden">
      <div className="flex flex-col sm:flex-row gap-1 sm:gap-4">
        <Input
          text={"שם פרטי"}
          inputName={"f_name"}
          val={user.f_name}
          onChange={onChange}
          error={errors.f_name}
        />
        <Input
          text={"שם משפחה"}
          inputName={"l_name"}
          val={user.l_name}
          onChange={onChange}
          error={errors.l_name}
        />
      </div>

      <div className="flex flex-col sm:flex-row gap-1 sm:gap-4">
        <Input
          text={"אימייל"}
          inputName={"email"}
          val={user.email}
          onChange={onChange}
          error={errors.email}
        />
        <Input
          text={"טלפון"}
          inputName={"phone"}
          val={user.phone}
          onChange={onChange}
          error={""}
          optional={true}
        />
      </div>
      <div className="flex flex-col sm:flex-row gap-1 sm:gap-4">
        <Input
          text={"שם משתמש"}
          inputName={"username"}
          val={user.username}
          onChange={onChange}
          error={errors.username}
        />
        <div className="flex flex-col sm:flex-row   gap-1 sm:gap-4">
          <Input
            text={"יישוב"}
            inputName={"settlement"}
            val={user.settlement}
            onChange={onChange}
            error={""}
            optional={true}
          />
        </div>
      </div>
      <div className="flex flex-col">
        <div className="flex flex-col sm:flex-row gap-4 w-[100%]">
          <Input
            text={"סיסמה"}
            inputName={"password"}
            val={user.password}
            onChange={onChange}
            error={""}
          />
          <Input
            text={"אימות סיסמה"}
            inputName={"confirm_password"}
            val={user.confirm_password}
            onChange={onChange}
            error={""}
          />
        </div>
        <p
          className={`${
            isError(errors.password) ? "" : "hidden"
          }bg-red-300 text-sm text-white rounded px-1 p-[.5px] my-1 text-center`}
        >
          {errors.password}
        </p>
      </div>
      <SelectGender onChange={onChange} error={errors.sex} />
      <ApprovalOfTerms
        accept_terms_of_service={user.accept_terms_of_service}
        error={errors.accept_terms_of_service}
        onAcceptTerms={onAcceptTerms}
      />
      <div className="w-full px-20 mt-6">
        <button className="button-primary w-full" onClick={onSubmit}>
          הרשם
        </button>
      </div>
      {isRegisterError && (
        <div className="mt-5 text-white bg-red-500 p-2 rounded">
          ההרשמה נכשלה, אנא בדוק את השדות ונסה שוב.
        </div>
      )}
    </div>
  );
};

export default Register;
