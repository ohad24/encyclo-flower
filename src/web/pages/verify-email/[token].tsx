import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Layout from "components/Layout/Layout";
import { verifyEmail } from "services/flowersService";

const VerifyEmail = () => {
  const [message, setMessage] = useState<string>("");

  const router = useRouter();
  useEffect(() => {
    async function verify() {
      try {
        const response = await verifyEmail(
          `users/verify-email/${router.query.token}`
        );
        response.status === 204
          ? setMessage("ההרשמה הצליחה")
          : setMessage("ההרשמה נכשלה");
      } catch (err) {
        console.log(err);
        setMessage("ההרשמה נכשלה");
      }
    }
    verify();
  }, [router.query.token]);
  return (
    <Layout>
      <div className="default-container">
        <div className="text-secondary font-bold m-auto text-center text-3xl">
          {message}
        </div>
      </div>
    </Layout>
  );
};

export default VerifyEmail;
