const updateResults = (arr: Object[]) => {
  return {
    type: "UpdateResults",
    payload: arr,
  };
};

const updateSelectedImages = (arr: FileList | File[] | null) => {
  return {
    type: "UpdateSelectedImages",
    payload: arr,
  };
};

const updateImagesCommunity = (arr: FileList | File[] | null) => {
  return {
    type: "UpdateImagesCommunity",
    payload: arr,
  };
};

const updatePlant = (obj: Object) => {
  return {
    type: "UpdatePlant",
    payload: obj,
  };
};

const UpdateClickCapture = (bool: boolean) => {
  return {
    type: "UpdateClickCapture",
    payload: bool,
  };
};

const UpdateQuestionId = (questionId: string) => {
  return {
    type: "UpdateQuestionId",
    payload: questionId,
  };
};

const UpdateObservationId = (observationId: string) => {
  return {
    type: "UpdateObservationId",
    payload: observationId,
  };
};

const UpdateArr = (arr: Array<object>) => {
  return {
    type: "UpdateArr",
    payload: arr,
  };
};

const UpdateQuestion = (obj: object) => {
  return {
    type: "UpdateQuestion",
    payload: obj,
  };
};

const UpdateToken = (str: string) => {
  return {
    type: "UpdateToken",
    payload: str,
  };
};

const UpdateIsQuestion = (bool: boolean) => {
  return {
    type: "UpdateIsQuestion",
    payload: bool,
  };
};

const UpdatePlantName = (plantName: string | undefined) => {
  return {
    type: "UpdatePlantName",
    payload: plantName,
  };
};

const UpdateUserName = (username: string) => {
  return {
    type: "UpdateUserName",
    payload: username,
  };
};

export {
  updateResults,
  updatePlant,
  UpdateClickCapture,
  updateSelectedImages,
  updateImagesCommunity,
  UpdateQuestionId,
  UpdateObservationId,
  UpdateArr,
  UpdateQuestion,
  UpdateToken,
  UpdateIsQuestion,
  UpdatePlantName,
  UpdateUserName,
};
