import { useRef, useState } from "react";
import { useDispatch } from "react-redux";
import ModalImage from "components/Modals/ModalImage";
import { UpdatePlantName, UpdateUserName } from "redux/action";
import RightButton from "components/Buttons/RightButton";
import LeftButton from "components/Buttons/LeftButton";
import ImageComp from "components/ImageComp/ImageComp";
import React from "react";

interface Props {
  username?: string;
  plantName?: string;
  photos: any;
  width: number;
  isQuestion?: boolean;
  imagesDetections?: boolean;
  imageFromTheUser: boolean;
}

const Images = ({
  username,
  plantName,
  photos,
  isQuestion,
  imagesDetections,
  imageFromTheUser,
}: Props) => {
  const dispatch = useDispatch();
  const [isImageOpen, setIsImageOpen] = useState<boolean>(false);
  const [chooseImage, setChooseImage] = useState<any>("");
  const elementRef = useRef(null);
  const [arrowDisable, setArrowDisable] = useState(true);

  const handleHorizantalScroll = (
    e: React.MouseEvent<HTMLButtonElement>,
    element: HTMLElement | null,
    speed: number,
    distance: number,
    step: number
  ) => {
    e.stopPropagation();
    let scrollAmount = 0;
    const slideTimer = setInterval(() => {
      if (element !== null) {
        element.scrollLeft += step;
        scrollAmount += Math.abs(step);
        if (scrollAmount >= distance) {
          clearInterval(slideTimer);
        }
        if (element.scrollLeft === 0) {
          setArrowDisable(true);
        } else {
          setArrowDisable(false);
        }
      }
    }, speed);
  };

  const clickImage = (
    e: React.MouseEvent<HTMLDivElement>,
    image: any,
    i: number
  ) => {
    e.stopPropagation();
    setIsImageOpen(true);
    setChooseImage({
      ...image,
      url: !imagesDetections
        ? imageFromTheUser
          ? isQuestion
            ? `${process.env.IMAGE_USER_BASE_URL}/questions/${image.file_name}`
            : `${process.env.IMAGE_USER_BASE_URL}/observations/${image.file_name}`
          : `${process.env.IMAGE_BASE_URL}/plants-images/images/${
              typeof photos[i] === "string" ? photos[i] : photos[i].file_name
            }`
        : `${process.env.IMAGE_USER_BASE_URL}/image_api_files/${image.file_name}`,
    });
    dispatch(UpdateUserName(username || ""));
    dispatch(UpdatePlantName(plantName));
  };

  const showButtonRight = !arrowDisable ? (
    <RightButton
      handleHorizantalScroll={handleHorizantalScroll}
      elementRef={elementRef}
    />
  ) : null;

  const rightOrLeft = photos ? (
    photos.length > 0 ? (
      <div>
        {showButtonRight}
        <LeftButton
          handleHorizantalScroll={handleHorizantalScroll}
          elementRef={elementRef}
        />
      </div>
    ) : null
  ) : null;

  const showImages = photos
    ? photos.map((image: any, i: number) => (
        <ImageComp
          key={image.file_name}
          image={image}
          i={i}
          clickImage={clickImage}
          photos={photos}
          imageFromTheUser={imageFromTheUser}
          imagesDetections={imagesDetections}
          isQuestion={isQuestion}
          username={username}
        />
      ))
    : null;

  return (
    <div className="relative flex flex-row items-center text-secondary mt-2 w-[100%]">
      {" "}
      <div className="flex flex-row gap-2.5 max-w-[100%]">
        {rightOrLeft}
        <div
          className="flex flex-row items-start gap-3 text-secondary max-w-[100%] overflow-x-scroll hide-scrollbar"
          ref={elementRef}
        >
          {" "}
          {showImages}
        </div>
      </div>
      <ModalImage
        isImageOpen={isImageOpen}
        setIsImageOpen={setIsImageOpen}
        image={chooseImage}
        imageFromTheUser={imageFromTheUser}
      />
    </div>
  );
};
export default Images;
