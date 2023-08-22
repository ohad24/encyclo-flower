import { ChangeEvent } from "react";
import { updateImagesCommunity } from "redux/action";
import { postWithAuthorization } from "services/flowersService";
import { AnyAction, Dispatch } from "redux";

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

export const addImage = async (
  e: ChangeEvent<HTMLInputElement>,
  store: any,
  questionsIds: string[],
  setQuestionsIds: React.Dispatch<React.SetStateAction<string[]>>,
  dispatch: Dispatch<AnyAction>
) => {
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
    dispatch(updateImagesCommunity(FileListItems(files, store)));
  } catch (err) {
    console.log(err);
  }
};
