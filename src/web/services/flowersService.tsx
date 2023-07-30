import axios from "axios";

const API_URL = process.env.SERVER_BASE_URL || "";

const getAll = (params: string) => axios.get(`${API_URL}/${params}`);

const getPlantByName = (name: string) => axios.get(`${API_URL}/${name}`);

const getSearchResults = (path: string, formData: FormData, token: string) =>
  axios.post(`${API_URL}/${path}`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${token}`,
    },
  });

const getIsFavorite = (path: string, token: string) =>
  axios.get(`${API_URL}/${path}`, {
    headers: {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${token}`,
    },
  });

const verifyEmail = (path: string) =>
  axios.get(`${API_URL}/${path}`, {
    headers: {
      accept: "*/*",
    },
  });

const login = (path: string, obj: object) =>
  axios.post(`${API_URL}/${path}`, new URLSearchParams({ ...obj }), {
    headers: {
      accept: "application/json",
    },
  });

const register = (path: string, obj: object) =>
  axios.post(
    `${API_URL}/${path}`,
    JSON.stringify({
      ...obj,
    }),
    {
      headers: {
        "Content-Type": "application/json",
      },
    }
  );

// לצמצם לאחד
const createQuestion = (path: string, text: string, token: string) =>
  axios.post(
    `${API_URL}/${path}`,
    JSON.stringify({
      question_text: text,
    }),
    {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    }
  );

// לצמצם לאחד
const createObservation = (path: string, text: string, token: string) =>
  axios.post(
    `${API_URL}/${path}`,
    JSON.stringify({
      observation_text: text,
    }),
    {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    }
  );

const addComment = (path: string, text: string, token: string) =>
  axios.post(
    `${API_URL}/${path}`,
    JSON.stringify({
      comment_text: text,
    }),
    {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    }
  );

const updateQuestionObservation = (path: string, obj: object, token: string) =>
  axios.put(`${API_URL}/${path}`, JSON.stringify(obj), {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });

const removeFavorite = (path: string, token: string) =>
  axios.delete(`${API_URL}/${path}`, {
    headers: {
      accept: "*/*",
      Authorization: `Bearer ${token}`,
    },
  });

const deleteImage = (path: string, token: string) =>
  axios.delete(`${API_URL}/${path}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

const rotateImageInQuestion = (path: string, token: string) =>
  axios.post(
    `${API_URL}/${path}`,
    JSON.stringify({
      angle: "R",
    }),
    {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    }
  );

const searchPlant = (path: string, obj: object) =>
  axios.post(
    `${API_URL}/${path}`,
    JSON.stringify({
      ...obj,
    }),
    {
      headers: {
        "Content-Type": "application/json",
      },
    }
  );

const update = (path: string, obj: object, token: string) =>
  axios.put(
    `${API_URL}/${path}`,
    JSON.stringify({
      ...obj,
    }),
    {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    }
  );

const submit = (path: string, token: string) =>
  axios.put(
    `${API_URL}/${path}`,
    {},
    {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    }
  );

export {
  getAll,
  login,
  register,
  getSearchResults,
  getPlantByName,
  getIsFavorite,
  verifyEmail,
  createQuestion,
  createObservation,
  addComment,
  updateQuestionObservation,
  removeFavorite,
  deleteImage,
  rotateImageInQuestion,
  searchPlant,
  update,
  submit,
};
