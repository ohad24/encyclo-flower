import axios from "axios";
import { useSelector } from "react-redux";

const API_URL = process.env.SERVER_BASE_URL || "";

//const token = useSelector((state: any) => state.token);

/*const token =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpZGFueW9zZWY0MiIsImlhdCI6MTY4NDU5NzkzOS45NDI5Mjc0LCJleHAiOjE2ODg1NzQ5NTd9.skmiNGlfp5cK28PqYSUZJupxUWGoI6qD7tV0xSkOcAU";
*/

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

const login = (path: string, obj: object) =>
  axios.post(`${API_URL}/${path}`, new URLSearchParams({ ...obj }), {
    headers: {
      accept: "application/json",
    },
  });

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
  getSearchResults,
  getPlantByName,
  getIsFavorite,
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

/*
const getFiveElements = (obj) => axios.get(API_URL, obj);

const getById = (id) => axios.get(API_URL + "/" + id);

const createData = (obj) => axios.post(API_URL, obj);

const updateData = (id, obj) => axios.put(API_URL + "/" + id, obj);

const deleteData = (id) => axios.delete(API_URL + "/" + id);

export { getFiveElements, getById, createData, updateData, deleteData };*/

/* http://ec2-3-20-223-255.us-east-2.compute.amazonaws.com:5000 */
