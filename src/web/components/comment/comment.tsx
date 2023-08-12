import React from "react";

interface Props {
  comment: any;
}

const Comment = ({ comment }: Props) => {
  const getTime = () => {
    const hours =
      Math.abs(new Date().getTime() - new Date(comment.create_dt).getTime()) /
      3600000;
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

  const fullName = comment.user_data.f_name + " " + comment.user_data.l_name;

  return (
    <div>
      <div className="flex flex-col max-w-[453px] min-h-[32px] rounded-2xl bg-neutral-200 pr-3  pb-2">
        <p className="text-lg text-orange-400 font-extrabold"> {fullName}</p>
        <p className="text-lg text-sky-900 font-normal">
          {comment.comment_text}
        </p>
      </div>
      <div className="flex flex-col max-w-[453px] min-h-[10px]">
        <p className="text-left text-xs text-sky-900 pl-2">{getTime()}</p>
      </div>
    </div>
  );
};

export default Comment;
