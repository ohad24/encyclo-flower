import { create, get } from "services/flowersService";
import { useSelector } from "react-redux";
import React, { useState } from "react";

interface Props {
  setComments: React.Dispatch<React.SetStateAction<string[]>>;
}

const FormComment = ({ setComments }: Props) => {
  const store = useSelector((state: any) => state);
  const [yourComment, setYourComment] = useState<string>("");
  const sendComment = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      await create(
        store.isQuestion
          ? `community/questions/${store.question.question_id}/comments`
          : `community/observations/${store.question.observation_id}/comment`,
        {
          comment_text: yourComment,
        },
        store.token
      );
      await getComments();
      setYourComment("");
    } catch (err) {
      console.log(err);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    setYourComment(value);
  };

  const getComments = async () => {
    try {
      const data = (
        await get(
          store.isQuestion
            ? `community/questions/${store.question.question_id}/comments`
            : `community/observations/${store.question.observation_id}/comments`
        )
      ).data;
      setComments(
        data.sort(
          (a: any, b: any) =>
            new Date(b.create_dt).getTime() - new Date(a.create_dt).getTime()
        )
      );
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <form
      onSubmit={sendComment}
      className="flex flex-row max-w-[453px] h-[32px] rounded-2xl bg-neutral-200"
    >
      <div className="w-[12px] h-[12px] bg-orange-400 rounded-full mt-3 mr-3 "></div>
      <input
        type="text"
        placeholder="התגובה שלך..."
        value={yourComment}
        onChange={handleChange}
        required
        className="w-[453px] h-[32px] rounded-2xl bg-neutral-200 border-transparent focus:outline-0 pr-2"
      />
      <button type="submit">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth="1.5"
          stroke="rgb(12 74 110)"
          className="h-8 w-8"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M11.25 9l-3 3m0 0l3 3m-3-3h7.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      </button>
    </form>
  );
};

export default FormComment;
