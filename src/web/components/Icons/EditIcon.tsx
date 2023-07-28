import React from "react";

type Props = {
  color?: string;
  size?: number;
};

const EditIcon = ({ color = "#0f4871", size = 16 }: Props) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      xmlnsXlink="http://www.w3.org/1999/xlink"
      id="Layer_1"
      className="enable-background:new 0 0 80 80;"
      version="1.1"
      viewBox="0 0 80 80"
      xmlSpace="preserve"
      width={size}
      height={size}
      fill={color}
    >
      <title />
      <g id="Layer_2">
        <g id="Layer_3">
          <polygon points="61.8,71.8 8.4,71.8 8.4,18.4 35.1,18.4 35.1,15.4 5.4,15.4 5.4,74.8 64.8,74.8 64.8,41.5 61.8,41.5   " />
          <path d="M22.6,46.2l-2.1,13.1l13.1-2.1l1.3-1.4l0,0l39.8-39.7L63.7,5.2L24,44.9L22.6,46.2z M25.3,48.3l6.1,6.2L24,55.7L25.3,48.3z     M70.4,16.1l-3.9,4l-6.6-6.7l4-3.9L70.4,16.1z M57.7,15.5l6.7,6.7L33.8,52.7L27.2,46L57.7,15.5z" />
        </g>
      </g>
    </svg>
  );
};

export default EditIcon;
