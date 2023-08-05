import React from "react";
import "../../styles/QuestionCommunity.module.css";
import { useSelector } from "react-redux";
import { putWithAuthorization } from "services/flowersService";
import { monthsText } from "helpers/globalObjects";
import Image from "components/Image/Image";
import SelectPicture from "components/Selects/SelectPicture";
import SelectLocation from "components/Selects/SelectLocation";
import Month from "components/Selects/Month";

const ImageFromQuestion = (props: {
  index: number;
  image: any;
  images: Array<any>;
  setImages: (arrIds: Array<any>) => void;
}) => {
  const store = useSelector((state: any) => state);
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
        await putWithAuthorization(
          `${path}/image/${props.image.image_id}`,
          obj,
          store.token
        );
      } catch (err) {
        console.log(err);
      }
    }
  };

  return (
    <div key={props.index} className="w-[100%] md:max-w-[371px] ">
      <div className="flex flex-row flex-wrap w-[100%] m-auto mb-0 gap-5 items-center">
        <Image
          path={path}
          index={props.index}
          image={props.image}
          images={props.images}
          setImages={props.setImages}
        />
        <div className="mb-5 w-[100%] sm:w-[155px]">
          <SelectPicture
            updateDataImage={updateDataImage}
            handleChange={handleChange}
          />
          <SelectLocation
            updateDataImage={updateDataImage}
            handleChange={handleChange}
          />
          <Month
            updateDataImage={updateDataImage}
            handleChange={handleChange}
            dataImage={dataImage}
          />
        </div>
      </div>
      <input
        className="relative p-2 mt-2 w-[100%] min-h-[60px] caret-color: #60a5fa inputQuestion placeholder-sky-900 text-sky-900 pb-9 rounded-3xl"
        name="description"
        id="description"
        placeholder="הסבר והערות"
        onBlur={updateDataImage}
        onChange={handleChange}
        value={dataImage.description ? dataImage.description : ""}
        style={{
          backgroundColor: "rgb(229 231 235)",
          borderRadius: "35px",
        }}
      />
    </div>
  );
};

export default ImageFromQuestion;
