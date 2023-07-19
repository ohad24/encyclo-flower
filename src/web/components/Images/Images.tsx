import { useRef, useState } from "react";
import Image from "next/image";
import link from "images/link.png";
import { useDispatch, useSelector } from "react-redux";
import ModalImage from "components/Modals/ModalImage";
import { UpdatePlantName, UpdateUserName } from "redux/action";

const Images = (props: {
  username?: string;
  plantName?: string;
  photos: any;
  width: number;
  isQuestion?: boolean;
  imagesDetections?: boolean;
  imageFromTheUser: boolean;
}) => {
  const store = useSelector((state: any) => state);
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

  return (
    <div
      className="flex flex-row items-center text-secondary mt-2 w-[100%] "
      style={{
        position: "relative",
      }}
    >
      <div
        className="flex flex-row gap-2.5 max-w-[100%]"
        style={{ direction: "rtl" }}
      >
        {props.photos.length > 0 ? (
          <div>
            {!arrowDisable ? (
              <button
                onClick={(e) => {
                  handleHorizantalScroll(e, elementRef.current, 25, 100, 10);
                }}
                style={{
                  width: "20px",
                  height: "20px",
                  background: "rgba(240,240,240,0.8)",
                  borderRadius: "100%",
                  display: "flex",
                  justifyContent: "space-between",
                  position: "absolute",
                  right: "0%",
                  top: "141px",
                  fontWeight: "700",
                  fontSize: "17px",
                  paddingLeft: "2px",
                }}
              >
                <div
                  style={{
                    position: "relative",
                    width: "20px",
                    height: "20px",
                    borderRadius: "100%",
                    bottom: "4px",
                  }}
                >
                  {"<"}
                </div>
              </button>
            ) : null}
            <button
              className="top-[90px] sm:top-[141px]"
              onClick={(e) => {
                handleHorizantalScroll(e, elementRef.current, 25, 100, -10);
              }}
              style={{
                width: "20px",
                height: "20px",
                background: "rgba(240,240,240,0.8)",
                borderRadius: "100%",
                display: "flex",
                justifyContent: "space-between",
                position: "absolute",
                left: "0%",
                fontWeight: "700",
                fontSize: "17px",
                paddingLeft: "0px",
              }}
            >
              <div
                style={{
                  position: "relative",
                  width: "20px",
                  height: "20px",
                  borderRadius: "100%",
                  bottom: "4px",
                }}
              >
                {">"}
              </div>
            </button>
          </div>
        ) : null}
        <div
          className="flex flex-row items-start gap-3 text-secondary max-w-[100%]"
          ref={elementRef}
          style={{
            display: "flex",
            overflow: "hidden",
          }}
        >
          {props.photos.map((image: any, i: number) => (
            <div key={image.image_id} className="max-w-[100%]">
              <img
                className="max-w-[235px] h-[190px] sm:max-w-[360px] sm:h-[302px] rounded-2xl object-cover"
                onClick={(e) => clickImage(e, image, i)}
                key={i}
                id={image.image_id}
                loading="lazy"
                alt={undefined}
                src={
                  !props.imagesDetections
                    ? props.imageFromTheUser
                      ? props.isQuestion
                        ? `https://storage.googleapis.com/ef-dev-fe/questions/${image.file_name}`
                        : `https://storage.googleapis.com/ef-dev-fe/observations/${image.file_name}`
                      : `https://storage.googleapis.com/ef-prod/plants-images/images/${
                          typeof props.photos[i] === "string"
                            ? props.photos[i]
                            : props.photos[i].file_name
                        }`
                    : `https://storage.googleapis.com/ef-dev-fe/image_api_files/${image.file_name}`
                }
              />
              <div className="flex mt-2 ml-2 mr-2 gap-2 w-[100%] sm:max-w-[360px] ">
                <div
                  className="text-secondary text-sm ml-auto"
                  style={{ direction: "rtl" }}
                >
                  צילום:{" "}
                  {image.author_name ? image.author_name : props.username}
                </div>
                {image.author_name ? (
                  <div className="flex ml-3">
                    <a href={image.source_url_page}>
                      <div className="relative h-[16px] w-[16px] cursor-pointer">
                        <Image
                          objectFit="contain"
                          layout="fill"
                          src={link}
                          alt="example "
                        />{" "}
                      </div>
                    </a>
                  </div>
                ) : null}
              </div>
            </div>
          ))}
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
