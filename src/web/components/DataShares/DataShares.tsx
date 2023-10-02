import LocationIcon from "components/Icons/LocationIcon";
import { useSelector } from "react-redux";

const DataShares = () => {
  const store = useSelector((state: any) => state);

  const getDate = () => {
    return (
      store.question.created_dt.slice(8, 10) +
      "." +
      store.question.created_dt.slice(5, 7) +
      "." +
      store.question.created_dt.slice(0, 4)
    );
  };

  return (
    <div className="max-w-[768px] m-auto">
      <p className="text-orange-300 text-2xl">{store.question.username}</p>
      <p className="text-xl text-sky-900 font-medium">
        {store.question.question_text}
      </p>
      <div className="flex gap-3 mt-3 font-medium">
        <div className="flex items-center cursor-pointer">
          <div className="relative h-[16px] w-[16px] flex">
            <LocationIcon color="#ffa255" size={13} />
          </div>
          <p className="text-xs text-orange-400">
            {store.question.location_name}
          </p>
        </div>
        <p className="text-xs text-sky-900">{getDate()}</p>
      </div>
    </div>
  );
};

export default DataShares;
