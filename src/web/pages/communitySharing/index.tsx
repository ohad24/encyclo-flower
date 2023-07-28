import Layout from "components/Layout/Layout";
import React, { useEffect } from "react";
import "../../styles/QuestionCommunity.module.css";
import { useDispatch, useSelector } from "react-redux";
import { UpdateIsQuestion } from "redux/action";
import {
  getAll,
  submit,
  updateQuestionObservation,
} from "services/flowersService";
import Router, { withRouter } from "next/router";
import FormToCommunity from "components/Forms/FormToCommunity";
import Loader from "components/Loader/Loader";

const CommunitySharing = () => {
  const [questionsIds, setQuestionsIds] = React.useState<string[]>([]);
  const [question, setQuestion] = React.useState("");
  const [images, setImages] = React.useState<any>([]);
  const [isSubmitting, setIsSubmitting] = React.useState<boolean>(false);

  const store = useSelector((state: any) => state);

  const dispatch = useDispatch();

  useEffect(() => {
    async function getData() {
      try {
        const data = (
          await getAll(`community/observations/${store.observationId}`)
        ).data;
        setImages(data.images);
      } catch (err) {
        console.log(err);
      }
    }
    getData();
    dispatch(UpdateIsQuestion(false));
  }, [dispatch, questionsIds]);

  const postQuestion = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setIsSubmitting(true);
      await updateQuestionObservation(
        `community/observations/${store.observationId}`,
        { observation_text: question },
        store.token
      );
      await submit(
        `community/observations/${store.observationId}/submit`,
        store.token
      );
      setIsSubmitting(false);
      Router.push({
        pathname: "/shares",
      });
    } catch (err) {
      console.log(err);
      setIsSubmitting(false);
    }
  };

  const getImages = async () => {
    try {
      const data = (
        await getAll(`community/observations/${store.observationId}`)
      ).data;
      setImages(data.images);
    } catch (err) {
      console.log(err);
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
        <Loader text="מפרסם תצפית..." isLoading={isSubmitting} />
      </div>
    </Layout>
  );
};

export default CommunitySharing;
