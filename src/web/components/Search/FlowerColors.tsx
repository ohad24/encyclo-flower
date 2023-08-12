import React, { useEffect } from "react";
import { globalColors } from "helpers/globalObjects";
type Props = {
  onColorChange: (color: string, isIn: boolean) => void;
};
const FlowerColors = ({ onColorChange }: Props) => {
  const [colors, setColors] = React.useState(globalColors);
  useEffect(() => {}, [colors]);

  const showColors = colors.map((item, index) => {
    return (
      <div
        key={item.color}
        className={`flex-1 text-1  w-[30px] h-[30px] rounded border border-gray-300 ${
          item.isActive
            ? "border-2 border-orange-500 shadow"
            : "border-gray-300"
        } cursor-pointer hover:scale-[1.1] transition duration-75`}
        style={{ background: item.color }}
        onClick={() => {
          const newItem = colors[index];
          newItem.isActive = !newItem.isActive;
          colors[index] = newItem;
          setColors([...colors]);
          onColorChange(newItem.name, newItem.isActive);
        }}
      >
        &nbsp;
      </div>
    );
  });

  return (
    <div>
      <div className="grid grid-cols-4 row-gap grid-cols-reverse gap-1  max-w-[200px] gap-y-2 gap-x-4">
        {colors && showColors}
      </div>
    </div>
  );
};

export default FlowerColors;
