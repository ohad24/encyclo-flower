import React from "react";

type Props = {
  children: JSX.Element;
  cssClass?: string;
};

const Select = ({ children, cssClass = "" }: Props) => {
  return (
    <div className="w-full ">
      <select
        className={`bg-primary rounded py-1 px-1 w-full outline-none font-bold text-sm ${cssClass}`}
      >
        {children}
      </select>
    </div>
  );
};

export default Select;
