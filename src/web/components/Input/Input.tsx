import React from "react";

interface Props {
  text: string;
  inputName: string;
  val?: string;
  onChange: (
    e: React.FormEvent<HTMLInputElement> | React.ChangeEvent<HTMLSelectElement>
  ) => void;
  error: string;
  optional?: boolean;
}

const Input = ({ text, inputName, val, onChange, error, optional }: Props) => {
  const isError = (p: string) => {
    const isError: boolean = p.length > 1;
    return isError;
  };

  return (
    <div className="flex flex-col">
      <p className="text-sm text-secondary font-bold mb-2">
        {text}&nbsp;
        {optional && <span className="text-xs text-gray-400">(אופציונלי)</span>}
      </p>
      <input
        className="input w-full"
        name={inputName}
        value={val}
        onChange={onChange}
      />
      <p
        className={`${
          isError(error) ? "" : "hidden"
        } bg-red-300 text-sm text-white rounded px-1 p-[.5px] my-1 text-center`}
      >
        {error}
      </p>
    </div>
  );
};

export default Input;
