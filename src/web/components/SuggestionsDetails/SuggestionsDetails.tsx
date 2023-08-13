import React from "react";

interface Props {
  username?: string;
  question: any;
  str: string;
}

const SuggestionsDetails = ({ username, question, str }: Props) => {
  const getDate = () => {
    return (
      question.created_dt.slice(8, 10) +
      "." +
      question.created_dt.slice(5, 7) +
      "." +
      question.created_dt.slice(0, 4)
    );
  };
  return (
    <div className="basis-1/2">
      <div className="flex flex-row flex-wrap w-[100%]">
        <p className="text-orange-300 font-medium mb-1 text-lg">
          {username
            ? username
            : question !== undefined
            ? question.username
            : null}
        </p>
        <p className="text-xs text-gray-400 m-auto">{getDate()}</p>
      </div>
      <p className="text-secondary text-base font-medium">
        {question !== undefined
          ? question[`${str}` as keyof typeof question]
          : null}
      </p>
    </div>
  );
};

export default SuggestionsDetails;
