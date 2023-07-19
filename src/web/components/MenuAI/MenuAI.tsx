import CamaraIcon from "components/Icons/CamaraIcon";
import HeartIcon from "components/Icons/HeartIcon";
import NewSearch from "components/NewSearch/NewSearch";
import Router, { useRouter } from "next/router";
import { useDispatch, useSelector } from "react-redux";
import {
  UpdateIsQuestion,
  UpdateQuestionId,
  updateImagesCommunity,
} from "redux/action";
import { createQuestion, getSearchResults } from "services/flowersService";

const MenuAI = (props: { setIsOpen: (bool: boolean) => void }) => {
  const dispatch = useDispatch();
  const store = useSelector((state: any) => state);

  function FileListItems(files: FileList | null, store: any) {
    var b = new ClipboardEvent("").clipboardData || new DataTransfer();
    for (var i = 0, len1 = store.imagesCommunity.length; i < len1; i++) {
      if (store.imagesCommunity[i].name) {
        b.items.add(store.imagesCommunity[i]);
      }
    }
    for (var i = 0, len = files !== null ? files.length : 0; i < len; i++) {
      if (files !== null) {
        b.items.add(files[i]);
      }
    }
    return b.files;
  }

  const askTheCommunity = async () => {
    try {
      const data = (
        await createQuestion("community/questions/", "מהי שאלתך?", store.token)
      ).data;
      dispatch(UpdateQuestionId(data.question_id));
      dispatch(UpdateIsQuestion(true));
      const files = store.selectedImages;
      const formData = new FormData();
      if (files && files[0]) {
        formData.append("image", files[0]);
      }
      try {
        await getSearchResults(
          store.isQuestion
            ? `community/questions/${data.question_id}/image`
            : `community/observations/${store.observationId}/image`,
          formData,
          store.token
        );
        dispatch(updateImagesCommunity(FileListItems(files, store)));
      } catch (err) {
        console.log(err);
      }
      Router.push({
        pathname: "/questionCommunity",
      });
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className="flex flex-col items-center">
      <div className="flex items-center justify-center my-5">
        <p className="font-bold text-secondary  border-b-4  border-b-primary mb-2 text-2xl w-[120px] text-center ">
          זיהוי צמח
        </p>
      </div>
      <div className="flex flex-col md:flex-row gap-5">
        <NewSearch isAI={true} questionsIds={[]} setQuestionsIds={() => {}} />
        <div
          onClick={() => askTheCommunity()}
          className="cursor-pointer flex justify-center items-center gap-2 text-secondary bg-gradient-to-r from-[#FFA500] to-[#FFD700] transition duration-500 min-w-[248px] text-center p-1 rounded shadow hover:shadow-lg"
        >
          <HeartIcon />
          <button>שאל את הקהילה</button>
        </div>
        <div
          className="cursor-pointer flex justify-center items-center gap-2 text-secondary bg-gradient-to-r from-[#FFA500] to-[#FFD700] transition duration-500  w-[248px] text-center p-1 rounded shadow hover:shadow-lg"
          onClick={() => props.setIsOpen(true)}
        >
          <CamaraIcon />
          <button>הנחיות צילום</button>
        </div>
      </div>
    </div>
  );
};

export default MenuAI;
