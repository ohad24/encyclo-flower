import type { NextPage } from "next";
import { useEffect, useState } from "react";
import Layout from "../components/Layout/Layout";
import Suggestions from "../components/Suggestions/Suggestions";
import TopToolbar from "../components/TopToolbar/TopToolbar";
import { get } from "services/flowersService";
import Router from "next/router";
import MoreButton from "components/Buttons/MoreButton";

const Home: NextPage = () => {
  const [questions, setQuestions] = useState<any[]>([]);
  const [observations, setObservations] = useState<any[]>([]);

  useEffect(() => {
    async function getData() {
      try {
        const questions = (
          await get("community/questions/?answer_filter=all&skip=0&limit=7")
        ).data;
        const observations = (
          await get("community/observations/?skip=0&limit=7")
        ).data;
        setQuestions(questions);
        setObservations(observations);
      } catch (err) {
        console.log(err);
      }
    }
    getData();
  }, []);

  const nextPage = (path: string) => {
    Router.push({
      pathname: path,
    });
  };

  const showQuestions = questions.map((question) => (
    <Suggestions
      key={question.question_id}
      str={"question_text"}
      question={question}
      isQuestion={true}
    />
  ));

  const showObservations = observations.map((observation) => (
    <Suggestions
      key={observation.observation_id}
      str={"observation_text"}
      question={observation}
      isQuestion={false}
    />
  ));

  return (
    <Layout>
      <div className="default-container">
        <TopToolbar />
        <div className="flex justify-center mt-5 md:mt-20">
          <p
            className="font-bold text-secondary  border-b-2 border-b-orange-300 mb-7"
            onClick={() => nextPage("/questionFromTheCommunity")}
          >
            עזרו לקהילה לזהות
          </p>
        </div>
        <div className="flex flex-col items-center gap-4">
          {showQuestions}
          <MoreButton
            text={"לעוד שאלות"}
            nextPage={nextPage}
            path={"/questionFromTheCommunity"}
          />
          <div className="flex justify-center mt-5 md:mt-20">
            <p
              className="font-bold text-secondary  border-b-2 border-b-orange-300 mb-7"
              onClick={() => nextPage("/shares")}
            >
              שיתופי תצפיות
            </p>
          </div>
          {showObservations}
          <MoreButton
            text={"לעוד שיתופים"}
            nextPage={nextPage}
            path={"/shares"}
          />
        </div>
      </div>
    </Layout>
  );
};

export default Home;
