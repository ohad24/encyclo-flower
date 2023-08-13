import Image from "next/image";
import heart from "../../images/heart.svg";

interface Props {
  nextPage: (path: string) => void;
}

const Supports = ({ nextPage }: Props) => {
  return (
    <div
      className="flex flex-col items-center justify-center p-2 md:p-4 w-[80px] cursor-pointer"
      onClick={() => nextPage("/support")}
    >
      <div>
        <Image src={heart} alt="Heart" />
      </div>
      <div>תומכים</div>
    </div>
  );
};

export default Supports;
