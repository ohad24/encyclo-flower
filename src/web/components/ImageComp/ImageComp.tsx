import React from "react";
import Image from "next/image";
import link from "images/link.png";

interface Props {
  image: any;
  i: number;
  imagesDetections?: boolean;
  imageFromTheUser?: boolean;
  isQuestion?: boolean;
  photos: any;
  username?: string;

  clickImage: (
    e: React.MouseEvent<HTMLDivElement>,
    image: any,
    i: number
  ) => void;
}

const ImageComp = ({
  image,
  i,
  clickImage,
  imagesDetections,
  imageFromTheUser,
  isQuestion,
  photos,
  username,
}: Props) => {
  const showSource = image.author_name ? (
    <div className="flex ml-3">
      <a href={image.source_url_page}>
        <div className="relative h-[16px] w-[16px] cursor-pointer">
          <Image objectFit="contain" layout="fill" src={link} alt="undefined" />{" "}
        </div>
      </a>
    </div>
  ) : null;

  const src = !imagesDetections
    ? imageFromTheUser
      ? isQuestion
        ? `${process.env.IMAGE_USER_BASE_URL}/questions/${image.file_name}`
        : `${process.env.IMAGE_USER_BASE_URL}/observations/${image.file_name}`
      : `${process.env.IMAGE_BASE_URL}/plants-images/images/${
          typeof photos[i] === "string" ? photos[i] : photos[i].file_name
        }`
    : `${process.env.IMAGE_USER_BASE_URL}/image_api_files/${image.file_name}`;

  const photographer = image.author_name ? image.author_name : username;

  return (
    <div className="max-w-[100%]">
      <img
        className="max-w-[235px] h-[190px] sm:max-w-[360px] sm:h-[302px] rounded-2xl object-cover"
        onClick={(e) => clickImage(e, image, i)}
        key={i}
        id={image.file_name}
        loading="lazy"
        alt="undefined"
        src={src}
      />
      <div className="flex mt-2 ml-2 mr-2 gap-2 w-[100%] sm:max-w-[360px] ">
        <div className="text-secondary text-sm ml-auto">
          צילום: {photographer}
        </div>
        {showSource}
      </div>
    </div>
  );
};

export default ImageComp;
