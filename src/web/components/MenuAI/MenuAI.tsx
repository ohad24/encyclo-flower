import React, { useState } from "react";
import ButtonAI from "components/Buttons/ButtonAI";
import CamaraIcon from "components/Icons/CamaraIcon";
import HeartIcon from "components/Icons/HeartIcon";
import NewSearch from "components/NewSearch/NewSearch";
import Router from "next/router";
import { useDispatch, useSelector } from "react-redux";
import {
  UpdateIsQuestion,
  UpdateQuestionId,
  updateImagesCommunity,
} from "redux/action";
import { create, postWithAuthorization } from "services/flowersService";
import ModalLoginMessage from "components/Modals/ModalLoginMessage";
import HeadLine from "components/HeadLine/HeadLine";

interface Props {
  setIsOpen: (bool: boolean) => void;
}

const MenuAI = ({ setIsOpen }: Props) => {
  const store = useSelector((state: any) => state);
  const dispatch = useDispatch();
  const [isOpen, setIsOpenLog] = useState(false);

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
      dispatch(updateImagesCommunity([]));
      const data = (
        await create(
          "community/questions/",
          { question_text: "מהי שאלתך?" },
          store.token
        )
      ).data;
      dispatch(UpdateQuestionId(data.question_id));
      dispatch(UpdateIsQuestion(true));
      const files = store.selectedImages;
      const formData = new FormData();
      if (files && files[0]) {
        formData.append("image", files[0]);
      }
      try {
        await postWithAuthorization(
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
      <HeadLine text={"זיהוי צמח"} width={120} />
      <div className="flex flex-col md:flex-row gap-5">
        <NewSearch isAI={true} questionsIds={[]} setQuestionsIds={() => {}} />
        <ButtonAI
          icon={<HeartIcon />}
          text={"שאל את הקהילה"}
          funcClick={
            store.token ? () => askTheCommunity() : () => setIsOpenLog(true)
          }
        />{" "}
        <ButtonAI
          icon={<CamaraIcon />}
          text={"הנחיות צילום"}
          funcClick={() => setIsOpen(true)}
        />
      </div>
      <ModalLoginMessage isOpen={isOpen} setIsOpen={setIsOpenLog} />
    </div>
  );
};

export default MenuAI;
