import React from "react";

type Props = {
  color?: string;
  size?: number;
};

const SaveIcon = ({ color = "#16a34a", size = 16 }: Props) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      xmlnsXlink="http://www.w3.org/1999/xlink"
      id="Layer_1"
      className="enable-background:new 0 0 30 30;"
      version="1.1"
      viewBox="0 0 30 30"
      xmlSpace="preserve"
      width={size}
      height={size}
    >
      <path
        fill={color}
        d="M22,4h-2v6c0,0.552-0.448,1-1,1h-9c-0.552,0-1-0.448-1-1V4H6C4.895,4,4,4.895,4,6v18c0,1.105,0.895,2,2,2h18  c1.105,0,2-0.895,2-2V8L22,4z M22,24H8v-6c0-1.105,0.895-2,2-2h10c1.105,0,2,0.895,2,2V24z"
      />
      <rect height="5" width="2" x="16" y="4" />
    </svg>
  );
};

export default SaveIcon;
