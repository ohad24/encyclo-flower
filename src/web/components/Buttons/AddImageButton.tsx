import { addImage } from "helpers/flowersService";
import React from "react";
import { useDispatch, useSelector } from "react-redux";

interface Props {
  questionsIds: string[];
  setQuestionsIds: React.Dispatch<React.SetStateAction<string[]>>;
}

const AddImageButton = ({ questionsIds, setQuestionsIds }: Props) => {
  const store = useSelector((state: any) => state);
  const dispatch = useDispatch();
  return (
    <button type="button" className="ml-auto mt-2 text-sky-900">
      <label htmlFor="filePicker">+ הוספת תמונה</label>
      <input
        id="filePicker"
        style={{ visibility: "hidden" }}
        type={"file"}
        className="text-secondary text-sm text-center max-w-[150px]"
        onChange={(e) =>
          addImage(e, store, questionsIds, setQuestionsIds, dispatch)
        }
        multiple={true}
      ></input>
    </button>
  );
};

export default AddImageButton;
