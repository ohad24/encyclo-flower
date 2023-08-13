import React, { useEffect, useState } from "react";
import { IQuestion, IObservations } from "helpers/interfaces";
import { get } from "services/flowersService";
import Images from "components/Images/Images";
import Router from "next/router";
import { useDispatch } from "react-redux";
import { UpdateIsQuestion, UpdateQuestion } from "redux/action";
import SuggestionsDetails from "components/SuggestionsDetails/SuggestionsDetails";

interface Props {
  question: IQuestion | IObservations;
  isQuestion: boolean;
  str: string;
  username?: string;
}

const Suggestions = ({ question, isQuestion, str, username }: Props) => {
  const [images, setImages] = useState<any[]>([]);
  const dispatch = useDispatch();
  useEffect(() => {
    async function getData() {
      try {
        const data = (
          await get(
            `community/${
              "question_id" in question
                ? `questions/${question.question_id}`
                : `observations/${question.observation_id}`
            }`
          )
        ).data;
        setImages(data.images);
      } catch (err) {
        console.log(err);
      }
    }
    getData();
  }, [dispatch, question]);

  const nextPage = () => {
    dispatch(
      UpdateQuestion({
        ...question,
        location_name: images[0].location_name,
        images: images,
      })
    );
    dispatch(UpdateIsQuestion(isQuestion));
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
        <SuggestionsDetails username={username} question={question} str={str} />
        <div className="flex flex-wrap basis-1/2 max-w-[100%] xl:max-w-[750px]">
          <div className="xl:mr-auto max-w-[100%]">
            <Images
              username={question.username}
              photos={images}
              width={520}
              imageFromTheUser={true}
              isQuestion={isQuestion}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Suggestions;
