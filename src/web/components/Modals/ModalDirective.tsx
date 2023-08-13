import {
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalOverlay,
} from "@chakra-ui/react";
import React from "react";
import helpImage1 from "../../images/ai_help_1.png";
import helpImage2 from "../../images/ai_help_2.png";
import helpImage3 from "../../images/ai_help_3.png";
import PhotographyGuidance from "components/PhotographyGuidance/PhotographyGuidance";

interface Props {
  isOpen: boolean;
  setIsOpen: (bool: boolean) => void;
}

const ModalDirective = ({ isOpen, setIsOpen }: Props) => {
  return (
    <Modal
      isCentered
      isOpen={isOpen}
      onClose={() => setIsOpen(false)}
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
            <PhotographyGuidance
              src={helpImage1}
              text={"כדאי לצלם את הפרח, <br /> מקרוב ובפוקוס"}
            />
            <PhotographyGuidance
              src={helpImage2}
              text={"אם אין פרח:<br /> אפשר לצלם את העלים מקרוב."}
            />
            <PhotographyGuidance
              src={helpImage3}
              text={"ממולץ לשמור על תאורה אחידה (שמש או צל אחיד בכל תמונה)"}
            />
          </div>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
};

export default ModalDirective;
