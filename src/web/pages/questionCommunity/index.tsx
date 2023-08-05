import Layout from "components/Layout/Layout";
import React, { useEffect } from "react";
import "../../styles/QuestionCommunity.module.css";
import { useSelector } from "react-redux";
import { get, putWithAuthorization } from "services/flowersService";
import Router from "next/router";
import FormToCommunity from "components/Forms/FormToCommunity";
import Loader from "components/Loader/Loader";

const QuestionCommunity = () => {
  const store = useSelector((state: any) => state);
  const [questionsIds, setQuestionsIds] = React.useState<string[]>([]);
  const [question, setQuestion] = React.useState("");
  const [images, setImages] = React.useState<any[]>([]);
  const [isSubmitting, setIsSubmitting] = React.useState<boolean>(false);

  const getImages = async () => {
    try {
      const data = (await get(`community/questions/${store.questionId}`)).data;
      setImages(data.images);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    async function getData() {
      try {
        const data = (await get(`community/questions/${store.questionId}`))
          .data;
        setImages(data.images);
      } catch (err) {
        console.log(err);
      }
    }
    getData();
  }, [questionsIds]);

  const postQuestion = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setIsSubmitting(true);
      await putWithAuthorization(
        `community/questions/${store.questionId}`,
        { question_text: question },
        store.token
      );
      await putWithAuthorization(
        `community/questions/${store.questionId}/submit`,
        {},
        store.token
      );
      Router.push({
        pathname: "/questionFromTheCommunity",
      });
      setIsSubmitting(false);
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
