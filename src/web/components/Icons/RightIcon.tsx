import React from "react";

type Props = {
  color?: string;
  size?: number;
};

const RightIcon = ({ color = "#0f4871", size = 16 }: Props) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      shape-rendering="geometricPrecision"
      text-rendering="geometricPrecision"
      image-rendering="optimizeQuality"
      fill-rule="evenodd"
      clip-rule="evenodd"
      viewBox="0 0 500 511.61"
      height={size}
      width={size}
    >
      <path
        fill={color}
        fill-rule="nonzero"
        d="M265.959 363.223l15.5-101.271c-45.53 4.53-96.071 15.77-138.721 45.89-47.721 33.69-86.321 91.711-98.251 191.802-.87 7.43-7.62 12.75-15.06 11.87-5.73-.68-10.21-4.86-11.55-10.14-10.881-32.61-16.461-63.42-17.631-92.34-3.27-79.401 26.391-144.222 70.181-193.612 43.36-48.921 100.661-82.641 153.321-100.331 20.181-6.8 39.791-11.27 57.771-13.36L266.079 15.9c-1.32-7.34 3.57-14.381 10.91-15.691 4.07-.72 8.04.46 11 2.9l207.102 171.302c5.76 4.77 6.57 13.33 1.8 19.08l-1.54 1.59-207.062 180.393c-5.64 4.92-14.22 4.319-19.14-1.321a13.534 13.534 0 01-3.191-10.93h.001z"
      />
    </svg>
  );
};

export default RightIcon;
