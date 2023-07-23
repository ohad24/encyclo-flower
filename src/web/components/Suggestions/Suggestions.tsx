import React, { useEffect, useState } from "react";
import { IQuestion, IObservations } from "helpers/interfaces";
import { getAll } from "services/flowersService";
import Images from "components/Images/Images";
import Router, { useRouter } from "next/router";
import { useDispatch } from "react-redux";
import { UpdateIsQuestion, UpdateQuestion } from "redux/action";

const Suggestions = (props: {
  question: IQuestion | IObservations;
  isQuestion: boolean;
  str: string;
  username?: string;
}) => {
  const [images, setImages] = useState<any[]>([]);
  const dispatch = useDispatch();
  useEffect(() => {
    async function getData() {
      try {
        const question = (
          await getAll(
            `community/${
              "question_id" in props.question
                ? `questions/${props.question.question_id}`
                : `observations/${props.question.observation_id}`
            }`
          )
        ).data;
        setImages(question.images);
      } catch (err) {
        console.log(err);
      }
    }
    getData();
  }, [dispatch, props.question]);

  const getDate = () => {
    return (
      props.question.created_dt.slice(8, 10) +
      "." +
      props.question.created_dt.slice(5, 7) +
      "." +
      props.question.created_dt.slice(0, 4)
    );
  };

  const nextPage = () => {
    dispatch(
      UpdateQuestion({
        ...props.question,
        location_name: images[0].location_name,
        images: images,
      })
    );
    dispatch(UpdateIsQuestion(props.isQuestion));
    Router.push({
      pathname: "/sharesFromTheCommunity",
    });
  };
  return (
    <div
      className="bg-gray-100 rounded shadow hover:shadow-lg hover:bg-white relative transition duration-100 p-2 mb-8 w-[100%] sm:w-[80%]"
      onClick={nextPage}
    >
      <div className="flex flex-col xl:flex-row p-2">
        <div className="basis-1/2">
          <div className="flex flex-row flex-wrap w-[100%]">
            <p className="text-orange-300 font-medium	 mb-1 text-lg">
              {props.username
                ? props.username
                : props.question !== undefined
                ? props.question.username
                : null}
            </p>
            <p
              className="text-xs text-gray-400 m-auto"
              style={{ direction: "ltr" }}
            >
              {getDate()}
            </p>
          </div>
          <p className="text-secondary text-base font-medium">
            {props.question !== undefined
              ? props.question[`${props.str}` as keyof typeof props.question]
              : null}
          </p>
        </div>

        <div className="flex flex-wrap basis-1/2 max-w-[100%] xl:max-w-[750px]">
          <div className="xl:mr-auto max-w-[100%]">
            <Images
              username={props.question.username}
              photos={images}
              width={520}
              imageFromTheUser={true}
              isQuestion={props.isQuestion}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Suggestions;
