import NextIcon from "components/Icons/NextIcon";
import { useSelector } from "react-redux";

const PostQuestionButton = () => {
  const store = useSelector((state: any) => state);

  return (
    <button
      type="submit"
      style={{
        filter: "drop-shadow(2.728px 2.925px 10.5px rgba(0,255,40,0.57))",
        backgroundImage: "linear-gradient(135deg, #65d890 0%, #50d653 100%)",
      }}
      className="flex flex-row text-2xl	text-sky-900 text-center font-bold mr-auto min-h-[43px] relative w-[100%] sm:w-[38%] rounded-xl	bg-gradient-to-r from-green-400 to-green-500"
    >
      <span className="flex flex-row m-auto">
        {store.isQuestion ? "פרסם שאלה" : "פרסם תצפית"}{" "}
        <NextIcon size={12} color="#003e5b" />
      </span>
    </button>
  );
};

export default PostQuestionButton;
