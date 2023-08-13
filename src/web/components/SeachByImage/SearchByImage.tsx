import GalleryIcon from "components/Icons/Gallery";

const SearchByImage = () => {
  return (
    <label
      htmlFor="filePicker"
      className="cursor-pointer text-center flex flex-col-reverse text-base m-auto text-secondary bg-gradient-to-r from-[#FFA500] to-[#FFD700] transition duration-500 h-[100px] w-[120px] rounded-3xl"
    >
      <span className="table m-auto">
        <span className="table m-auto">
          <GalleryIcon size={22} />
        </span>
        <span className="flex flex-wrap leading-5 max-w-[100px] font-bold">
          חיפוש בעזרת תמונה
        </span>
      </span>
    </label>
  );
};

export default SearchByImage;
