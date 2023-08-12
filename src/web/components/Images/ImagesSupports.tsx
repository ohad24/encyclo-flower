import Image from "next/image";
import support1 from "../../images/support-1.png";
import support2 from "../../images/support-2.jpg";
import support3 from "../../images/support-3.jpg";

const ImagesSupports = () => {
  return (
    <div className="flex flex-col md:flex-row items-center md:justify-center  gap-[1.6rem] md:gap-[4.5rem]   min-h-[310px] md:min-h-[170px]">
      <div>
        <Image
          width="280px"
          height="92.14px"
          src={support1}
          alt="support kkl "
        />
      </div>
      <div>
        <Image
          width="280px"
          height="118.69px"
          src={support2}
          alt="support kkl "
        />
      </div>
      <div>
        <Image width="280px" height="157px" src={support3} alt="support 2 " />
      </div>
    </div>
  );
};
export default ImagesSupports;
