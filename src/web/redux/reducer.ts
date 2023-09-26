const initialState = {
  results: [],
  resultsByAttributes: [],
  selectedImages: [],
  imagesCommunity: [],
  plant: {},
  clickCapture: false,
  questionId: "",
  observationId: "",
  arr: [],
  question: {},
  token: "",
  isQuestion: false,
  plantName: "",
  username: "",
  pathname: "",
  search: {
    name_text: "",
    colors: [],
    location_names: [],
    flowering_seasons: [],
    petals: [],
    leaf_shapes: [],
    leaf_edges: [],
    leaf_arrangements: [],
    life_forms: [],
    habitats: [],
    stem_shapes: [],
    spine: [],
    red: false,
    invasive: false,
    danger: false,
    rare: false,
    protected: false,
    page: 1,
  },
};

const applyChanges = (state = initialState, action: any) => {
  switch (action.type) {
    case "UpdateResults":
      return { ...state, results: action.payload };
    case "UpdateResultsByAttributes":
      return { ...state, resultsByAttributes: action.payload };
    case "UpdateSelectedImages":
      return { ...state, selectedImages: action.payload };
    case "UpdateImagesCommunity":
      return { ...state, imagesCommunity: action.payload };
    case "UpdatePlant":
      return { ...state, plant: action.payload };
    case "UpdateClickCapture":
      return { ...state, clickCapture: action.payload };
    case "UpdateQuestionId":
      return { ...state, questionId: action.payload };
    case "UpdateObservationId":
      return { ...state, observationId: action.payload };
    case "UpdateArr":
      return { ...state, arr: action.payload };
    case "UpdateQuestion":
      return { ...state, question: action.payload };
    case "UpdateToken":
      return { ...state, token: action.payload };
    case "UpdateIsQuestion":
      return { ...state, isQuestion: action.payload };
    case "UpdatePlantName":
      return { ...state, plantName: action.payload };
    case "UpdateUserName":
      return { ...state, username: action.payload };
    case "UpdatePathName":
      return { ...state, pathname: action.payload };
    case "UpdateSearch":
      return { ...state, search: action.payload };
    default:
      return state;
  }
};

export default applyChanges;
