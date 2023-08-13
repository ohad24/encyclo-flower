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
  renderMenu: (isSeperator: boolean) => React.JSX.Element;
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

const ModalLogin = ({ isOpen, renderMenu, setIsOpen }: Props) => {
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
          <nav className="flex flex-col justify-center items-center gap-2 pb-8">
            {renderMenu(false)}
          </nav>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
};

export default ModalLogin;
