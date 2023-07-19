import React from "react";
import Image from "next/image";

import {
  leafArrangements,
  leafEdges,
  leafShapes,
  stemShapes,
} from "helpers/flowersShapeObjects";

type Props = {
  startIngIndex: number;
  onShapeChange: (value: string, isIn: boolean) => void;
};

const getShape = (startIngIndex: number) => {
  if (startIngIndex === 0) {
    return leafShapes;
  } else if (startIngIndex === 4) {
    return leafArrangements;
  } else if (startIngIndex === 5) {
    return leafEdges;
  } else {
    return stemShapes;
  }
};

const FlowerShape = ({ startIngIndex, onShapeChange }: Props) => {
  const [currentShapes, setShape] = React.useState(getShape(startIngIndex));

  return (
    <div>
      <div className="grid grid-cols-3 row-gap grid-cols-reverse gap-1  max-w-[200px] gap-y-6 gap-x-6">
        {currentShapes.map((shape, index) => {
          return (
            <div
              key={index}
              className={`border  ${
                shape.isActive ? "border-primary border-2" : "border-gray-400"
              } p-[3px] rounded-xl cursor-pointer transition duration-300 hover:scale-[1.2]`}
              onClick={() => {
                const newItem = currentShapes[index];
                newItem.isActive = !newItem.isActive;
                currentShapes[index] = newItem;
                setShape([...currentShapes]);
                onShapeChange(newItem.name, newItem.isActive);
              }}
            >
              <Image
                src={shape.image}
                objectFit="contain"
                width={50}
                height={50}
                alt="Map Image"
              />
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default FlowerShape;
