import { useDispatch, useSelector } from "react-redux";
import { updateImagesCommunity } from "redux/action";
import { deleteWithAuthorization, create } from "services/flowersService";
import RotateIcon from "components/Icons/CamaraIcon copy";

interface Props {
  path: string;
  index: number;
  image: any;
  images: Array<any>;
  setImages: (arrIds: Array<any>) => void;
}

const Image = ({ path, index, image, images, setImages }: Props) => {
  const store = useSelector((state: any) => state);
  const dispatch = useDispatch();

  const removeImage = async (index: number) => {
    try {
      const arr2: string[] = [...images];
      const img = arr2.splice(index, 1);
      await deleteWithAuthorization(
        store.isQuestion
          ? `${path}/images/${image.image_id}`
          : `${path}/image/${image.image_id}`,
        store.token
      );
      setImages(arr2);
      const arr1: File[] = Array.from(store.imagesCommunity);
      arr1.splice(index, 1);
      dispatch(updateImagesCommunity(arr1));
    } catch (err) {
      console.log(err);
    }
  };

  const rotateImage = async (index: number) => {
    try {
      await create(
        `${path}/images/${image.image_id}/rotate`,
        {
          angle: "R",
        },
        store.token
      );
      const element: HTMLElement | null = document.getElementById(
        `img${index}`
      )!;
      const currentRotate = element.style.transform;
      element.style.transform = currentRotate + "rotate(90deg)";
    } catch (err) {
      console.log(err);
    }
  };

  const src = store.isQuestion
    ? `${process.env.IMAGE_USER_BASE_URL}/questions/${image.file_name}`
    : `${process.env.IMAGE_USER_BASE_URL}/observations/${image.file_name}`;

  return (
    <div className="m-auto sm:m-0">
      <img
        id={`img${index}`}
        alt="undefined"
        src={src}
        className="w-[196px] h-[169px] rounded-3xl m-auto md:m-0 bg-blue-100 object-cover mb-2"
      />
      <div className="flex flex-row mt-1">
        <div className="mt-3" onClick={() => rotateImage(index)}>
          <RotateIcon />
        </div>
        <button
          type="button"
          onClick={() => removeImage(index)}
          className="text-sky-900 mr-6 font-medium"
        >
          <span className="text-2xl">x</span> הסר תמונה
        </button>
      </div>
    </div>
  );
};

export default Image;
