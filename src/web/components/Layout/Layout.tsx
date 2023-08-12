import React from "react";
import Footer from "../Footer/Footer";
import Header from "../Header/Header";

type Props = {
  children?: JSX.Element;
};

const Layout = ({ children }: Props) => {
  return (
    <div className="flex flex-col min-h-[100vh]">
      <Header />
      <div className="grow px-4">{children}</div>
      <Footer />
    </div>
  );
};

export default Layout;
