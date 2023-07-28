import React from "react";
import Image from "next/image";
import camara from "../../images/camara.png";
import { ChangeEvent } from "react";
import Router, { withRouter } from "next/router";
import { getSearchResults } from "services/flowersService";
import { useDispatch, useSelector } from "react-redux";
import {
  updateImagesCommunity,
  updateResults,
  updateSelectedImages,
} from "redux/action";
import Loader from "components/Loader/Loader";

const ModalCamera = (props: {
  isAI: boolean;
  isAIOpen: boolean;
  setIsAIOpen: (bool: boolean) => void;
  questionsIds: Array<string>;
  setQuestionsIds: (arrIds: Array<string>) => void;
}) => {
  const dispatch = useDispatch();
  const store = useSelector((state: any) => state);
  const [isSubmitting, setIsSubmitting] = React.useState<boolean>(false);

  function FileListItems(files: FileList | null) {
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

  const handleSetImage = async (e: ChangeEvent<HTMLInputElement>) => {
    const { files } = e.target;
    const formData = new FormData();
    if (files && files[0]) {
      formData.append("file", files[0]);
    }
    try {
      setIsSubmitting(true);
      const data = (
        await getSearchResults("detect/image/", formData, store.token)
      ).data;
      dispatch(updateResults(data));
      dispatch(updateSelectedImages(files));
      Router.push({
        pathname: "/ai",
      });
      setIsSubmitting(false);
    } catch (err) {
      console.log(err);
      setIsSubmitting(false);
    }
  };

  const addImage = async (e: ChangeEvent<HTMLInputElement>) => {
    const { files } = e.target;
    const formData = new FormData();
    if (files && files[0]) {
      formData.append("image", files[0]);
    }
    try {
      const data = (
        await getSearchResults(
          store.isQuestion
            ? `community/questions/${store.questionId}/image`
            : `community/observations/${store.observationId}/image`,
          formData,
          store.token
        )
      ).data;
      props.setQuestionsIds([...props.questionsIds, data.image_id]);
      props.setIsAIOpen(false);
      dispatch(updateImagesCommunity(FileListItems(files)));
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className="toolbar-card">
      <Loader text="טוען תוצאות חיפוש..." isLoading={isSubmitting} />
      <label
        className="flex flex-col items-center justify-center p-2 pt-0"
        htmlFor="filePicker"
      >
        <input
          id="filePicker"
          type={"file"}
          className="text-secondary text-sm text-center max-w-[150px] invisible"
          onChange={(e) => (props.isAI ? handleSetImage(e) : addImage(e))}
          multiple={props.isAI ? true : false}
        ></input>
        <span>
          <Image src={camara} alt="Camara" />
        </span>
        <span className="text-secondary font-bold font-xl">זיהוי צמח</span>
        <span className="text-sm">זיהוי AI/קהילה</span>
      </label>
    </div>
  );
};

export default ModalCamera;
