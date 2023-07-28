// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from "next";
import api from "apis/serverAPI";
type Data = {
  name: string;
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const searchFilters = req.body;
  try {
    const { data } = await api.post("/plants/search/", searchFilters);
    return res.status(200).send(data);
  } catch (err: any) {
    return res.status(err.statusCode).json({ error: err });
  }
}
