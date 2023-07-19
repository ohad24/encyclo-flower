import React from "react";
import LikeIcon from "components/Icons/LikeIcon";

const Comment = (props: { comment: any }) => {
  const getTime = () => {
    const hours =
      Math.abs(
        new Date().getTime() - new Date(props.comment.create_dt).getTime()
      ) / 3600000;
    if (hours < 1) {
      const minutes = hours * 60;
      if (minutes < 1) {
        return Math.floor(minutes * 60) + " שניות";
      } else {
        return Math.floor(hours * 60) + " דקות";
      }
    } else {
      return Math.floor(hours) + " שעות";
    }
  };

  return (
    <div>
      <div className="flex flex-col max-w-[453px] min-h-[32px] rounded-2xl bg-neutral-200 pr-3  pb-2">
        <p className="text-lg text-orange-400 font-extrabold">
          {" "}
          {props.comment.user_data.f_name +
            " " +
            props.comment.user_data.l_name}
        </p>
        <p className="text-lg text-sky-900 font-normal">
          {props.comment.comment_text}
        </p>
      </div>
      <div className="flex flex-col max-w-[453px] min-h-[10px]">
        <p className="text-left text-xs text-sky-900 pl-2">{getTime()}</p>
      </div>
    </div>
  );
};

export default Comment;

/* גרסה הבאה
<div className="flex flex-row text-sm	text-sky-900 font-medium	ml-2">
          <div
            className="w-[20px] h-[20px] rounded-full mr-auto ml-1 pr-0.5 pt-0.5"
            style={{
              filter: "drop-shadow(0px 4px 10.5px rgba(249,189,56,0.73))",
              backgroundImage:
                "linear-gradient(135deg, #f58f3b 0%, #f9bd38 100%)",
            }}
          >
            <LikeIcon color="#003e5b" size={16} />
          </div>{" "}
          <p>98</p>
        </div> */
