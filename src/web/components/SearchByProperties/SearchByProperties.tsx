import SearchIcon from "components/Icons/SearchIcon";

const SearchByProperties = () => {
  return (
    <label
      htmlFor="filePicker"
      className="cursor-pointer flex justify-center items-center gap-2 text-secondary bg-gradient-to-r from-[#FFA500] to-[#FFD700] transition duration-500 min-w-[248px] text-center p-1 rounded shadow hover:shadow-lg"
    >
      <SearchIcon /> <span>חיפוש חדש</span>
    </label>
  );
};

export default SearchByProperties;
