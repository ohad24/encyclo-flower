import Layout from "components/Layout/Layout";
import React, { useEffect } from "react";
import "../../styles/QuestionCommunity.module.css";
import { useSelector } from "react-redux";
import {
  getAll,
  submit,
  updateQuestionObservation,
} from "services/flowersService";
import Router, { withRouter } from "next/router";
import FormToCommunity from "components/Forms/FormToCommunity";
import Loader from "components/Loader/Loader";

const QuestionCommunity = () => {
  const [questionsIds, setQuestionsIds] = React.useState<string[]>([]);
  const [question, setQuestion] = React.useState("");
  const store = useSelector((state: any) => state);
  const [images, setImages] = React.useState<any[]>([]);
  const [isSubmitting, setIsSubmitting] = React.useState<boolean>(false);

  useEffect(() => {
    async function getData() {
      await getImages();
    }
    getData();
  }, [questionsIds]);

  const getImages = async () => {
    try {
      const data = (await getAll(`community/questions/${store.questionId}`))
        .data;
      setImages(data.images);
    } catch (err) {
      console.log(err);
    }
  };

  const postQuestion = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      setIsSubmitting(true);
      await updateQuestionObservation(
        `community/questions/${store.questionId}`,
        { question_text: question },
        store.token
      );
      await submit(
        `community/questions/${store.questionId}/submit`,
        store.token
      );
      setIsSubmitting(false);
      Router.push({
        pathname: "/questionFromTheCommunity",
      });
    } catch (err) {
      console.log(err);
      setIsSubmitting(false);
    }
  };

  const handleChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    await getImages();
    const { value } = e.target;
    setQuestion(value);
  };

  return (
    <Layout>
      <div className="default-container">
        <FormToCommunity
          postQuestion={postQuestion}
          handleChange={handleChange}
          images={images}
          setImages={setImages}
          questionsIds={questionsIds}
          setQuestionsIds={setQuestionsIds}
        />
        <Loader text="מפרסם שאלה..." isLoading={isSubmitting} />
      </div>
    </Layout>
  );
};

export default QuestionCommunity;
