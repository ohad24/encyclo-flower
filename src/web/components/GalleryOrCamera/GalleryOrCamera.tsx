import React from "react";
import Image from "next/image";
import camara from "../../images/camara.png";
import { ChangeEvent } from "react";
import Router from "next/router";
import { postWithAuthorization } from "services/flowersService";
import { useDispatch, useSelector } from "react-redux";
import {
  updateImagesCommunity,
  updateResults,
  updateSelectedImages,
} from "redux/action";
import Loader from "components/Loader/Loader";

interface Props {
  isAI: boolean;
  questionsIds: Array<string>;
  setQuestionsIds: (arrIds: Array<string>) => void;
}

const GalleryOrCamera = ({ isAI, questionsIds, setQuestionsIds }: Props) => {
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
        await postWithAuthorization("detect/image/", formData, store.token)
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
        await postWithAuthorization(
          store.isQuestion
            ? `community/questions/${store.questionId}/image`
            : `community/observations/${store.observationId}/image`,
          formData,
          store.token
        )
      ).data;
      setQuestionsIds([...questionsIds, data.image_id]);
      dispatch(updateImagesCommunity(FileListItems(files)));
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div>
      <Loader text="טוען תוצאות חיפוש..." isLoading={isSubmitting} />
      <label
        htmlFor="filePicker"
        className="toolbar-card flex flex-col items-center justify-center p-2 pt-0"
      >
        <input
          id="filePicker"
          type={"file"}
          className="text-secondary text-sm text-center invisible max-w-[150px]"
          onChange={(e) => (isAI ? handleSetImage(e) : addImage(e))}
          multiple={isAI ? true : false}
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

export default GalleryOrCamera;
