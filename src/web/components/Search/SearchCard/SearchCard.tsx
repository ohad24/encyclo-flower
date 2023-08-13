import React, { useEffect } from "react";
import { ISearchResult } from "helpers/interfaces";
import { globalColors } from "helpers/globalObjects";
import PageLinesIcon from "components/Icons/PageLinesIcon";
import FlaskIcon from "components/Icons/FlaskIcon";
import PaintBrush from "components/Icons/PaintBrush";
import Link from "next/link";

interface Props {
  item: ISearchResult;
}

const getColors = (color: string): string => {
  let newColor: string | undefined = globalColors?.find(
    (x) => x.name === color
  )?.color;

  if (newColor === undefined) newColor = "#fff";
  return newColor;
};

const SearchCard = ({ item }: Props) => {
  useEffect(() => {}, []);

  return (
    <div
      className="flex flex-col   w-full sm:w-[20rem] my-4 
          bg-white rounded-xl transform transition-all hover:-translate-y-[0.5px] shadow hover:shadow-xl
          duration-300 pb-3 group"
    >
      <img
        src={`${process.env.IMAGE_BASE_URL}/plants-images/thumbnails/${item.image}`}
        className="h-40 object-cover rounded-xl w-full rounded-b-none"
        alt="some alt"
      />
      <div className="p-2 flex flex-col justify-center gap-2">
        <div className="flex items-center gap-4">
          <PageLinesIcon size={20} color={"#0f4871"} />
          <h2 className="font-bold text-lg text-primary">{item.heb_name}</h2>
        </div>
        <div className="flex items-center gap-4">
          <FlaskIcon size={20} color={"#0f4871"} />
          <p className="text-sm  text-secondary font-bold">
            שם מדעי:<span className="">&nbsp;{item.science_name}</span>
          </p>
        </div>
        <div className="flex items-center gap-4">
          <PaintBrush size={20} color={"#0f4871"} />
          <p className="text-sm  text-secondary font-bold flex items-center gap-3">
            צבעים בטבע:
            <div className="flex gap-1 ">
              {item.colors?.map((color) => {
                const bgColor = getColors(color);

                return (
                  <div
                    key={color}
                    className={`rounded-full w-[14px] h-[14px] border border-gray-700 '`}
                    style={{ backgroundColor: `${bgColor}` }}
                  >
                    &nbsp;
                  </div>
                );
              })}
            </div>
          </p>
        </div>
      </div>
      <div className="mt-2 self-center">
        <Link role="button" href={`/plantes/${item.science_name}`}>
          <div className="text-white transform transition-all cursor-pointer duration-300  bg-gradient-to-t from-[#FFA500] to-[#FFD700] hover:from-[#FFD700] hover:to-[#FFA500] px-3 py-1 rounded-md ">
            בקר בדף הצמח
          </div>
        </Link>
      </div>
    </div>
  );
};

export default SearchCard;
