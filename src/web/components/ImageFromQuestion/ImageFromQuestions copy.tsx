import React from "react";
import "../../styles/QuestionCommunity.module.css";
import { Input } from "@chakra-ui/react";
import RotateIcon from "components/Icons/CamaraIcon copy";
import { useDispatch, useSelector } from "react-redux";
import { updateImagesCommunity } from "redux/action";
import {
  deleteImage,
  rotateImageInQuestion,
  update,
} from "services/flowersService";
import { monthsText } from "helpers/globalObjects";

const ImageFromQuestion = (props: {
  index: number;
  image: any;
  images: Array<any>;
  setImages: (arrIds: Array<any>) => void;
}) => {
  const store = useSelector((state: any) => state);
  const dispatch = useDispatch();
  const [dataImage, setDataImage] = React.useState({
    description: props.image.description,
    content_category: props.image.content_category,
    location_name: props.image.location_name,
    month_taken: store.imagesCommunity[props.index].lastModifiedDate
      .toISOString()
      .slice(0, 10),
  });

  const path = store.isQuestion
    ? `community/questions/${store.questionId}`
    : `community/observations/${store.observationId}`;
  const rotateImage = async (index: number) => {
    try {
      await rotateImageInQuestion(
        `${path}/images/${props.image.image_id}/rotate`,
        store.token
      );
      const element: HTMLElement | null = document.getElementById(
        `img${index}`
      )!;
      const currentRotate = element.style.transform;
      element.style.transform = currentRotate + "rotate(90deg)";
    } catch (err) {
      console.log(err);
    }
  };

  const removeImage = async (index: number) => {
    try {
      const arr2: string[] = [...props.images];
      const img = arr2.splice(index, 1);
      await deleteImage(
        store.isQuestion
          ? `${path}/images/${props.image.image_id}`
          : `${path}/image/${props.image.image_id}`,
        store.token
      );
      props.setImages(arr2);
      const arr1: File[] = Array.from(store.imagesCommunity);
      arr1.splice(index, 1);
      dispatch(updateImagesCommunity(arr1));
    } catch (err) {
      console.log(err);
    }
  };

  const handleChange = (
    e:
      | React.ChangeEvent<HTMLSelectElement>
      | React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value } = e.target;
    const obj = { ...dataImage };
    (obj as any)[name] = value;
    setDataImage(obj);
  };

  const updateDataImage = async () => {
    let bool = false;
    for (const [key, value] of Object.entries(dataImage)) {
      if (value === "") {
        bool = true;
        break;
      }
    }
    if (!bool) {
      try {
        const obj = {
          ...dataImage,
          month_taken: monthsText[+dataImage.month_taken.slice(6, 7) - 1].name,
        };
        await update(`${path}/image/${props.image.image_id}`, obj, store.token);
      } catch (err) {
        console.log(err);
      }
    }
  };

  return (
    <div key={props.index} className="w-[100%] md:max-w-[371px] ">
      <div className="flex flex-row flex-wrap w-[100%] m-auto mb-0 gap-5 items-center">
        <div className="m-auto sm:m-0">
          <img
            id={`img${props.index}`}
            alt="undefined"
            src={
              store.isQuestion
                ? `https://storage.googleapis.com/ef-dev-fe/questions/${props.image.file_name}`
                : `https://storage.googleapis.com/ef-dev-fe/observations/${props.image.file_name}`
            }
            className="w-[196px] h-[169px] rounded-3xl m-auto md:m-0 bg-blue-100 object-cover mb-2"
          />
          <div className="flex flex-row">
            <div className="mt-3" onClick={() => rotateImage(props.index)}>
              <RotateIcon />
            </div>
            <button
              type="button"
              onClick={() => removeImage(props.index)}
              className="text-sky-900 mr-6 font-medium"
            >
              <span className="text-2xl">x</span> הסר תמונה
            </button>
          </div>
        </div>
        <div className="mb-5 w-[100%] sm:w-[155px]">
          <select
            id="countries"
            name="content_category"
            onBlur={updateDataImage}
            onChange={handleChange}
            defaultValue={"default"}
            value={
              dataImage.content_category == null
                ? ""
                : dataImage.content_category
            }
            required
            className="mb-4 w-[100%] sm:w-[155px] h-[32px] caret-color: #60a5fa inputQuestion placeholder-sky-900 text-sky-900"
            style={{
              backgroundColor: "#ffa255",
              borderRadius: "27px",
              textAlign: "center",
              fontWeight: "500",
              paddingBottom: "2px",
              filter:
                "drop-shadow(2.728px 2.925px 10.5px rgba(249,189,56,0.73))",
              backgroundImage:
                "linear-gradient(135deg, #f58f3b 0%, #f9bd38 100%)",
            }}
          >
            <option value="default" disabled>
              מה בתמונה?
            </option>
            <option value="הצמח במלואו">הצמח במלואו</option>
            <option value="פרי">פרי</option>
            <option value="פרח">פרח</option>
            <option value="עלים">עלים</option>
            <option value="זרעים">זרעים</option>
            <option value="פרח בבית הגידול"> פרח בבית הגידול</option>
          </select>
          <div className="w-[100%] sm:w-[155px]">
            <select
              id="place"
              name="location_name"
              onBlur={updateDataImage}
              onChange={handleChange}
              defaultValue={"default"}
              value={dataImage.location_name}
              required
              className=" mb-4 w-[100%] sm:w-[155px] h-[25px] caret-color: #60a5fa inputQuestion placeholder-sky-900 text-sky-900"
              style={{
                backgroundColor: "#ffa255",
                borderRadius: "27px",
                textAlign: "center",
                height: "32px",
                fontWeight: "500",
                paddingBottom: "2px",
                appearance: "none",
                filter:
                  "drop-shadow(2.728px 2.925px 10.5px rgba(249,189,56,0.73))",
                backgroundImage:
                  "linear-gradient(135deg, #f58f3b 0%, #f9bd38 100%)",
              }}
            >
              <option value="default" disabled>
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

          <div className="w-[100%] sm:w-[155px]">
            <Input
              required
              className="p-2 mb-3 w-[100%] sm:w-[155px] h-[20px] caret-color: #60a5fa inputQuestion placeholder-sky-900 text-sky-900 "
              type="date"
              id="date"
              name="month_taken"
              placeholder="תאריך"
              onBlur={updateDataImage}
              onChange={handleChange}
              value={dataImage.month_taken}
              style={{
                backgroundColor: "#ffa255",
                borderRadius: "27px",
                textAlign: "center",
                height: "32px",
                paddingBottom: "10px",
                fontWeight: "500",

                filter:
                  "drop-shadow(2.728px 2.925px 10.5px rgba(249,189,56,0.73))",
                backgroundImage:
                  "linear-gradient(135deg, #f58f3b 0%, #f9bd38 100%)",
              }}
            />
          </div>
        </div>
      </div>
      <input
        className="relative p-2 mt-2 w-[100%] min-h-[60px] caret-color: #60a5fa inputQuestion placeholder-sky-900 text-sky-900 "
        name="description"
        id="description"
        placeholder="הסבר והערות"
        onBlur={updateDataImage}
        onChange={handleChange}
        value={dataImage.description}
        style={{
          backgroundColor: "rgb(229 231 235)",
          paddingBottom: "35px",
          borderRadius: "35px",
        }}
      />
    </div>
  );
};

export default ImageFromQuestion;
