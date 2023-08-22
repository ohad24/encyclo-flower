import React, { useEffect, useState } from "react";
import Link from "next/link";
import Cookies from "universal-cookie";
import MenuIcon from "../MenuIcon/Menu";
import LoginAndRegisterModel from "../LoginAndRegisterModel/LoginAndRegisterModel";

import { nanoid } from "nanoid";
import Router from "next/router";

// Icons components
import ModalLogin from "components/Modals/ModalLogin";
import Logo from "components/Logo/Logo";
import Supports from "components/Supports/Supports";
import Notifications from "components/Notifications/Notifications";
import LoginOrRegister from "components/LoginOrRegister/LoginOrRegister";
import { useSelector } from "react-redux";
import ModalLoginMessage from "components/Modals/ModalLoginMessage";

const cookies = new Cookies();
const menuItems = [
  { text: "בית", url: "/" },
  { text: "זיהוי צמח", url: "/ai" },
  { text: "חיפוש צמח", url: "/search" },
  { text: "שאלות מהקהילה", url: "/questionFromTheCommunity" },
  { text: " פרסומים ותצפיות", url: "/shares" },
  { text: "תומכים", url: "/support" },
  { text: "כתבו לנו", url: "/writeToUs" },
  { text: "אודות", url: "/about" },
  { text: "הפרופיל שלי", url: "/myProfile" },
];

const Header = () => {
  const store = useSelector((state: any) => state);
  const [isOpen, setIsOpen] = React.useState(false);
  const [isOpenMessage, setIsOpenMessage] = React.useState(false);
  const [menuId, setMenuId] = useState(0);
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const handleMenuId = (id: number) => {
    setMenuId(id);
    cookies.set("menuId", id, { path: "/" });
  };

  useEffect(() => {
    const menuCookie = cookies.get("menuId");
    if (!menuCookie) {
      console.log("undefiend");
    } else {
      setMenuId(Number(menuCookie));
    }
  }, []);

  const showMessage = (item: any) => {
    if (item.text === "הפרופיל שלי") {
      setIsOpenMessage(true);
    }
  };

  const renderMenu = (isSeperator: boolean) => {
    return (
      <>
        {menuItems.map((item, index) => {
          return (
            <div key={nanoid()} className="flex flex-row gap-2">
              <div
                onClick={
                  store.token
                    ? () => handleMenuId(index)
                    : () => showMessage(item)
                }
                className={`${
                  menuId === index ? "text-primary" : ""
                } cursor-pointer ${
                  !isSeperator
                    ? "border-2 border-transparent border-b-orange-100 w-full text-center p-1 pb-3"
                    : null
                }`}
              >
                <Link
                  href={
                    !store.token && item.text === "הפרופיל שלי"
                      ? ""
                      : `${item.url}`
                  }
                >
                  {item.text}
                </Link>
              </div>
              {isSeperator ? <div>|</div> : ""}
            </div>
          );
        })}
      </>
    );
  };

  const nextPage = (path: string) => {
    Router.push({
      pathname: path,
    });
  };

  return (
    <header className="flex flex-col gap-4 default-container pb-2">
      <div className="flex items-center flex-row-reverse">
        <Supports nextPage={nextPage} />
        <Logo />
        <div className="flex flex-col items-center justify-center p-2 md:p-4 ">
          <div className="flex gap-2 md:gap-5 align-center justify-center flex-row-reverse">
            <Notifications />
            <LoginOrRegister setIsLoginOpen={setIsLoginOpen} />
            <div className="md:hidden" onClick={() => setIsOpen(true)}>
              <MenuIcon />
            </div>
          </div>
        </div>
      </div>
      <nav className=" gap-2 text-sm px-2 md:px-4 justify-center hidden md:flex">
        {renderMenu(true)}
      </nav>
      <LoginAndRegisterModel
        isOpen={isLoginOpen}
        onClose={() => {
          setIsLoginOpen(false);
        }}
      />
      <ModalLogin
        isOpen={isOpen}
        setIsOpen={setIsOpen}
        renderMenu={renderMenu}
      />
      <ModalLoginMessage isOpen={isOpenMessage} setIsOpen={setIsOpenMessage} />
    </header>
  );
};

export default Header;
