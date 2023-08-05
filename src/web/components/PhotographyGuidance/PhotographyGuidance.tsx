import Image, { StaticImageData } from "next/image";

interface Props {
  src: StaticImageData;
  text: string;
}
const PhotographyGuidance = ({ src, text }: Props) => {
  return (
    <div className="flex flex-col justify-center items-center gap-3 mb-4">
      <Image
        src={src}
        objectFit="contain"
        width={50}
        height={50}
        alt="Map Image"
      />
      <p
        className="text-secondary text-sm text-center max-w-[150px]"
        dangerouslySetInnerHTML={{ __html: text }}
      ></p>
    </div>
  );
};

export default PhotographyGuidance;
