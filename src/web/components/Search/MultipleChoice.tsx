import React from "react";

type Props = {
  list: { name: string; isActive: boolean }[];
  isSingSelection?: boolean;
  onChange: (value: string, isIn: boolean) => void;
};
const MultipleChoice = ({ list, onChange, isSingSelection = false }: Props) => {
  const [state, setState] = React.useState(list);

  const showChoice = state.map((item, index) => {
    return (
      <div
        key={item.name}
        className={`p-1 border rounded-xl text-xs
         ${
           item.isActive
             ? "text-primary border-primary"
             : "text-gray-500 border-gray-400"
         } 
          min-w-[40px] text-center cursor-pointer transition duration-500 `}
        onClick={() => {
          if (isSingSelection) state.map((item) => (item.isActive = false));
          const newItem = state[index];
          newItem.isActive = !newItem.isActive || isSingSelection;
          state[index] = newItem;
          setState([...state]);
          onChange(newItem.name, newItem.isActive);
        }}
      >
        {item.name}
      </div>
    );
  });

  return (
    <div className="flex flex-wrap max-w-[340px] gap-2 p-2 justify-center">
      {showChoice}
    </div>
  );
};

export default MultipleChoice;
