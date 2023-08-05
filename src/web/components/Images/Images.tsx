import { useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import ModalImage from "components/Modals/ModalImage";
import { UpdatePlantName, UpdateUserName } from "redux/action";
import RightButton from "components/Buttons/RightButton";
import LeftButton from "components/Buttons/LeftButton";
import ImageComp from "components/ImageComp/ImageComp";
import React from "react";

const Images = (props: {
  username?: string;
  plantName?: string;
  photos: any;
  width: number;
  isQuestion?: boolean;
  imagesDetections?: boolean;
  imageFromTheUser: boolean;
}) => {
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
      url: !props.imagesDetections
        ? props.imageFromTheUser
          ? props.isQuestion
            ? `https://storage.googleapis.com/ef-dev-fe/questions/${image.file_name}`
            : `https://storage.googleapis.com/ef-dev-fe/observations/${image.file_name}`
          : `https://storage.googleapis.com/ef-prod/plants-images/images/${
              typeof props.photos[i] === "string"
                ? props.photos[i]
                : props.photos[i].file_name
            }`
        : `https://storage.googleapis.com/ef-dev-fe/image_api_files/${image.file_name}`,
    });
    dispatch(UpdateUserName(props.username || ""));
    dispatch(UpdatePlantName(props.plantName));
  };

  const showButtonRight = !arrowDisable ? (
    <RightButton
      handleHorizantalScroll={handleHorizantalScroll}
      elementRef={elementRef}
    />
  ) : null;

  const rightOrLeft =
    props.photos.length > 0 ? (
      <div>
        {showButtonRight}
        <LeftButton
          handleHorizantalScroll={handleHorizantalScroll}
          elementRef={elementRef}
        />
      </div>
    ) : null;

  const showImages = props.photos.map((image: any, i: number) => (
    <ImageComp
      key={image.file_name}
      image={image}
      i={i}
      clickImage={clickImage}
      photos={props.photos}
      imageFromTheUser={props.imageFromTheUser}
      imagesDetections={props.imagesDetections}
      isQuestion={props.isQuestion}
      username={props.username}
    />
  ));

  return (
    <div className="relative flex flex-row items-center text-secondary mt-2 w-[100%]	">
      <div className="flex flex-row gap-2.5 max-w-[100%]">
        {rightOrLeft}
        <div
          className="flex flex-row items-start gap-3 text-secondary max-w-[100%] overflow-hidden"
          ref={elementRef}
        >
          {showImages}
        </div>
      </div>
      <ModalImage
        isImageOpen={isImageOpen}
        setIsImageOpen={setIsImageOpen}
        image={chooseImage}
        imageFromTheUser={props.imageFromTheUser}
      />
    </div>
  );
};
export default Images;
