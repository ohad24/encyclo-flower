import React from "react";

interface Props {
  color?: string;
  size?: number;
}

const NextIcon = ({ color = "#", size = 16 }: Props) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      className="svg-icon mr-2 mt-3.5 font-bold"
      viewBox="0 0 1028 1024"
      version="1.1"
      width={size}
      height={size}
      overflow="hidden"
      transform="rotate(90)"
    >
      <path
        fill={color}
        d="M512 968.5c-7 0-13.8-3.4-19.1-10.3L123.5 479.8c-11.2-14.4-11-38.4 0.9-51.8 10.6-12 26.7-11.4 36.8 1.7l331.2 429c10.8 14 28.3 14 39.1 0l330.8-428.4c11.2-14.4 29.6-14.2 40 1.2 9.3 13.8 8.8 34.6-1.3 47.7l-369.9 479c-5.2 6.9-12.1 10.3-19.1 10.3z"
      />
      <path
        fill={color}
        d="M512 604.5c-7 0-13.8-3.4-19.1-10.3L123.5 115.8c-11.2-14.4-11-38.4 0.9-51.8 10.6-12 26.7-11.4 36.8 1.7l331.2 429c10.8 14 28.3 14 39.1 0L862.9 65.8c10.1-13.1 26.2-13.7 36.8-1.7 11.9 13.4 12.1 37.3 0.9 51.8L531.2 594.3c-5.3 6.8-12.2 10.2-19.2 10.2z"
      />
    </svg>
  );
};

export default NextIcon;

/*


        */
