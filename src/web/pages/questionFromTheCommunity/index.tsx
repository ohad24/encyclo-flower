import Layout from "components/Layout/Layout";
import React, { useEffect, useState } from "react";
import { getAll } from "services/flowersService";
import Suggestions from "components/Suggestions/Suggestions";
import InfiniteScroll from "react-infinite-scroll-component";

const QuestionCommunity = () => {
  const [questions, setQuestions] = useState<any[]>([]);
  const [page, setPage] = useState<number>(9);
  const [hasMore, setHasMore] = useState<boolean>(true);

  useEffect(() => {
    async function getData() {
      try {
        const questions = (
          await getAll("community/questions/?answer_filter=all&skip=0&limit=9")
        ).data;
        setQuestions(questions);
      } catch (err) {
        console.log(err);
      }
    }
    getData();
  }, []);

  const fetchData = async () => {
    try {
      const data = (
        await getAll(
          `community/questions/?answer_filter=all&skip=${page}&limit=9`
        )
      ).data;
      if (data.length === 0) {
        setHasMore(false);
      } else {
        setQuestions([...questions, ...data]);
        setPage(page + 9);
      }
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <Layout>
      <div className="default-container">
        <div className="flex flex-col justify-center items-center max-w-[52.7%] m-auto">
          <div className="flex items-center justify-center my-5 ">
            <p className="font-bold text-secondary  border-b-4  border-b-primary mb-7 text-2xl w-[186px] text-center ">
              שאלות מהקהילה
            </p>
          </div>
        </div>
        <InfiniteScroll
          className="flex flex-col items-center gap-4"
          dataLength={questions.length}
          next={() => fetchData()}
          hasMore={hasMore}
          loader={<h2>טוען...</h2>}
        >
          {questions.map((question) => (
            <Suggestions
              key={question.question_id}
              str={"question_text"}
              question={question}
              isQuestion={true}
            />
          ))}
        </InfiniteScroll>
      </div>
    </Layout>
  );
};

export default QuestionCommunity;
