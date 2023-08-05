import React, { useEffect, useState } from "react";
import { IQuestion, IObservations } from "helpers/interfaces";
import { get } from "services/flowersService";
import Images from "components/Images/Images";
import Router from "next/router";
import { useDispatch } from "react-redux";
import { UpdateIsQuestion, UpdateQuestion } from "redux/action";
import SuggestionsDetails from "components/SuggestionsDetails/SuggestionsDetails";

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
          await get(
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
        <SuggestionsDetails
          username={props.username}
          question={props.question}
          str={props.str}
        />
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
