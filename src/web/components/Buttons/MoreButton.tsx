import React from "react";

interface Props {
  nextPage: (path: string) => void;
  path: string;
  text: string;
}

const MoreButton = ({ nextPage, path, text }: Props) => {
  return (
    <button
      className="text-white text-xl font-medium bg-sky-800 w-[200px] h-[40px] rounded"
      onClick={() => nextPage(path)}
    >
      {text}
    </button>
  );
};

export default MoreButton;
