import { useDispatch, useSelector } from "react-redux";
import { updateSelectedImages } from "redux/action";

const ImagePlant = (props: { index: number; selectedImage: any }) => {
  const store = useSelector((state: any) => state);
  const dispatch = useDispatch();

  const removeImage = (index: number) => {
    const arr: File[] = Array.from(store.selectedImages);
    arr.splice(index, 1);
    dispatch(updateSelectedImages(arr));
  };

  return (
    <div key={props.index} className="m-auto md:m-0">
      <div>
        <img
          alt="undefined"
          src={URL.createObjectURL(store.selectedImages[props.index])}
          className="w-[374px] h-[306px] rounded-3xl object-cover"
        />
        <button
          onClick={() => removeImage(props.index)}
          className="text-red-600"
        >
          <span className="text-2xl">x</span> הסר תמונה
        </button>
      </div>
    </div>
  );
};
export default ImagePlant;
