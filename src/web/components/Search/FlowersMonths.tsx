import React from "react";
import { Checkbox } from "@chakra-ui/react";
import { monthsText } from "helpers/globalObjects";

type Props = {
  onMonthChange: (month: string, isIn: boolean) => void;
};
const FlowersMonths = ({ onMonthChange }: Props) => {
  const [months, setMonths] = React.useState(monthsText);

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 grid-cols-reverse gap-1 ">
      {monthsText.map((month, index) => {
        return (
          <div key={month.name} className="flex-1 text-1">
            <Checkbox
              size="sm"
              colorScheme="orange"
              isChecked={monthsText[index].isActive}
              onChange={(e) => {
                const newItem = months[index];
                newItem.isActive = !newItem.isActive;
                months[index] = newItem;
                setMonths([...months]);
                onMonthChange(String(index + 1), e.target.checked);
              }}
            >
              {month.name}
            </Checkbox>
          </div>
        );
      })}
    </div>
  );
};

export default FlowersMonths;
