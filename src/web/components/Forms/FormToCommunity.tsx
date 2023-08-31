import AddImageButton from "components/Buttons/AddImageButton";
import PostQuestionButton from "components/Buttons/PostQuestionButton";
import ImageFromQuestion from "components/ImageFromQuestion/ImageFromQuestions";
import { useSelector } from "react-redux";
import { Input } from "@chakra-ui/react";
import HeadLine from "components/Headline/headLine";

interface Props {
  postQuestion: (e: React.FormEvent) => Promise<void>;
  handleChange: (e: React.ChangeEvent<HTMLInputElement>) => Promise<void>;
  images: any;
  setImages: React.Dispatch<any>;
  questionsIds: string[];
  setQuestionsIds: React.Dispatch<React.SetStateAction<string[]>>;
}

const FormToCommunity = ({
  postQuestion,
  handleChange,
  images,
  setImages,
  questionsIds,
  setQuestionsIds,
}: Props) => {
  const store = useSelector((state: any) => state);

  const showImages = Array.from(images).map((image: any, index) => {
    return (
      <ImageFromQuestion
        key={image.image_id}
        index={index}
        image={image}
        images={images}
        setImages={setImages}
      />
    );
  });

  const questionOrShare = store.isQuestion ? "שאלה לקהילה" : "שיתוף תצפית";

  return (
    <form
      onSubmit={postQuestion}
      className="flex flex-col justify-center items-center w-[100%] md:max-w-[52.7%] m-auto"
    >
      <HeadLine text={questionOrShare} width={158} />

      <Input
        className="relative p-2 mb-8 max-w-[100%] min-h-[80px] caret-color: #60a5fa placeholder-sky-900 text-sky-900 pb-12"
        placeholder="מהי שאלתך?"
        onBlur={handleChange}
        minLength={5}
        required
        style={{
          borderRadius: "25px",
          backgroundColor: "rgb(229 231 235)",
        }}
      />
      <div className="flex flex-row gap-10 ml-auto flex-wrap">{showImages}</div>
      <AddImageButton
        questionsIds={questionsIds}
        setQuestionsIds={setQuestionsIds}
      />
      <br />
      <PostQuestionButton />
    </form>
  );
};

export default FormToCommunity;
