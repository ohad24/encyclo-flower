import React from "react";
import Image from "next/image";
import logo from "../../images/logo.png";
import Router, { useRouter } from "next/router";
import footerImage from "../../images/footer.png";

const Footer = () => {
  const nextPage = () => {
    Router.push({
      pathname: "/termsOfUse",
    });
  };
  return (
    <div className="h-[200px] relative flex mt-3 md:mt-16">
      <Image src={footerImage} alt="footer" objectFit="fill" layout="fill" />
      <div className="text-center w-[100%]  text-white text-sm pb-1 inset-x-0 bottom-0 absolute">
        כל הזכויות שמורות – אנציקלופרח |{" "}
        <button onClick={nextPage}> תנאי שימוש </button> |{" "}
        <Image src={logo} alt="Logo" width={66.13} height={34} />
      </div>
    </div>
  );
};

export default Footer;
/*

<div className="text-center w-[100%]  text-white text-sm pb-1 top-full absolute">
        כל הזכויות שמורות – אנציקלופרח |{" "}
        <button onClick={nextPage}> תנאי שימוש </button> |{" "}
        <Image src={logo} alt="Logo" width={66.13} height={34} />
      </div>
  */
