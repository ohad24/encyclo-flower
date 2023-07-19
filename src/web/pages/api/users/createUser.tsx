// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next';
import api from '../../../apis/serverAPI';

export default async function handler(
	req: NextApiRequest,
	res: NextApiResponse
) {
	const user = req.body;
	try {
		const { data } = await api.post('/users', user);
		console.log(user);

		res.status(res.statusCode).json(data);
	} catch (err: any) {
		console.log('herror', err.response.data, err.response.data.detail);
		res.status(err.response.status).send({ error: err.response.data.error });
	}
}
