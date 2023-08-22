import { useDispatch, useSelector } from "react-redux";
import Image from "next/image";
import account from "../../images/account.png";
import LogoutIcon from "components/Icons/LogoutIcon";
import { UpdateToken } from "redux/action";
import Router from "next/router";

interface Props {
  setIsLoginOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

const LoginOrRegister = ({ setIsLoginOpen }: Props) => {
  const store = useSelector((state: any) => state);
  const dispatch = useDispatch();

  const logout = () => {
    dispatch(UpdateToken(""));
    nextPage("/");
  };

  const nextPage = (path: string) => {
    Router.push({
      pathname: path,
    });
  };

  const isLogin = store.token ? (
    <div onClick={logout}>
      <LogoutIcon color="orange" size={24.8} />
    </div>
  ) : null;

  return (
    <div className="flex flex-row flex-wrap">
      {isLogin}
      <div
        className=" flex flex-col justify-center items-center cursor-pointer"
        onClick={() => setIsLoginOpen(store.token ? false : true)}
      >
        <div>
          <Image src={account} alt="Logo" />
        </div>
        {store.token ? (
          <div className="hidden md:block text-xs">מחובר</div>
        ) : (
          <div className="hidden md:block text-xs">התחבר \ הירשם</div>
        )}
      </div>
    </div>
  );
};

export default LoginOrRegister;
