import React from "react";
import { Select } from "@chakra-ui/react";

interface Props {
  onChange: (
    e: React.FormEvent<HTMLInputElement> | React.ChangeEvent<HTMLSelectElement>
  ) => void;
  error: string;
}

const SelectGender = ({ onChange, error }: Props) => {
  const isError = (p: string) => {
    const isError: boolean = p.length > 1;
    return isError;
  };
  return (
    <div className="flex flex-col">
      <p className="text-sm text-secondary font-bold mb-2">מגדר&nbsp;</p>
      <Select name="sex" onChange={onChange}>
        <option value="0">-- בחר מגדר --</option>
        <option value="זכר">זכר</option>
        <option value="נקבה">נקבה</option>
      </Select>
      <p
        className={`${
          isError(error) ? "" : "hidden"
        }bg-red-300 text-sm text-white rounded px-1 p-[.5px] my-1 text-center`}
      >
        {error}
      </p>
    </div>
  );
};

export default SelectGender;
