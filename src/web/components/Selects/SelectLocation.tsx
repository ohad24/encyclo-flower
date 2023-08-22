import React from "react";

interface Props {
  updateDataImage: () => Promise<void>;
  location_name: string;
  handleChange: (
    e:
      | React.ChangeEvent<HTMLSelectElement>
      | React.ChangeEvent<HTMLInputElement>
  ) => void;
}

const SelectLocation = ({
  updateDataImage,
  handleChange,
  location_name,
}: Props) => {
  return (
    <div className="w-[100%] sm:w-[155px]">
      <select
        id="place"
        name="location_name"
        onBlur={updateDataImage}
        onChange={handleChange}
        defaultValue={location_name}
        required
        className="mb-4 w-[100%] sm:w-[155px] h-[32px] caret-color: #60a5fa inputQuestion placeholder-sky-900 text-sky-900 rounded-3xl text-center font-medium pb-0.5 appearance-none"
        style={{
          backgroundColor: "#ffa255",
          filter: "drop-shadow(2.728px 2.925px 10.5px rgba(249,189,56,0.73))",
          backgroundImage: "linear-gradient(135deg, #f58f3b 0%, #f9bd38 100%)",
        }}
      >
        <option value="default" hidden>
          מיקום
        </option>
        <option value="חוף הגליל">חוף הגליל</option>
        <option value="חוף הכרמל">חוף הכרמל</option>
        <option value="שרון">שרון</option>
        <option value="מישור החוף הדרומי">מישור החוף הדרומי</option>
        <option value="גליל עליון">גליל עליון</option>
        <option value="גליל תחתון">גליל תחתון</option>
        <option value="כרמל">כרמל</option>
        <option value="רמות מנשה">רמות מנשה</option>
        <option value="עמק יזרעאל">עמק יזרעאל</option>
        <option value="הרי שומרון">הרי שומרון</option>
        <option value="שפלת יהודה">שפלת יהודה</option>
        <option value="הרי יהודה">הרי יהודה</option>
        <option value="צפון הנגב">צפון הנגב</option>
        <option value="מערב הנגב">מערב הנגב</option>
        <option value="מרכז והר הנגב">מרכז והר הנגב</option>
        <option value="דרום הנגב">דרום הנגב</option>
        <option value="עמק החולה">עמק החולה</option>
        <option value="בקעת כינרות">בקעת כינרות</option>
        <option value="עמק בית שאן">עמק בית שאן</option>
        <option value="גלבוע">גלבוע</option>
        <option value="מדבר שומרון">מדבר שומרון</option>
        <option value="מדבר יהודה">מדבר יהודה</option>
        <option value="בקעת הירדן">בקעת הירדן</option>
        <option value="בקעת ים המלח">בקעת ים המלח</option>
        <option value="ערבה">ערבה</option>
        <option value="חרמון">חרמון</option>
        <option value="גולן">גולן</option>
        <option value="גלעד">גלעד</option>
        <option value="עמון">עמון</option>
        <option value="מואב">מואב</option>
        <option value="אדום">אדום</option>
      </select>
    </div>
  );
};

export default SelectLocation;
