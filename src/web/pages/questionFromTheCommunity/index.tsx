import Layout from "components/Layout/Layout";
import React, { useEffect, useState } from "react";
import { get } from "services/flowersService";
import HeadLine from "components/Headline/headLine";
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
          await get("community/questions/?answer_filter=all&skip=0&limit=9")
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
        await get(`community/questions/?answer_filter=all&skip=${page}&limit=9`)
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

  const showQuestions = questions.map((question) => (
    <Suggestions
      key={question.question_id}
      str={"question_text"}
      question={question}
      isQuestion={true}
    />
  ));

  return (
    <Layout>
      <div className="default-container">
        <div className="flex flex-col justify-center items-center max-w-[52.7%] m-auto">
          <HeadLine text={"שאלות מהקהילה"} width={186} />
        </div>
        <InfiniteScroll
          className="flex flex-col items-center gap-4"
          dataLength={questions.length}
          next={() => fetchData()}
          hasMore={hasMore}
          loader={<h2>טוען...</h2>}
        >
          {showQuestions}
        </InfiniteScroll>
      </div>
    </Layout>
  );
};

export default QuestionCommunity;
