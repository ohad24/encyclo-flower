import ConfirmTheMail from "components/ConfirmTheEmail/ConfirmTheEmail";
import React, { useState } from "react";
import { postWithObj } from "services/flowersService";

const ResetPassword = () => {
  const [isContinue, setIsContinue] = useState<boolean>(false);
  const [email, setEmail] = useState<string>("");
  const [error, setError] = useState<string>("");

  const validateForm = () => {
    let isValid: boolean = true;
    if (!isValidEmail(email)) {
      setError("דוא''ל לא תקני");
      isValid = false;
    }

    return isValid;
  };

  const isValidEmail = (email: string) => {
    const isValid = /\S+@\S+\.\S+/.test(email);
    return isValid;
  };

  const isError = (p: string) => {
    const isError: boolean = p.length > 1;
    return isError;
  };

  const ContinueToConfirm = async () => {
    if (!validateForm()) return;
    try {
      setError("");
      await postWithObj("reset-password-request", {
        email,
      });
      setIsContinue(true);
    } catch (err) {
      console.log(err);
      setError("המייל אינו רשום באתר");
    }
  };

  if (isContinue) return <ConfirmTheMail />;

  return (
    <div className="flex flex-col overflow-hidden mb-20">
      <div className="flex flex-col gap-5 w-[200px] md:w-[300px]">
        <h2 className="text-center text-sky-900 font-bold text-xl">
          איפוס סיסמה
        </h2>
        <div>
          <input
            className="input w-full"
            type="text"
            name="email"
            placeholder="אימייל"
            onChange={(e) => setEmail(e.target.value)}
          />
          <p
            className={`${
              isError(error) ? "" : "hidden"
            } bg-red-300 text-sm text-white rounded px-1 p-[.5px] my-1 text-center`}
          >
            {error}
          </p>
        </div>
        <div>
          <input
            type="button"
            className="button-primary input w-full font-bold"
            value="המשך >>"
            onClick={ContinueToConfirm}
          />
        </div>
      </div>
    </div>
  );
};

export default ResetPassword;
