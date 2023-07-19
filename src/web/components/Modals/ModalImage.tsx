import {
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalOverlay,
} from "@chakra-ui/react";
import React from "react";
import link from "images/link.png";
import { useSelector } from "react-redux";
import NextImage from "next/image";

const ModalImage = (props: {
  image: any;
  imageFromTheUser: boolean;
  isImageOpen: boolean;
  setIsImageOpen: (bool: boolean) => void;
}) => {
  const store = useSelector((state: any) => state);
  return (
    <Modal
      isCentered
      isOpen={props.isImageOpen}
      onClose={() => props.setIsImageOpen(false)}
      size="xl"
    >
      <ModalOverlay
        bg="none"
        backdropFilter="auto"
        backdropInvert="0%"
        backdropBlur="5px"
      />
      <ModalContent>
        <ModalCloseButton />
        <ModalBody className="mt-[2rem]">
          <div className="max-w-[100%]">
            <p className="text-3xl mb-2 text-sky-900 font-black	text-center	">
              {store.plantName}
            </p>
            <img
              className={`flex sm:h-[400px] md:h-[500px] w-[100%] m-auto rounded-2xl object-cover pl-2 pr-2`}
              alt={undefined}
              role="presentation"
              src={props.image.url}
            />
            <div className="flex flex-row">
              <div className="flex items-center mt-2 mb-5 ml-3 mr-3">
                <div
                  className="text-secondary text-sm ml-auto"
                  style={{ direction: "rtl" }}
                >
                  צילום:{" "}
                  {props.image.author_name
                    ? props.image.author_name
                    : store.username}
                </div>
              </div>
              {props.image.author_name ? (
                <div className="flex flex-row-reverse items-center justify-center h-[15px] mt-3 ml-3 mr-auto">
                  <a href={props.image.source_url_page}>
                    <div className="relative h-[16px] w-[16px] cursor-pointer">
                      <NextImage
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
            <p className="text-base text-sky-900 mr-2">
              {props.image.description}
            </p>
          </div>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
};

export default ModalImage;
