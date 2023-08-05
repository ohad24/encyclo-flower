import axios from "axios";

const API_URL = process.env.SERVER_BASE_URL || "";

const get = (path: string) => axios.get(`${API_URL}/${path}`);

const getWithAuthorization = (path: string, token: string) =>
  axios.get(`${API_URL}/${path}`, {
    headers: {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${token}`,
    },
  });

const post = (path: string, obj: object) =>
  axios.post(`${API_URL}/${path}`, new URLSearchParams({ ...obj }), {
    headers: {
      accept: "application/json",
    },
  });

// register
const postWithObj = (path: string, obj: object) =>
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

const postWithAuthorization = (path: string, data: any, token: string) =>
  axios.post(`${API_URL}/${path}`, data, {
    headers: {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${token}`,
    },
  });

const create = (path: string, data: any, token: string) =>
  axios.post(`${API_URL}/${path}`, JSON.stringify(data), {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });

const putWithAuthorization = (path: string, obj: object, token: string) =>
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

const deleteWithAuthorization = (path: string, token: string) =>
  axios.delete(`${API_URL}/${path}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

export {
  get,
  getWithAuthorization,
  post,
  postWithObj,
  postWithAuthorization,
  create,
  putWithAuthorization,
  deleteWithAuthorization,
};
