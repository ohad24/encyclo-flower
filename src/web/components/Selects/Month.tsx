import React from "react";
import { Input } from "@chakra-ui/react";

interface Props {
  dataImage: {
    description: any;
    content_category: any;
    location_name: any;
    month_taken: any;
  };
  updateDataImage: () => Promise<void>;
  handleChange: (
    e:
      | React.ChangeEvent<HTMLSelectElement>
      | React.ChangeEvent<HTMLInputElement>
  ) => void;
}

const Month = ({ updateDataImage, handleChange, dataImage }: Props) => {
  return (
    <div className="w-[100%] sm:w-[155px]">
      <Input
        required
        className="p-2 pb-2 mb-3 w-[100%] sm:w-[155px] h-[20px] caret-color: #60a5fa inputQuestion placeholder-sky-900 text-sky-900 text-center font-bold"
        type="date"
        id="date"
        name="month_taken"
        placeholder="תאריך"
        onBlur={updateDataImage}
        onChange={handleChange}
        value={dataImage.month_taken ? dataImage.month_taken : ""}
        style={{
          backgroundColor: "#ffa255",
          borderRadius: "32px",
          height: "32px",
          filter: "drop-shadow(2.728px 2.925px 10.5px rgba(249,189,56,0.73))",
          backgroundImage: "linear-gradient(135deg, #f58f3b 0%, #f9bd38 100%)",
        }}
      />
    </div>
  );
};

export default Month;
