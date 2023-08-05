import React from "react";

interface Props {
  updateDataImage: () => Promise<void>;
  handleChange: (
    e:
      | React.ChangeEvent<HTMLSelectElement>
      | React.ChangeEvent<HTMLInputElement>
  ) => void;
}

const SelectPicture = ({ updateDataImage, handleChange }: Props) => {
  return (
    <select
      id="countries"
      name="content_category"
      onBlur={updateDataImage}
      onChange={handleChange}
      defaultValue={"default"}
      required
      className="mb-4 w-[100%] sm:w-[155px] h-[32px] caret-color: #60a5fa inputQuestion placeholder-sky-900 text-sky-900 rounded-3xl text-center font-medium pb-0.5"
      style={{
        backgroundColor: "#ffa255",
        filter: "drop-shadow(2.728px 2.925px 10.5px rgba(249,189,56,0.73))",
        backgroundImage: "linear-gradient(135deg, #f58f3b 0%, #f9bd38 100%)",
      }}
    >
      <option value="default" hidden>
        מה בתמונה?
      </option>
      <option value="הצמח במלואו">הצמח במלואו</option>
      <option value="פרי">פרי</option>
      <option value="פרח">פרח</option>
      <option value="עלים">עלים</option>
      <option value="זרעים">זרעים</option>
      <option value="פרח בבית הגידול"> פרח בבית הגידול</option>
    </select>
  );
};

export default SelectPicture;
