import React from "react";
import { Checkbox } from "@chakra-ui/react";

const EnvTypes = ({ state, onChange }) => {
  return (
    <div className="flex flex-wrap  gap-2 w-[180px] justify-center">
      <Checkbox
        size="sm"
        colorScheme="orange"
        isChecked={state.red}
        onChange={(e) => {
          onChange("red", e.target.checked);
        }}
      >
        אדום
      </Checkbox>
      <Checkbox
        size="sm"
        colorScheme="orange"
        isChecked={state.protected}
        onChange={(e) => {
          onChange("protected", e.target.checked);
        }}
      >
        מוגן{" "}
      </Checkbox>
      <Checkbox
        size="sm"
        colorScheme="orange"
        isChecked={state.invasive}
        onChange={(e) => {
          onChange("invasive", e.target.checked);
        }}
      >
        פולש{" "}
      </Checkbox>
      <Checkbox
        size="sm"
        colorScheme="orange"
        isChecked={state.rare}
        onChange={(e) => {
          onChange("rare", e.target.checked);
        }}
      >
        נדיר{" "}
      </Checkbox>
      <Checkbox
        size="sm"
        colorScheme="orange"
        isChecked={state.danger}
        onChange={(e) => {
          onChange("danger", e.target.checked);
        }}
      >
        בסיכון{" "}
      </Checkbox>
    </div>
  );
};

export default EnvTypes;
