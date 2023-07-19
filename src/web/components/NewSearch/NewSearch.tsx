import React from "react";
import GalleryIcon from "components/Icons/Gallery";
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
import SearchIcon from "components/Icons/SearchIcon";

const NewSearch = (props: {
  isAI: boolean;
  isSearchFromPlant?: boolean;
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
      dispatch(updateImagesCommunity(FileListItems(files)));
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div
      className={
        props.isSearchFromPlant
          ? "h-[100px] m-auto max-w-[120px] mt-2 sm:mt-5"
          : "h-[32px]"
      }
    >
      {" "}
      <Loader text="טוען תוצאות חיפוש..." isLoading={isSubmitting} />
      {props.isSearchFromPlant ? (
        <label
          htmlFor="filePicker"
          className="cursor-pointer text-center flex flex-col-reverse text-base m-auto text-secondary bg-gradient-to-r from-[#FFA500] to-[#FFD700] transition duration-500 h-[100px] w-[120px] rounded-3xl"
        >
          <span className="table m-auto">
            <span className="table m-auto">
              <GalleryIcon size={22} />
            </span>
            <span className="flex flex-wrap leading-5 max-w-[100px] font-bold">
              חיפוש בעזרת תמונה
            </span>
          </span>
        </label>
      ) : (
        <label
          htmlFor="filePicker"
          className="cursor-pointer flex justify-center items-center gap-2 text-secondary bg-gradient-to-r from-[#FFA500] to-[#FFD700] transition duration-500 min-w-[248px] text-center p-1 rounded shadow hover:shadow-lg"
        >
          <SearchIcon /> <span>חיפוש חדש</span>
        </label>
      )}
      <input
        id="filePicker"
        style={{ visibility: "hidden" }}
        type={"file"}
        className="text-secondary text-sm text-center max-w-[150px]"
        onChange={(e) => (props.isAI ? handleSetImage(e) : addImage(e))}
        multiple={props.isAI ? true : false}
      ></input>
    </div>
  );
};

export default NewSearch;

/* 
    <button className="flex flex-col-reverse text-base m-auto text-secondary bg-gradient-to-r from-[#FFA500] to-[#FFD700] transition duration-500 h-[100px] w-[120px] mt-2 sm:mt-5 rounded-3xl">
            <span className="table m-auto">
              <span className="table m-auto">
                <GalleryIcon size={22} />
              </span>
              <span className="flex flex-wrap leading-5 max-w-[100px] font-bold">
                חיפוש בעזרת תמונה
              </span>
            </span>
          </button>
<div className="cursor-pointer h-[50px] flex justify-center items-center gap-2 text-secondary bg-gradient-to-r from-[#FFA500] to-[#FFD700] transition duration-500 min-w-[248px] text-center p-1 rounded shadow hover:shadow-lg">
      <Loader text="טוען תוצאות חיפוש..." isLoading={isSubmitting} />
      <div className="bg-orange-500">
        <label htmlFor="filePicker" className="flex flex-row">
          <input
            id="filePicker"
            style={{ visibility: "hidden" }}
            type={"file"}
            className="text-secondary text-sm text-center max-w-[150px]"
            onChange={(e) => (props.isAI ? handleSetImage(e) : addImage(e))}
            multiple={props.isAI ? true : false}
          ></input>
          <span className="flex flex-row m-auto inline-block items-center">
            {" "}
            <SearchIcon /> <span className="m-auto">חיפוש חדש</span>{" "}
          </span>
        </label>
      </div>
    </div> */
