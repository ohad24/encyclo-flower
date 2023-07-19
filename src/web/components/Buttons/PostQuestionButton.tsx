import NextIcon from "components/Icons/NextIcon";
import { useSelector } from "react-redux";

const PostQuestionButton = () => {
  const store = useSelector((state: any) => state);

  return (
    <button
      type="submit"
      style={{
        display: "flex",
        flexDirection: "row",
        minHeight: "43px",
        fontSize: "23px",
        color: "#003e5b",
        fontWeight: "700",
        textAlign: "center",
        borderRadius: "10px",
        marginRight: "auto",
        filter: "drop-shadow(2.728px 2.925px 10.5px rgba(0,255,40,0.57))",
        backgroundImage: "linear-gradient(135deg, #65d890 0%, #50d653 100%)",
      }}
      className="relative w-[100%] sm:w-[38%]"
    >
      <span
        style={{
          margin: "auto",
          display: "flex",
          flexDirection: "row",
        }}
      >
        {store.isQuestion ? "פרסם שאלה" : "פרסם תצפית"}{" "}
        <NextIcon size={12} color="#003e5b" />
      </span>
    </button>
  );
};

export default PostQuestionButton;
