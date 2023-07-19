import { NextApiHandler, NextApiRequest } from 'next';
import formidable from 'formidable';
import path from 'path';
import fs from 'fs/promises';

export const config = {
	api: {
		bodyParser: false,
	},
};
const readFile = (
	req: NextApiRequest,
	saveLocally: boolean
): Promise<{ fields: formidable.Fields; files: formidable.Files }> => {
	const options: formidable.Options = {};
	if (saveLocally) {
		options.uploadDir = path.join(process.cwd(), '/public/images');
		options.filename = (name, ext, path, form) => {
			return Date.now().toString() + '_' + path.originalFilename;
		};
	}
	const form = formidable(options);
	return new Promise((resolve, reject) => {
		form.parse(req, (err, fields, files) => {
			console.log('parsing');
			if (err) reject(err);
			console.log('resolving');
			resolve({ fields, files });
		});
		console.log(' 2');
	});
};

const readFile2 = (
	req: NextApiRequest,
	saveLocally?: boolean
): Promise<{ fields: formidable.Fields; files: formidable.Files }> => {
	const options: formidable.Options = {};
	if (saveLocally) {
		options.uploadDir = path.join(process.cwd(), '/public/images');
		options.filename = (name, ext, path, form) => {
			return Date.now().toString() + '_' + path.originalFilename;
		};
	}
	options.maxFileSize = 4000 * 1024 * 1024;
	const form = formidable(options);
	return new Promise((resolve, reject) => {
		form.parse(req, (err, fields, files) => {
			if (err) reject(err);
			resolve({ fields, files });
		});
	});
};
const handler: NextApiHandler = async (req, res) => {
	console.log(req);
	try {
		await readFile(req, true);
		res.json({ message: 'completed' });
	} catch (err) {
		res.json({ error: err });
		console.log(err);
	}
};

export default handler;
