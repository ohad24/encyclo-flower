/* eslint-disable @next/next/no-img-element */
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
const uploadfiles = () => {
	// const inputUpload = useRef<HTMLInputElement | undefined>(null);
	// const [uploading, setUploading] = React.useState(false);
	// const [selectedImage, setSelectedImage] = useState('');
	// const [selectedFile, setSelectedFile] = useState<File>();
	// const handleUpload = async () => {
	// 	setUploading(true);
	// 	try {
	// 		if (!selectedFile) return;
	// 		const formData = new FormData();
	// 		formData.append('myimage', selectedFile);
	// 		const { data } = await axios.post('/api/images', formData);
	// 		console.log(data);
	// 	} catch (err: any) {
	// 		console.log(err);
	// 	}
	// 	setUploading(false);
	// };
	// useEffect(() => {
	// 	if (selectedFile) handleUpload();
	// }, [selectedFile]);
	// return (
	// 	<div className='max-w-4xl mx-auto p-0 space-y-6'>
	// 		<input
	// 			type='file'
	// 			ref={inputUpload}
	// 			hidden
	// 			onChange={({ target }) => {
	// 				if (target.files) {
	// 					const file = target.files[0];
	// 					setSelectedImage(URL.createObjectURL(file));
	// 					setSelectedFile(file);
	// 				}
	// 			}}
	// 		/>
	// 		<div className='w-40 aspect-video rounded flex items-center justify-center border-dashed cursor-pointer'>
	// 			{selectedImage ? <img src={selectedImage} alt='' /> : 'Selectet Image'}
	// 		</div>
	// 		<button
	// 			disabled={uploading}
	// 			style={{ opacity: uploading ? '.5' : '1' }}
	// 			className='bg-red-600 p-3 w-32 text-center rounded text-white'
	// 			onClick={() => {
	// 				inputUpload?.current?.click();
	// 			}}
	// 		>
	// 			{uploading ? 'Uploading...' : 'Upload'}
	// 		</button>
	// 	</div>
	// );
};

export default uploadfiles;
