import React from "react";

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
