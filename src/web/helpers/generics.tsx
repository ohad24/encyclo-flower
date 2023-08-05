import { IState } from "./interfaces";

export const removeEmptyValues = (state: IState) => {
  let searchResults = {};
  let item: keyof typeof state;

  Object.entries(state).forEach(([key, value]) => {
    if (typeof value === "string" || "array" || "object") {
      if (value.length > 0) {
        searchResults = { ...searchResults, [key]: value };
      }
    }
    if (typeof value === "boolean" && value === true) {
      searchResults = { ...searchResults, [key]: value };
    }
  });

  return searchResults;
};
