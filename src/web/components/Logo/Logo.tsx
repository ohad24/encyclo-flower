import Image from "next/image";
import Link from "next/link";
import logo from "../../images/logo.png";

const Logo = () => {
  return (
    <div className="grow flex items-center justify-center cursor-pointer ">
      <Link href="/">
        <a>
          <Image src={logo} alt="Logo" priority />
        </a>
      </Link>
    </div>
  );
};

export default Logo;
