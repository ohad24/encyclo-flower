import Input from "components/Input/Input";
import React, { useState } from "react";
import { useRouter } from "next/router";
import { postWithObj } from "services/flowersService";

interface Obj {
  password: string;
  confirm_password: string;
}

const initialUser: Obj = {
  password: "",
  confirm_password: "",
};

const FormResetPassword = () => {
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

  const showSuccessfully = success ? (
    <p
      className={
        "bg-sky-300 text-sm text-white rounded px-1 p-[.5px] my-1 text-center"
      }
    >
      {"הסיסמה אופסה בהצלחה"}
    </p>
  ) : null;

  return (
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
      {showSuccessfully}
      <button className="button-primary w-full mt-2" onClick={reset}>
        אפס סיסמה
      </button>
    </div>
  );
};

export default FormResetPassword;
