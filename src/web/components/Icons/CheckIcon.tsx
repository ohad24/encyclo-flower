import React from "react";
interface Props {
  size?: number;
  color?: string;
}

const CheckIcon = ({ size = 32, color = "#" }: Props) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      id="check"
      height={size}
      width={size - 2}
      fill={color}
    >
      <path fill="none" d="M0 0h24v24H0V0z" />
      <path d="M9 16.17L5.53 12.7c-.39-.39-1.02-.39-1.41 0-.39.39-.39 1.02 0 1.41l4.18 4.18c.39.39 1.02.39 1.41 0L20.29 7.71c.39-.39.39-1.02 0-1.41-.39-.39-1.02-.39-1.41 0L9 16.17z" />
    </svg>
  );
};

export default CheckIcon;
