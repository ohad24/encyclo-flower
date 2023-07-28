import {
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalOverlay,
} from "@chakra-ui/react";
import Image from "next/image";
import React from "react";
import helpImage1 from "../../images/ai_help_1.png";
import helpImage2 from "../../images/ai_help_2.png";
import helpImage3 from "../../images/ai_help_3.png";

const ModalDirective = (props: {
  isOpen: boolean;
  setIsOpen: (bool: boolean) => void;
}) => {
  return (
    <Modal
      isCentered
      isOpen={props.isOpen}
      onClose={() => props.setIsOpen(false)}
      size="2xl"
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
          <div className="flex flex-col md:flex-row  md:justify-around p-4 ">
            <div className="flex flex-col  justify-center items-center gap-3 mb-4">
              <Image
                src={helpImage1}
                objectFit="contain"
                width={50}
                height={50}
                alt="Map Image"
              />
              <p className="text-secondary text-sm text-center  max-w-[150px]">
                כדאי לצלם את הפרח, <br />
                מקרוב ובפוקוס
              </p>
            </div>
            <div className="flex flex-col justify-center items-center  gap-3 mb-4">
              <Image
                src={helpImage2}
                objectFit="contain"
                width={50}
                height={50}
                alt="Map Image"
              />
              <p className="text-secondary text-sm text-center max-w-[150px]">
                אם אין פרח:
                <br />
                אפשר לצלם את העלים מקרוב.
              </p>
            </div>
            <div className="flex flex-col justify-center items-center gap-3 mb-4">
              <Image
                src={helpImage3}
                objectFit="contain"
                width={50}
                height={50}
                alt="Map Image"
              />
              <p className="text-secondary text-sm text-center max-w-[150px]">
                ממולץ לשמור על תאורה אחידה (שמש או צל אחיד בכל תמונה)
              </p>
            </div>
          </div>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
};

export default ModalDirective;
