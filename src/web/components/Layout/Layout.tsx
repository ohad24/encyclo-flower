import React from "react";
import Footer from "../Footer/Footer";
import Header from "../Header/Header";

import Router, { useRouter } from "next/router";

type Props = {
  children?: JSX.Element;
};

const Layout = ({ children }: Props) => {
  const nextPage = () => {
    Router.push({
      pathname: "/termsOfUse",
    });
  };
  return (
    <div className="flex flex-col min-h-[100vh]">
      <Header />
      <div className="grow px-4">{children}</div>
      <Footer />
    </div>
  );
};

export default Layout;

/*

<div className="text-center w-[100%] bg-gray-400 text-white text-sm pb-1 ">
        כל הזכויות שמורות – אנציקלופרח |{" "}
        <button onClick={nextPage}> תנאי שימוש </button> |{" "}
        <Image src={logo} alt="Logo" width={66.13} height={34} />
      </div>

*/
