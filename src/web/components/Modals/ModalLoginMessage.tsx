import {
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalOverlay,
} from "@chakra-ui/react";
import React from "react";

interface Props {
  isOpen: boolean;
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

const ModalLoginMessage = ({ isOpen, setIsOpen }: Props) => {
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
        <ModalBody className=" m-auto text-sky-900 text-xl	">
          התחבר או הירשם כדי לבצע פעולות נוספות באתר
        </ModalBody>
      </ModalContent>
    </Modal>
  );
};

export default ModalLoginMessage;
