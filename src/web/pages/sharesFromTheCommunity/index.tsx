import Layout from "components/Layout/Layout";
import React, { useEffect, useState } from "react";
import { addComment, getAll } from "services/flowersService";
import { useSelector } from "react-redux";
import LocationIcon from "components/Icons/LocationIcon";
import Images from "components/Images/Images";
import Comment from "components/comment/comment";

const SharesCommunity = () => {
  const store = useSelector((state: any) => state);
  const [yourComment, setYourComment] = useState<string>("");
  const [comments, setComments] = useState<string[]>([]);

  useEffect(() => {
    async function getData() {
      try {
        const data = (
          await getAll(
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
    }
    getData();
  }, []);

  const getDate = () => {
    return (
      store.question.created_dt.slice(8, 10) +
      "." +
      store.question.created_dt.slice(5, 7) +
      "." +
      store.question.created_dt.slice(0, 4)
    );
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    setYourComment(value);
  };

  const getComments = async () => {
    try {
      const data = (
        await getAll(
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

  const sendComment = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      await addComment(
        store.isQuestion
          ? `community/questions/${store.question.question_id}/comments`
          : `community/observations/${store.question.observation_id}/comment`,
        yourComment,
        store.token
      );
      await getComments();
      setYourComment("");
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <Layout>
      <div className="default-container">
        <div className="flex flex-col justify-center items-center max-w-[52.7%] m-auto">
          <div className="flex items-center justify-center my-5 ">
            <p className="font-bold text-secondary  border-b-4  border-b-primary  text-2xl max-w-[205px] text-center ">
              שיתופים מהקהילה
            </p>
          </div>
        </div>
        <div className="max-w-[768px] m-auto">
          <p className="text-orange-300 text-2xl font-black">
            {store.question.username}
          </p>
          <p className="text-xl text-sky-900 font-medium">
            {store.question.question_text}
          </p>
          <div className="flex gap-3 mt-3 font-medium">
            <div className="flex items-center cursor-pointer">
              <div className="relative h-[16px] w-[16px] flex">
                <LocationIcon color="#ffa255" size={13} />
              </div>
              <p className="text-xs text-orange-400">
                {store.question.location_name}
              </p>
            </div>
            <p className="text-xs text-sky-900">{getDate()}</p>
          </div>
        </div>

        <div className="flex flex-col max-w-[100%] m-auto mt-5 gap-5">
          <Images
            username={store.question.username}
            photos={store.question.images}
            width={520}
            imageFromTheUser={true}
            isQuestion={store.isQuestion}
          />
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
          {comments.map((comment: any) => {
            return <Comment key={comment.comment_id} comment={comment} />;
          })}
        </div>
      </div>
    </Layout>
  );
};

export default SharesCommunity;

/*
גרסה הבאה
<div className="flex gap-1 flex-row-reverse items-center cursor-pointer">
              <div className="relative h-[16px] w-[16px] flex">
                <Image
                  objectFit="contain"
                  layout="fill"
                  src={heart}
                  alt="example "
                />
              </div>
              <p className="text-xs text-sky-900">322</p>
            </div>

  */
