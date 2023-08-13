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

const LeftButton = ({ handleHorizantalScroll, elementRef }: Props) => {
  return (
    <button
      className="top-[90px] sm:top-[141px] absolute flex w-[20px] h-[20px] rounded-full font-bold pl-0 left-0"
      onClick={(e) => {
        handleHorizantalScroll(e, elementRef.current, 25, 100, -10);
      }}
      style={{
        background: "rgba(240,240,240,0.8)",
        justifyContent: "space-between",
        fontSize: "17px",
      }}
    >
      <div className="relative w-[20px] h-[20px] rounded-full bottom-1">
        {">"}
      </div>
    </button>
  );
};

export default LeftButton;
