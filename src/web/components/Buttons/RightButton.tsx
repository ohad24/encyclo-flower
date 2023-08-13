import React, { MutableRefObject } from "react";

interface Props {
  handleHorizantalScroll: (
    e: React.MouseEvent<HTMLButtonElement>,
    element: HTMLElement | null,
    speed: number,
    distance: number,
    step: number
  ) => void;
  elementRef: MutableRefObject<null>;
}

const RightButton = ({ handleHorizantalScroll, elementRef }: Props) => {
  return (
    <button
      className="absolute flex w-[20px] h-[20px] rounded-full font-bold pl-0.5 "
      onClick={(e) => {
        handleHorizantalScroll(e, elementRef.current, 25, 100, 10);
      }}
      style={{
        background: "rgba(240,240,240,0.8)",
        justifyContent: "space-between",
        top: "141px",
        fontSize: "17px",
      }}
    >
      <div className="relative w-[20px] h-[20px] rounded-full bottom-1">
        {"<"}
      </div>
    </button>
  );
};

export default RightButton;
